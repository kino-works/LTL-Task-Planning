import os
from pathlib import Path
import pddlgym
from pddlgym_planners.fd import FD
import shutil
import subprocess
import util.delta_util.utils as utils


PLANNER = "./downward/fast-downward.py "
ALIAS = "--alias seq-opt-lmcut "
MAX_ERR_MSG_LEN = 100
PDDLGYM_PATH = os.path.dirname(pddlgym.__file__)


def SEARCH_CONFIG(
    mt): return "--search 'astar(lmcut(), max_time={})' ".format(mt)


def query(domain_path: str, problem_path: str, plan_file: str, print_plan: False, max_time: float = 120):
    plan_file = os.path.join(os.getcwd(), plan_file)
    command = PLANNER + "--plan-file {} ".format(plan_file) +\
        domain_path + " " + problem_path + " " + SEARCH_CONFIG(max_time)

    # Execute planner
    print("Planning...")
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()

    exit_code = 0
    cost = 0
    plan_time = 0.
    plan = None
    err_msg = err.decode()
    #print("output:", output)
    if "Solution found" in str(output):
        for line in str(output).split("\\n"):
            if "Plan cost: " in line:
                cost = int(line.strip().split(" ")[-1])
            if "Planner time: " in line:
                plan_time = float(line.strip().split(" ")[-1].replace("s", ""))
        print("Found solution in {} with cost {}".format(plan_time, cost))
        # Read plan file
        if os.path.isfile(plan_file):
            with open(plan_file, "r") as pf:
                plan = pf.read()
        if print_plan:
            print("Task plan: \n{}".format(plan))
        exit_code = 1
    else:
        # TODO: error handling with exit code
        print(err_msg)
        if "Time limit reached" in err_msg or "Time limit reached" in str(output):
            exit_code = 3
        elif "Argument" in err_msg and "not in params" in err_msg:
            exit_code = 4
        elif "Undeclared predicate" in err_msg or ("Predicate" in err_msg and "not defined" in err_msg):
            exit_code = 5
        else:
            exit_code = 2
        print("Could not find solution")

    return plan, cost, plan_time, exit_code, err_msg


def export_domain_to_pddlgym(domain: str, src_domain_file: str):
    dst_domain_file = os.path.join(
        PDDLGYM_PATH, "pddl/{}.pddl".format(domain))
    if os.path.isfile(dst_domain_file):
        os.remove(dst_domain_file)
    shutil.copyfile(src_domain_file, dst_domain_file)


def export_problem_to_pddlgym(domain: str, src_problem_file: str, p_idx: str, clear_dir=False):
    dst_problem_path = os.path.join(
        PDDLGYM_PATH, "pddl/{}/".format(domain))
    Path(dst_problem_path).mkdir(parents=True, exist_ok=True)
    if clear_dir:
        for f in os.listdir(dst_problem_path):
            os.remove(os.path.join(dst_problem_path, f))
    dst_problem_file = os.path.join(
        dst_problem_path, "problem{}.pddl".format(p_idx))
    shutil.copyfile(src_problem_file, dst_problem_file)


def register_new_pddlgym_env(new_domain: str):
    new_env = (new_domain, {'operators_as_actions': True,
               'dynamic_action_space': True})
    new_line = "\t\t" + str(new_env) + ",\n"

    with open(os.path.join(PDDLGYM_PATH, "__init__.py"), "r+") as file:
        lines = file.readlines()
        if new_line not in lines:
            print("Registering new PDDLGym environment '{}'...".format(new_domain))
            for i, line in enumerate(lines):
                if "for env_name, kwargs in [" in line:
                    lines.insert(i + 1, new_line)
                    file.seek(0)
                    file.writelines(lines)
        else:
            print("PDDLGym environment '{}' already registered!".format(new_domain))


def query_pddlgym(domain: str, p_idx: int = 0, max_time: float = 120):
    plan = None
    cost = 0
    node = 0
    time = 0.
    exit_code = 0
    print("Planning with undecomposed problem...")

    try:
        fd_planner = FD()
        env = pddlgym.make("PDDLEnv{}-v0".format(domain.capitalize()))
        env.fix_problem_index(p_idx)
        state, _ = env.reset()
        plan = fd_planner(env.domain, state, timeout=max_time)
        statistic = fd_planner.get_statistics()
        time = statistic["total_time"]
        cost = statistic["plan_cost"]
        node = statistic["num_node_expansions"]
        for act in plan:
            state, reward, done, truncated, info = env.step(act)
        exit_code = 1
    except Exception as err:
        print("err (repr):", repr(err))
        print("err (str):", str(err))
        err_msg = str(err)
        print("Could not find solution!", err_msg)
    return [p.pddl_str() for p in plan] if exit_code == 1 else None, time, node, cost, exit_code


def query_pddlgym_decompose(domain: str, subgoal_pddl_list: list, save_path: str = None, max_time: float = 120):
    digits = 2 if len(str(len(subgoal_pddl_list))) > 1 else 1
    d_file = os.path.join(PDDLGYM_PATH, "pddl/{}.pddl".format(domain))
    p_0_file = os.path.join(
        PDDLGYM_PATH, "pddl/{}/problem{}.pddl".format(domain, str(0).zfill(digits)))
    assert os.path.isfile(d_file), "Missing domain file in PDDLGym directory!"
    assert os.path.isfile(
        p_0_file), "Missing initial problem file in PDDLGym directory!"
    assert len([name for name in os.listdir(os.path.join(PDDLGYM_PATH, "pddl/{}/".format(domain)))
                if os.path.isfile(os.path.join(PDDLGYM_PATH, "pddl/{}/{}".format(domain, name)))]) == 1, \
        "PDDLGym problem directory contains more than 1 file!"
    print("Planning with decomposed problems...")

    plans = []
    times = []
    nodes = []
    costs = []
    final_state_list = []
    exit_code = 0
    fd_planner = FD()
    completed_sp = 0

    for idx, sgp in enumerate(subgoal_pddl_list, start=1):
        # Create new sub-problem file with new states and sub-goal
        sp_file = os.path.join(
            PDDLGYM_PATH, "pddl/{}/problem{}.pddl".format(domain, str(idx).zfill(digits)))

        shutil.copyfile(p_0_file, sp_file)
        try:
            utils.set_pddl_problem_goal(sp_file, sgp)
            if idx > 1:
                utils.set_pddl_problem_init(sp_file, final_state_list)
        except Exception as err:
            exit_code = 6
            print("Error when writing PDDL states!", str(err))

        # Log sub-problem file
        if save_path is not None:
            save_file = os.path.join(
                save_path, "p{}.pddl".format(str(idx).zfill(digits)))
            shutil.copyfile(sp_file, save_file)

        # Planning with sub-problem
        plan, statistic = None, None
        try:
            env = pddlgym.make("PDDLEnv{}-v0".format(domain.capitalize()))
            env.fix_problem_index(idx)
            state, _ = env.reset()
            plan = fd_planner(env.domain, state, timeout=max_time)
            statistic = fd_planner.get_statistics()
            print("Subgoal: {}/{}, Plan time: {:.2f}s, Plan cost: {}".format(
                idx, len(subgoal_pddl_list), statistic["total_time"], statistic["plan_cost"]))
            for act in plan:
                state, reward, done, truncated, info = env.step(act)
            final_state_list = sorted(
                [lit.pddl_str() for lit in state.literals if not lit.is_negative])
            # print("final:", final_state_list)
            completed_sp += 1
            exit_code = 1
        except Exception as err:
            # TODO: error handling with exit code
            err_msg = str(err)
            if "Planning timed out" in err_msg:
                exit_code = 3
            elif "Argument" in err_msg and "not in params" in err_msg:
                exit_code = 4
            elif "Undeclared predicate" in err_msg or ("Predicate" in err_msg and "not defined" in err_msg):
                exit_code = 5
            else:
                exit_code = 2
            print(" not find solution!", err_msg)
            break
        plans.append([p.pddl_str() for p in plan] if plan is not None else "")
        times.append(statistic["total_time"] if statistic is not None else 0.)
        nodes.append(statistic["num_node_expansions"]
                     if statistic is not None else 0)
        costs.append(statistic["plan_cost"] if statistic is not None else 0)

    print("Total plan time of all sub-problems: {:.2f}s".format(sum(times)))
    print("Total cost: {}".format(sum(costs)))
    return plans, times, nodes, costs, exit_code, completed_sp


def validate(domain_file: str, problem_file: str, plan_file: str):
    command = "Validate -v " + domain_file + \
        " " + problem_file + " " + plan_file
    print("command:", command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p.wait()

    #print(err)
    if "Plan valid" in str(output):
        print("VAL: Plan valid!")
        return True, "Plan succeeded."
    else:
        print("VAL: Plan invalid!")
        repair_phrase = "Plan Repair Advice:"
        if repair_phrase in str(output):
            out_str = str(output)
            msg = out_str[out_str.index(repair_phrase) + len(repair_phrase):]
            msg, _ = msg.split("Failed plans:")
            msg = "NOTE: " + msg.strip()
        else:
            msg = "NOTE: The plan did not achieve the goal."
        return False, msg


def val_feedback(err_msg: str):
    feedback = "Plan did not achieve the goal!"
    prefix = [x for x in err_msg.split("\\n") if x][1] + ", " \
        if "\\n" in err_msg else ""
    exit_code = 2

    if "(Set (neighbor " in err_msg and "to true)" in err_msg:
        # Unconnected rooms
        error = err_msg[err_msg.find(
            "(Set (neighbor ") + len("(Set (neighbor "):].split(" ")
        feedback = "Cannot go from {} to {}, they are not neighbors!".format(
            error[0], error[1])
        exit_code = 3
    elif "(Set (item_at " in err_msg and "to true)" in err_msg:
        # Wrong item location
        error = err_msg[err_msg.find(
            "(Set (item_at ") + len("(Set (item_at "):].split(" ")
        feedback = "Item {} is not in room {}!".format(
            error[0], error[1])
        exit_code = 4
    elif "(pick robot locker" in err_msg or "(pick robot shelf" in err_msg\
            or "(drop robot locker" in err_msg or "(drop robot shelf" in err_msg:
        # Invalid robot action
        err_act = err_msg[err_msg.find("(") + 1: err_msg.find("robot") - 1]
        err_item = err_msg[err_msg.find(
            "robot") + len("robot") + 1:].split(" ")[0]
        feedback = "Invalid action! Robot cannot {} {}!".format(
            err_act, err_item)
        exit_code = 5
    else:
        feedback += err_msg

    return prefix + feedback, exit_code
