import os
import sys
import time
import datetime
import argparse
import openai
import re
import copy 

# Project paths (adjust if needed)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "util"))
sys.path.append(os.path.join(project_root, "baseline"))

from dotenv import load_dotenv

# util imports (edit to your actual module names)
from util.isr_llm_util.Planner import Planner
from util.isr_llm_util.Household_Sim import HouseholdSim
from util.isr_llm_util.utils import load_test_scenarios


def run_cap(
    simulator: HouseholdSim,
    planner: Planner,
    test_initial_state,
    test_goal_state,
    num_test: int,
    max_num_refine: int,
    max_refine_temperature: float,
    num_prompt_examples_dataset: int,
    base_logdir: str, 
    args_obj,  
    wait_seconds: float,
):

    allowed_verbs = {"goto", "pick", "place", "turn_on", "turn_off", 'turn_on_switch', 'turn_off_switch', "wipe",
                    "wait_cook_bread", "wait_cook_ramen", "wait_boil_water", "wait_heat_food", "wait_heat_pot", "wait_charge_phone"}

    for i in range(num_test):
        time.sleep(wait_seconds)

        test_dir = os.path.join(base_logdir, f"test{i}")
        os.makedirs(test_dir, exist_ok=True) 

        test_log_file_path = os.path.join(test_dir, "test_log.txt")     
        final_plan_file_path = os.path.join(test_dir, "final_plan.plan")

        args_test = copy.copy(args_obj)    
        args_test.logdir = test_dir                   

        setattr(args_test, "prompt_example_root", args_test.plan_prompt_dir)   
        planner = Planner(args_test, is_log_example=True)                                    

        with open(test_log_file_path, "w") as f:                               
            f.write(f"[Test {i}] Test log for household (self-feedback).\n")   

        idx = i + num_prompt_examples_dataset
        initial_state = test_initial_state[idx, 0]
        goal_state = test_goal_state[idx, 0]

        # 1) NL scene description
        description = simulator.generate_scene_description(initial_state)
        planning_problem = description

        print(description.replace("\\n", "\n"))

        with open(test_log_file_path, "a") as f:
            f.write(f"Test case index: {idx}\n")
            f.write(description + "\n")

        # 2) Refinement loop
        for j in range(max_num_refine + 1):
            time.sleep(wait_seconds)
            simulator.initialize_state(initial_state)

            with open(test_log_file_path, "a") as f:
                f.write(f"Attempt: {j}\n")

            # Planner query
            temperature = 0.0 if i == 0 else min(max_refine_temperature, 0.1 * i)
            resp = planner.query(planning_problem, is_append=(j > 0), temperature=temperature)
            if isinstance(resp, str):
                action_sequence = resp
            else:
                action_sequence = resp.get("choices")[0]["message"]["content"]

            print(f"Attempt {j} sequence:")
            #print(action_sequence)
            with open(test_log_file_path, "a") as f:
                f.write(action_sequence + "\n")
                f.write("Analysis:\n")

            parsed = re.findall(r"\((.*?)\)", action_sequence, flags=re.S)
            if parsed:
                actions = [a.strip() for a in parsed]
            else:
                actions = [line.strip() for line in action_sequence.splitlines() if line.strip()]
            actions = [a for a in actions if a.split()[0] in allowed_verbs]
            
            formatted_plan = "\n".join(f"({a})" for a in actions) + "\n"
            with open(final_plan_file_path, "w") as f:
                f.write(formatted_plan)
            
            # 3) Execute & feedback
            is_satisfied, is_error, error_message, error_action = simulator.simulate_actions(actions, test_log_file_path)

            if is_error:
                if not is_satisfied:
                    if error_action:
                        planning_problem = (
                            f"Action {error_action} is wrong. Error info: {error_message}. "
                            + "Please find a new plan."
                        )
                    else:
                        planning_problem = f"{error_message} Please find a new plan."
                else:
                    planning_problem = (
                        f"{error_message} Please ignore actions after {error_action}."
                    )
                with open(test_log_file_path, "a") as f:
                    f.write(planning_problem + "\n")
            elif is_error is None:
                planning_problem = "Please find a new plan."
                with open(test_log_file_path, "a") as f:
                    f.write(planning_problem + "\n")
            else:
                # no error: success
                break
        
        planner.init_messages(is_reinitialize=True)

        with open(test_log_file_path, "a") as f:
            f.write(f"End of test case {idx}\n\n")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--logdir", type=str, default=None)
    parser.add_argument('--domain', type=str, default="household")
    parser.add_argument("--num_plan_ex", type=int, default=3)
    parser.add_argument("--num_test", type=int, default=2)
    parser.add_argument("--max_refine", type=int, default=10)
    parser.add_argument("--max_temp", type=float, default=0.4)
    parser.add_argument("--wait_sec", type=float, default=30)
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--plan_prompt_dir",  default="data/cap")

    args = parser.parse_args()

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Log dir
    if args.logdir is None:
        args.logdir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "results",
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
        )
    os.makedirs(args.logdir, exist_ok=True)

    simulator = HouseholdSim()

    # Load scenarios
    test_initial_state, test_goal_state = load_test_scenarios(args)

    # Compute how many front examples to skip in dataset
    num_prompt_examples_dataset = args.num_plan_ex

    # Run
    run_cap(
        simulator=simulator,
        planner=None,
        test_initial_state=test_initial_state,
        test_goal_state=test_goal_state,
        num_test=args.num_test,
        max_num_refine=args.max_refine,
        max_refine_temperature=args.max_temp,
        num_prompt_examples_dataset=num_prompt_examples_dataset,
        base_logdir=args.logdir, 
        args_obj=args,  
        wait_seconds=args.wait_sec,
    )


if __name__ == "__main__":
    main()