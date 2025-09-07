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
from util.isr_llm_util.Planner import Planner
from util.isr_llm_util.Household_Sim import HouseholdSim

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

    setattr(args_test, "prompt_example_root", args_test.plan_prompt_dir)
    planner = Planner(args_test, is_log_example=True)

    with open(test_log_file_path, "w") as f:
        f.write(f"[Test {test_idx}, Episode {episode_idx}] Log for household (No Translator).\n")

    # 1) NL description
    description = simulator.generate_scene_description(initial_state, goal_state)
    planning_problem = description

    print(description)
    with open(test_log_file_path, "a") as f:
        f.write(f"Test case index: {test_idx}, Episode: {episode_idx}\n")
        f.write(description + "\n")

    # 2) Refinement loop
    final_actions = []
    is_satisfied = False
    is_error = True

    for j in range(max_num_refine + 1):
        time.sleep(wait_seconds)
        simulator.initialize_state(initial_state)

        with open(test_log_file_path, "a") as f:
            f.write(f"Attempt: {j}\n")

        temperature = 0 if test_idx == 1 else min(max_refine_temperature, 0.1 * (test_idx - 1))
        action_sequence = planner.query(planning_problem, is_append=(j > 0), temperature=temperature)

        print(f"Attempt {j} sequence:")
        with open(test_log_file_path, "a") as f:
            f.write(action_sequence + "\n")
            f.write("Analysis:\n")
        
        parsed = re.findall(r"\((.*?)\)", action_sequence, flags=re.S)
        if parsed:
            actions = [a.strip() for a in parsed]
        else:
            actions = [line.strip() for line in action_sequence.splitlines() if line.strip()]

        final_actions = [f"({a})" for a in actions]
        with open(final_plan_file_path, "w") as f:
            f.write("\n".join(final_actions))

        # 3) simulator validating
        is_satisfied, is_error, error_message, error_action = simulator.simulate_actions(actions, test_log_file_path)

        if is_error:
            if not is_satisfied:
                if error_action:
                    planning_problem = f"Action ({error_action}) is wrong. Error info: {error_message}. Please find a new plan."
                else:
                    planning_problem = f"{error_message} Please find a new plan."
            else:
                planning_problem = f"{error_message} Please ignore actions after action ({error_action})."
            
            with open(test_log_file_path, "a") as f:
                f.write(f"Feedback: {planning_problem}\n")
        else:
            print("Plan successful.")
            with open(test_log_file_path, "a") as f:
                f.write("Plan successful.\n")
            break
        # validating 종료

    planner.init_messages(is_reinitialize=True)

    with open(test_log_file_path, "a") as f:
        f.write(f"End of Test {test_idx}, Episode {episode_idx}\n\n\n")

    validation_status = "Success" if is_satisfied and not is_error else "Failure"
    return final_actions, validation_status


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--logdir", type=str, default=None)
    parser.add_argument('--domain', type=str, default="household")
    parser.add_argument("--num_plan_ex", type=int, default=3)
    parser.add_argument("--num_test", type=int, default=1)
    parser.add_argument("--max_refine", type=int, default=2)
    parser.add_argument("--max_temp", type=float, default=0.4)
    parser.add_argument("--wait_sec", type=float, default=30)
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--plan_prompt_dir",  default="data/cap")
    parser.add_argument("--test_input_file", type=str, default="baseline/test_input.json")
    parser.add_argument("--test_scenarios_file", type=str, default="data/isr_llm/test_scenarios.json")

    args = parser.parse_args()

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if args.logdir is None:
        args.logdir = os.path.join(project_root, "results", "cap")
    os.makedirs(args.logdir, exist_ok=True)

    simulator = HouseholdSim()

    base_initial_states, base_goal_states, base_tasks_info = load_scenarios(
        args.test_input_file, args.test_scenarios_file
    )
    num_base_tests = len(base_initial_states)

    for i in range(num_base_tests):
        for j in range(args.num_test):
            final_plan, validation_status = run_episode(
                initial_state=base_initial_states[i],
                goal_state=base_goal_states[i],
                test_idx=i + 1,
                episode_idx=j + 1,
                base_logdir=args.logdir,
                simulator=simulator,
                max_num_refine=args.max_refine,
                max_refine_temperature=args.max_temp,
                args_obj=args,
                wait_seconds=args.wait_sec,
            )
    
    print("\nAll tests completed!")

    all_results = []
    for i in range(num_base_tests):
        for j in range(args.num_test):
            task_info = base_tasks_info[i]
            result = {
                "test": i + 1,
                "episode": j + 1,
                "baseline": "cap",
                "scene": task_info["scene"],
                "selected_task": task_info["selected_task"],
                "final_plan": final_plan,
                "validate": validation_status
            }
            all_results.append(result)

    final_output_path = os.path.join(args.logdir, "test_out.json")

    with open(final_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()