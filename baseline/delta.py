import argparse
import os
import sys
import openai
import pandas as pd
from pathlib import Path

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "util"))
sys.path.append(os.path.join(project_root, "baseline"))

from data.delta.scene_graph import load_scene_graph, prune_sg_with_item, extract_accessible_items_from_sg
from data.delta import example
from data.delta.target import generate_domain_query
from datetime import datetime
import util.delta_util.llm as llm
import util.delta_util.llm_utils as llm_utils
import util.delta_util.planner as planner
import util.delta_util.prompt as p
import time

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Parameters
DEFAULT_LLM = "gpt-4o"
TEMPERATURE = 0.0
TOP_P = 1.0
EPISODE = 2
MAX_TIME = 60

# Examples (prompt 예시용으로 EXHOME 사용)
DOMAIN_EXAMPLE = "exhousework"
SCENE_EXAMPLE   = "exhome"

# Queries (실제 실행할 HOME 도메인/씬)
DOMAIN_QUERY    = "housework"
SCENE_QUERY     = "home"


def SRC_DOMAIN_PATH(d):
    return f"./data/delta/domain/{d}_domain.pddl"


def SRC_PROBLEM_PATH(s, d):
    return f"./data/delta/problem/{s}_{d}_problem.pddl"


def LOG_PATH(t):
    return f"result/{t}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--experiment", "-e", nargs="+", default=["all"],
        choices=["all", "domain", "prune", "problem", "decompose"]
    )
    parser.add_argument(
        "-m", "--model", type=str, default=DEFAULT_LLM
    )
    parser.add_argument(
        "-t", "--temperature", type=float, default=TEMPERATURE
    )
    parser.add_argument(
        "--top-p", type=float, default=TOP_P,
    )
    parser.add_argument(
        "--print-prompt", action="store_true", default=True
    )
    parser.add_argument(
        "--print-response", action="store_true", default=True
    )
    parser.add_argument(
        "--print-plan", action="store_true", default=False
    )

    parser.add_argument(
        "-d", "--domain", type=str, dest="domain", default=DOMAIN_QUERY
    )
    parser.add_argument(
        "--domain-example", type=str, dest="domain_example", default=DOMAIN_EXAMPLE
    )
    parser.add_argument(
        "-s", "--scene", type=str, dest="scene", default=SCENE_QUERY
    )
    parser.add_argument(
        "--scene-example", type=str, dest="scene_example", default=SCENE_EXAMPLE
    )
    parser.add_argument(
        "--no-plan", action="store_true", default=False
    )
    parser.add_argument(
        "--max-time", type=float, dest="max_time", default=MAX_TIME
    )
    parser.add_argument(
        "--logdir", "-l", type=str, dest="logdir", default="result"
    )
    parser.add_argument("-n", "--episode", type=int, dest="episode", default=EPISODE
    )

    args = parser.parse_args()
    if "all" in args.experiment and any(x in ["domain", "problem", "decompose"] for x in args.experiment):
        raise argparse.ArgumentError("Duplicate experiments!")
    if args.scene == args.scene_example:
        raise argparse.ArgumentError(
            "Scene graph example cannot be identical to scene graph query!")
    print("Using model {}".format(args.model))

    # Loading files
    domain_exp, problem_exp = None, None
    if os.path.isfile(SRC_DOMAIN_PATH(args.domain_example)):
        with open(SRC_DOMAIN_PATH(args.domain_example), "r") as src_d_file:
            domain_exp = src_d_file.read()
    else:
        raise Exception(
            "Cannot load domain example {}".format(args.domain_example))
    if os.path.isfile(SRC_PROBLEM_PATH(args.scene_example, args.domain_example)):
        with open(SRC_PROBLEM_PATH(args.scene_example, args.domain_example), "r") as src_p_file:
            problem_exp = src_p_file.read()
    else:
        raise Exception(
            "Cannot load problem example {}".format(args.scene_example))
    print("Domain example: {} \nScene example: {} \nDomain query: {} \nScene query: {}".format(
        args.domain_example, args.scene_example, args.domain, args.scene))

    # Additional information for prompting
    exp = example.get_example(args.domain_example)
    qry = example.get_example(args.domain)
    if args.scene_example not in exp["scene"]:
        raise Exception("Scene example {} is not supported for domain example{}!".format(
            args.scene_example, args.domain_example))
    if args.scene not in qry["scene"]:
        raise Exception("Scene {} is not supported for domain {}!".format(
            args.scene, args.domain))
    add_obj_exp = exp["add_obj"]
    add_act_exp = exp["add_act"]
    goal_exp = exp["goal"]
    subgoal_exp = exp["subgoal"]
    item_keep_exp = exp["item_keep"]
    add_obj_qry = qry["add_obj"]
    add_act_qry = qry["add_act"]
    goal_qry = qry["goal"]
    gt_cost = qry["gt_cost"][args.scene]

    curr_time = datetime.now().strftime("%Y%m%d_%H%M%S/")
    success = 0
    success_orig = 0
    data_list = []

    # Loading LLM
    model = llm.load_llm(args.model, args.temperature, args.top_p)

    for e in range(args.episode):
        model.reset()

        log_path = os.path.join(LOG_PATH(curr_time), "e_{:03}/".format(e))
        Path(log_path).mkdir(parents=True, exist_ok=True)

        scene_exp = load_scene_graph(args.scene_example)
        scene_qry = load_scene_graph(args.scene)

        domain_tar, problem_tar = None, None
        d_tar_file = os.path.join(
            log_path, "{}_domain.pddl".format(args.domain))
        p_tar_file = os.path.join(
            log_path, "{}_{}_problem.pddl".format(args.scene, args.domain))
        plan_file = os.path.join(
            log_path, "{}_{}.plan".format(args.domain, args.scene))
        plan_decomp_file = os.path.join(
            log_path, "{}_{}_decomp.plan".format(args.domain, args.scene))

        d_time, pr_time, p_time, dp_time = 0., 0., 0., 0.
        subgoal_pddl_list = []
        item_keep = []
        start = time.time()

        ###################### Stage 1: Generating domain file ######################
        if "all" in args.experiment or "domain" in args.experiment:
            content_d, prompt_d = p.nl_2_pddl_domain(
                domain_exp, args.domain, add_obj_exp, add_obj_qry, add_act_exp, add_act_qry)
            print("Prompt tokens for domain generation: {}".format(
                model.count_tokens(prompt_d)))
            if args.print_prompt:
                model.log(content_d + prompt_d, os.path.join(
                    log_path, "{}_domain.prompt".format(args.domain)))
            model.init_prompt_chain(content_d, prompt_d)
            d_start = time.time()
            domain_tar = model.query_msg_chain()
            d_time = time.time() - d_start
            if args.print_response:
                model.log(domain_tar, os.path.join(
                    log_path, "{}_domain.response".format(args.domain)))
            llm_utils.export_result(domain_tar, d_tar_file)
            print(
                "Response time for generating domain file: {:.2f}s".format(d_time))
            model.update_prompt_chain_w_response(domain_tar)

        ###################### Step 2: Pruning scene graph items ######################
        if "all" in args.experiment or "prune" in args.experiment:
            items_exp = extract_accessible_items_from_sg(scene_exp)
            items_qry = extract_accessible_items_from_sg(scene_qry)
            if domain_tar is None:
                with open(SRC_DOMAIN_PATH(args.domain), "r") as df:
                    domain_tar = df.read()
            content_pr, prompt_pr = p.nl_prune_item(
                items_exp, items_qry, goal_exp, goal_qry, item_keep_exp, domain_exp, domain_tar)
            print("Prompt tokens for pruning scene graph: {}".format(
                model.count_tokens(prompt_pr)))
            if args.print_prompt:
                model.log(content_pr + prompt_pr, os.path.join(
                    log_path, "{}_prune.prompt".format(args.scene)))

            if "all" in args.experiment or "domain" in args.experiment:
                model.update_prompt_chain(content_pr, prompt_pr)
            else:
                model.init_prompt_chain(content_pr, prompt_pr)
            pr_start = time.time()
            prune_tar = model.query_msg_chain()
            pr_time = time.time() - pr_start
            if args.print_response:
                model.log(prune_tar, os.path.join(
                    log_path, "{}_{}_prune.response".format(args.scene, args.domain)))
            item_keep = llm_utils.export_obj_list(prune_tar)
            print("Items to keep: {}".format(item_keep))
            print(
                "Response time for pruning scene graph: {:.2f}s".format(pr_time))
            model.update_prompt_chain_w_response(prune_tar)
            scene_exp = prune_sg_with_item(scene_exp, item_keep_exp)
            scene_qry = prune_sg_with_item(scene_qry, item_keep)

        ###################### Stage 3: Generating problem file ######################
        if "all" in args.experiment or "problem" in args.experiment:
            # Load ground truth domain file for stand-alone experiment
            if domain_tar is None:
                with open(SRC_DOMAIN_PATH(args.domain), "r") as df:
                    domain_tar = df.read()

            content_p, prompt_p = p.sg_2_pddl_problem(args.domain_example,
                                                      domain_exp, problem_exp,
                                                      scene_exp, scene_qry, goal_exp,
                                                      goal_qry, domain_tar, args.domain)
            print("Prompt tokens for problem generation: {}".format(
                model.count_tokens(prompt_p)))
            if args.print_prompt:
                model.log(content_p + prompt_p, os.path.join(
                    log_path, "{}_{}_prob.prompt".format(args.scene, args.domain)))

            if "all" in args.experiment or "domain" in args.experiment or "prune" in args.experiment:
                model.update_prompt_chain(content_p, prompt_p)
            else:
                model.init_prompt_chain(content_p, prompt_p)
            p_start = time.time()
            problem_tar = model.query_msg_chain()
            p_time = time.time() - p_start
            if args.print_response:
                model.log(problem_tar, os.path.join(
                    log_path, "{}_{}_prob.response".format(args.scene, args.domain)))
            llm_utils.export_result(problem_tar, p_tar_file)
            print(
                "Response time for generating problem file: {:.2f}s".format(p_time))
            model.update_prompt_chain_w_response(problem_tar)

        ###################### Stage 4: Decomposing problem file ######################
        if "all" in args.experiment or "decompose" in args.experiment:
            # Load domain and problem files for stand-alone experiment
            if domain_tar is None:
                with open(SRC_DOMAIN_PATH(args.domain), "r") as df:
                    domain_tar = df.read()
            if problem_tar is None:
                with open(SRC_PROBLEM_PATH(args.scene, args.domain), "r") as pf:
                    problem_tar = pf.read()

            accumulate_subgoal = True if args.domain == "office" else False
            if "all" in args.experiment or "domain" in args.experiment or \
                    "prune" in args.experiment or "problem" in args.experiment:
                content_dp, prompt_dp = p.decompose_problem_chain(
                    goal_exp, subgoal_exp, exp["subgoal_pddl"], item_keep_exp,
                    goal_qry, problem_exp, item_keep, problem_tar, domain_tar,
                    accumulate_subgoal)
                model.update_prompt_chain(content_dp, prompt_dp)
            else:
                content_dp, prompt_dp = p.decompose_problem(
                    goal_exp, subgoal_exp, exp["subgoal_pddl"], item_keep_exp,
                    goal_qry, problem_exp, item_keep, problem_tar, domain_tar,
                    accumulate_subgoal)
                model.init_prompt_chain(content_dp, prompt_dp)
            print("Prompt tokens for problem decomposition: {}".format(
                model.count_tokens(prompt_dp)))
            if args.print_prompt:
                model.log(content_dp + prompt_dp, os.path.join(
                    log_path, "{}_{}_decomp.prompt".format(args.scene, args.domain)))
            dp_start = time.time()
            decomp_tar = model.query_msg_chain()
            dp_time = time.time() - dp_start
            subgoal_pddl_list = llm_utils.export_subgoal_list(decomp_tar)
            if args.print_response:
                model.log(decomp_tar, os.path.join(
                    log_path, "{}_{}_decomp.response".format(args.scene, args.domain)))
            print(
                "Response time for decomposing problem file: {:.2f}s".format(dp_time))
            model.update_prompt_chain_w_response(decomp_tar)

        total_llm_time = d_time + pr_time + p_time + dp_time
        print("Total response time of {}: {:.2f}s".format(
            args.model, total_llm_time))

        if args.no_plan:
            continue

        ##################### Generating task plan(s) ######################
        # Copy generated domain and (sub-)problem files in pddlgym directory
        if not os.path.isfile(d_tar_file):
            d_tar_file = SRC_DOMAIN_PATH(args.domain)
        if not os.path.isfile(p_tar_file):
            p_tar_file = SRC_PROBLEM_PATH(args.scene, args.domain)
        planner.export_domain_to_pddlgym(args.domain, d_tar_file)
        planner.export_problem_to_pddlgym(args.domain, p_tar_file, p_idx="00" if len(
            str(len(subgoal_pddl_list))) > 1 else "0", clear_dir=True)
        planner.register_new_pddlgym_env(args.domain)

        # First execute planner with undecomposed problem to get planning time
        plan, plan_time, node, cost, exit_code = planner.query_pddlgym(
            args.domain, max_time=args.max_time)
        if exit_code == 1:
            with open(plan_file, "w") as pf:
                pf.write("\n".join(plan))
            is_valid, val_info = planner.validate(SRC_DOMAIN_PATH(
                args.domain), SRC_PROBLEM_PATH(args.scene, args.domain), plan_file)
            # if cost == gt_cost or is_valid:
            if is_valid:
                success_orig += 1
            else:
                exit_code = 0

        # Hierarchical planning for sub-problems
        if len(subgoal_pddl_list) > 0:
            plans, times, nodes, costs, exit_code_decomp, completed_sp = planner.query_pddlgym_decompose(
                args.domain, subgoal_pddl_list, save_path=log_path, max_time=args.max_time)
            if exit_code_decomp == 1:
                with open(plan_decomp_file, "w") as pdf:
                    for sp in plans:
                        pdf.writelines("\n".join(sp) + "\n\n")
                is_valid_decomp, val_info_decomp = planner.validate(SRC_DOMAIN_PATH(
                    args.domain), SRC_PROBLEM_PATH(args.scene, args.domain), plan_decomp_file)
                # if sum(costs) == gt_cost or is_valid_decomp:
                if is_valid_decomp:
                    success += 1
                else:
                    exit_code_decomp = 0
        else:
            print("No decomposed subgoals!")
            plans, times, nodes, costs, completed_sp = [], [], [], [], None
            exit_code_decomp = 7

        print("==================== Episode {}/{}, Success Orig. {}, Total Success: {} ====================".format(
            e + 1, args.episode, success_orig, success))
        data_list.append([e, exit_code, exit_code_decomp, success, success_orig, args.experiment, args.model, args.temperature,
                          args.domain_example, args.scene_example, args.domain, args.scene,
                          d_time, pr_time, p_time, dp_time,  total_llm_time,
                          len(subgoal_pddl_list), completed_sp, plan_time, cost, node,
                          sum(times), times, sum(nodes), nodes,
                          sum(costs), costs, gt_cost, item_keep])

    if args.no_plan:
        quit()

    df = pd.DataFrame(data_list, columns=["Episode", "Exit Code", "Exit Code Decomp", "Total Success Decomp", "Total Success Orig", "Experiment", "LLM", "Temp",
                                          "Domain Exp", "Scene Exp", "Domain Qry", "Scene Qry",
                                          "Time Domain", "Time Prune", "Time Problem", "Time Decomp", "Total LLM Time",
                                          "Subgoals", "Completed Subgoals", "Plan Time", "Cost", "Node Expanded",
                                          "Plan Time Decomp", "Plan Time Sub-P",
                                          "Node Expanded Decomp", "Node Expanded Sub-P",
                                          "Cost Decomp", "Cost Sub-P", "GT Cost", "Items Keep"])
    df.to_csv(os.path.join(LOG_PATH(curr_time), "log.csv"))
    print("Success rate w/o decomposition: {:.2f}%".format(
        success_orig / args.episode * 100.))
    print("Success rate with decomposition: {:.2f}%".format(
        success / args.episode * 100.))
