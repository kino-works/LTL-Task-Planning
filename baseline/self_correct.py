import os
import sys
import time
import datetime
import argparse
import openai
import re
import copy 
import json

# Project paths (adjust if needed)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "util"))
sys.path.append(os.path.join(project_root, "baseline"))

from dotenv import load_dotenv

# util imports (edit to your actual module names)
from util.isr_llm_util.Translator import Translator
from util.isr_llm_util.Planner import Planner
from util.isr_llm_util.Validator import Validator
from util.isr_llm_util.Household_Sim import HouseholdSim
from util.isr_llm_util.utils import (
    extract_state_pddl,
    extract_action_description,
)

def load_scenarios(input_filepath, scenarios_filepath):
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            test_inputs = json.load(f)
        with open(scenarios_filepath, 'r', encoding='utf-8') as f:
            scenarios_data = json.load(f)
    except FileNotFoundError as e:
        print(f"cannot find file {e.filename}")
        sys.exit(1)

    scenario_map = {s['scene']: s for s in scenarios_data}
    final_initial_states = []
    final_goal_states = []
    final_tasks_info = []

    for test in test_inputs:
        scene_name = test.get("scene")
        scenario_template = scenario_map[scene_name]

        base_initial_state = scenario_template['initial_state']
        goal_options = scenario_template['goal_state']

        for task_group in test['domain']:
            current_goal_state = []
            for task in task_group:
                if task in goal_options:
                    predicates = goal_options[task]
                    if isinstance(predicates, list):
                        current_goal_state.extend(predicates)
                    else:
                        current_goal_state.append(predicates)
                else:
                    print(f"'cannot find goal state about '{task}'")

            final_initial_states.append(base_initial_state)
            final_goal_states.append(str(current_goal_state).replace("'", ""))
            final_tasks_info.append({
                "scene": scene_name,
                "selected_task": task_group
            })

    return final_initial_states, final_goal_states, final_tasks_info


def run_episode(
    simulator: HouseholdSim,
    initial_state,
    goal_state,
    base_logdir: str, 
    test_idx: int,
    episode_idx: int,
    max_num_refine: int,
    max_refine_temperature: float,
    args_obj,  
    wait_seconds: float,
):
    episode_log_dir = os.path.join(base_logdir, f"test{test_idx}", f"ep{episode_idx}")
    os.makedirs(episode_log_dir, exist_ok=True) 

    test_log_file_path = os.path.join(episode_log_dir, "test_log.txt")     
    final_plan_file_path = os.path.join(episode_log_dir, "final_plan.plan")

    time.sleep(wait_seconds)
    args_test = copy.copy(args_obj)    
    args_test.logdir = episode_log_dir   

    setattr(args_test, "prompt_example_root", args_test.trans_prompt_dir)  
    translator = Translator(args_test, is_log_example=True)                

    setattr(args_test, "prompt_example_root", args_test.plan_prompt_dir)   
    planner = Planner(args_test, is_log_example=True)                     

    setattr(args_test, "prompt_example_root", args_test.valid_prompt_dir)  
    validator = Validator(args_test, is_log_example=True)                 

    with open(test_log_file_path, "w") as f:                               
        f.write(f"[Test {test_idx}, Episode {episode_idx}] Log for household.\n")   
    
    # 1) NL description
    description = simulator.generate_scene_description(initial_state, goal_state)
    print(description)
    with open(test_log_file_path, "a") as f:
        f.write(f"Test case index: {test_idx}, Episode: {episode_idx}\n")
        f.write(description + "\n")

    # 2) Translator → planning problem
    resp_txt = translator.query(description, is_append=False)
    planning_problem = resp_txt
    
    # Extract init/goal for validator prompt
    pddl_init_state, pddl_goal_state = extract_state_pddl(planning_problem, domain="household")

    # 3) Refinement loop
    self_eval_success = False
    action_description = ""  

    for j in range(max_num_refine + 1):
        time.sleep(wait_seconds)

        simulator.initialize_state(initial_state)

        with open(test_log_file_path, "a") as f:
            f.write(f"Attempt: {j}\n")

        temperature = 0 if test_idx == 1 else min(max_refine_temperature, 0.1 * (test_idx - 1))
        action_sequence = planner.query(planning_problem, is_append=True, temperature=temperature)
        
        print("Attempt", j)
        #print(action_sequence)
        with open(test_log_file_path, "a") as f:
            f.write(action_sequence + "\n")
            f.write("Analysis: \n")

        # 4) Self evaluation
        action_description = extract_action_description(action_sequence, domain="household")

        validate_question = "Question:\nInitial state: \n" + pddl_init_state + "\nGoal state:\n" + pddl_goal_state + "\nExamined action sequence:\n" + action_description
        print(validate_question)
        with open(test_log_file_path, "a") as f:
            f.write(validate_question + "\n")

        time.sleep(wait_seconds)
        validator_text = validator.query(validate_question, is_append=True)
        with open(test_log_file_path, "a") as f:
            f.write(validator_text + "\n")

        # Parse "Final answer:" token
        parts = validator_text.split("Final answer:", 1)
        if len(parts) == 1:
            print("Validator returned no 'Final answer' token. Breaking.")
            break
        final_answer = parts[1].strip()
        fa_norm = final_answer.lower().strip()
        if fa_norm.startswith("yes"):
            self_eval_success = True
            print("Self-evaluation suggests a solution.")
            with open(test_log_file_path, "a") as f:
                f.write("Self-evaluation suggests a solution.\n")
            break
        elif fa_norm.startswith("no"):
            print("Self-evaluation suggests a failure.")
            error_description = "Goal is not satisfied. "
            planning_problem = (
                error_description
                + "Please find a new plan by considering the household constraints and object locations. "
            )
            with open(test_log_file_path, "a") as f:
                f.write(planning_problem + "\n")
        else:
            print("Unknown validator decision:", final_answer)
            with open(test_log_file_path, "a") as f:
                f.write(f"Unknown validator decision: {final_answer}\n")
    # Refinement loop finish

    print("Actual analysis:")
    with open(test_log_file_path, "a") as f:
        f.write("Actual analysis:\n")

    with open(final_plan_file_path, "w") as f:
        f.write(action_description)
    
    raw_actions = action_description
    parsed = re.findall(r"\((.*?)\)", raw_actions, flags=re.S)
    if parsed:
        actions = [a.strip() for a in parsed]
    else:
        actions = [line.strip() for line in raw_actions.splitlines() if line.strip()]

    if not action_description.strip():
        with open(test_log_file_path, "a") as f:
            f.write("No action_description; skipping simulation.\n")
        success, failure, err_msg, failed_action = False, True, "empty plan", None
    else:
        success, failure, err_msg, failed_action = simulator.simulate_actions(actions, test_log_file_path)

    if (success and not failure) and self_eval_success:
        validation_status = "Success"
        with open(test_log_file_path, "a") as f:
            reason = "by simulation" if (success and not failure) else "by self-evaluation"
            f.write(f"Validation marked Success ({reason}).\n")
            if success and not failure:
                f.write("Simulation completed successfully.\n")
    else:
        validation_status = "Failure"
        with open(test_log_file_path, "a") as f:
            if not (success and not failure):
                f.write(f"Simulation failed at action: {failed_action}, reason: {err_msg}\n")
            f.write("Validation marked Failure.\n")

    planner.init_messages(is_reinitialize=True)

    with open(test_log_file_path, "a") as f:
        f.write(f"End of Test {test_idx}, Episode {episode_idx}\n\n\n")

    return validation_status


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--logdir", type=str, default=None)
    parser.add_argument('--domain', type=str, default="household")
    parser.add_argument("--num_trans_ex", type=int, default=4)
    parser.add_argument("--num_plan_ex", type=int, default=4)
    parser.add_argument("--num_valid_ex", type=int, default=8)
    parser.add_argument("--num_test", type=int, default=1)
    parser.add_argument("--max_refine", type=int, default=5)
    parser.add_argument("--max_temp", type=float, default=0.4)
    parser.add_argument("--wait_sec", type=float, default=30)
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--trans_prompt_dir", default="data/self_correct/trans")
    parser.add_argument("--plan_prompt_dir",  default="data/self_correct/plan")
    parser.add_argument("--valid_prompt_dir", default="data/self_correct/valid")
    parser.add_argument("--test_input_file", type=str, default="baseline/test_input.json")
    parser.add_argument("--test_scenarios_file", type=str, default="data/isr_llm/test_scenarios.json")

    args = parser.parse_args()

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Log dir
    if args.logdir is None:
        args.logdir = os.path.join(project_root, "results", "self_correct")
    os.makedirs(args.logdir, exist_ok=True)

    simulator = HouseholdSim()

    base_initial_states, base_goal_states,  base_tasks_info= load_scenarios(
        args.test_input_file, args.test_scenarios_file
    )

    num_base_tests = len(base_initial_states)
    all_results = []

    for i in range(num_base_tests):
        for j in range(args.num_test):
            test_idx = i + 1
            episode_idx = j + 1

            validation_status = run_episode(
                initial_state=base_initial_states[i],
                goal_state=base_goal_states[i],
                test_idx=test_idx,
                episode_idx=episode_idx,
                base_logdir=args.logdir,
                simulator=simulator,
                max_num_refine=args.max_refine,
                max_refine_temperature=args.max_temp,
                args_obj=args,
                wait_seconds=args.wait_sec,
            )

            episode_log_dir = os.path.join(args.logdir, f"test{test_idx}", f"ep{episode_idx}")
            plan_file = os.path.join(episode_log_dir, "final_plan.plan")

            final_plan = []
            try:
                with open(plan_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    parsed = re.findall(r"\((.*?)\)", content, flags=re.S)
                    if parsed:
                        final_plan = [f"({p.strip()})" for p in parsed]
            except FileNotFoundError:
                print(f"Warning: Plan file not found at {plan_file}")
            
            task_info = base_tasks_info[i]

            result = {
                "test": test_idx,
                "episode": episode_idx,
                "baseline": "self_correct",
                "scene": task_info["scene"],
                "selected_task": task_info["selected_task"],
                "final_plan": final_plan,
                "validate": validation_status
            }
            all_results.append(result)

    print("\nAll tests completed!")

    final_output_path = os.path.join(args.logdir, "test_out.json")
    with open(final_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()