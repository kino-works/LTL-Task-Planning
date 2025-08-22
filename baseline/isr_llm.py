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
from util.isr_llm_util.Translator import Translator
from util.isr_llm_util.Planner import Planner
from util.isr_llm_util.Validator import Validator
from util.isr_llm_util.Household_Sim import HouseholdSim
from util.isr_llm_util.utils import (
    load_test_scenarios,
    extract_state_pddl,
    extract_action_description,
)


def run_isr_llm(
    simulator: HouseholdSim,
    translator: Translator,
    planner: Planner,
    validator: Validator,
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

    for i in range(num_test):
        time.sleep(wait_seconds)

        test_dir = os.path.join(base_logdir, f"test{i}")
        os.makedirs(test_dir, exist_ok=True) 

        test_log_file_path = os.path.join(test_dir, "test_log.txt")     
        final_plan_file_path = os.path.join(test_dir, "final_plan.plan")

        args_test = copy.copy(args_obj)    
        args_test.logdir = test_dir      

        setattr(args_test, "prompt_example_root", args_test.trans_prompt_dir)  
        translator = Translator(args_test, is_log_example=True)                

        setattr(args_test, "prompt_example_root", args_test.plan_prompt_dir)   
        planner = Planner(args_test, is_log_example=True)                     

        setattr(args_test, "prompt_example_root", args_test.valid_prompt_dir)  
        validator = Validator(args_test, is_log_example=True)                 

        with open(test_log_file_path, "w") as f:                               
            f.write(f"[Test {i}] Test log for household (self-feedback).\n")   

        idx = i + num_prompt_examples_dataset
        initial_state = test_initial_state[idx, 0]
        goal_state = test_goal_state[idx, 0]

        # 1) NL description
        description = simulator.generate_scene_description(initial_state)
        print(idx, description)
        with open(test_log_file_path, "a") as f:
            f.write(f"Test case index: {idx}\n")
            f.write(description + "\n")

        # 2) Translator → planning problem
        resp_txt = translator.query(description, is_append=False)
        planning_problem = resp_txt
        
        # Extract init/goal for validator prompt
        pddl_init_state, pddl_goal_state = extract_state_pddl(planning_problem, domain="household")

        # 3) Refinement loop
        for j in range(max_num_refine + 1):
            time.sleep(wait_seconds)

            simulator.initialize_state(initial_state)

            with open(test_log_file_path, "a") as f:
                f.write(f"Attempt: {j}\n")

            temperature = 0 if i == 0 else min(max_refine_temperature, 0.1 * i)
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
            final_answer = parts[1]

            if 'Yes' in final_answer:
                print("Self-evaluation suggests a solution.")
                with open(test_log_file_path, "a") as f:
                    f.write("Self-evaluation suggests a solution.\n")
                break
            elif 'No' in final_answer:
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

        simulator.simulate_actions(actions, test_log_file_path)
        
        planner.init_messages(is_reinitialize=True)

        with open(test_log_file_path, "a") as f:
            f.write(f"End of test case {idx}\n\n\n")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--logdir", type=str, default=None)
    parser.add_argument('--domain', type=str, default="household")
    parser.add_argument("--num_trans_ex", type=int, default=3)
    parser.add_argument("--num_plan_ex", type=int, default=3)
    parser.add_argument("--num_valid_ex", type=int, default=3)
    parser.add_argument("--num_test", type=int, default=2)
    parser.add_argument("--max_refine", type=int, default=10)
    parser.add_argument("--max_temp", type=float, default=0.4)
    parser.add_argument("--wait_sec", type=float, default=30)
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--trans_prompt_dir", default="data/isr_llm/trans")
    parser.add_argument("--plan_prompt_dir",  default="data/isr_llm/plan")
    parser.add_argument("--valid_prompt_dir", default="data/isr_llm/valid")

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
    num_prompt_examples_dataset = max(args.num_trans_ex, args.num_plan_ex, args.num_valid_ex)

    # Run
    run_isr_llm(
        simulator=simulator,
        translator=None,
        planner=None,
        validator=None,
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