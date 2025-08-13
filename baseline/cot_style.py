#!/usr/bin/env python3
import os
import sys
import time
import datetime
import argparse
import openai
from dotenv import load_dotenv
import re

# Project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "util"))
sys.path.append(os.path.join(project_root, "baseline"))

from util.isr_llm_util.Planner import Planner
from util.isr_llm_util.Household_Sim import HouseholdSim
from util.isr_llm_util.utils import load_test_scenarios


def test_no_trans_household(
    simulator: HouseholdSim,
    planner: Planner,
    test_initial_state,
    test_goal_state,
    num_test: int,
    max_num_refine: int,
    max_refine_temperature: float,
    num_prompt_examples_dataset: int,
    test_log_file_path: str,
    wait_seconds: float,
):
    """
    Run LLM-only CoT loop on household domain without translator or validator.
    Parses planner output to extract valid actions before simulation.
    """
    # Define allowed action verbs for filtering
    allowed_verbs = {"goto", "pick", "place", "turnOn", "turnOff", "wait", "wipe"}

    for i in range(num_test):
        time.sleep(wait_seconds)
        idx = i + num_prompt_examples_dataset
        initial_state = test_initial_state[idx, 0]
        goal_state = test_goal_state[idx, 0]

        # 1) NL scene description
        description = simulator.generate_scene_description(initial_state)
        planning_problem = description

        print(f"Description:")
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

            # Parse and filter actions before simulation
            parsed = re.findall(r"\((.*?)\)", action_sequence, flags=re.S)
            if parsed:
                actions = [a.strip() for a in parsed]
            else:
                actions = [line.strip() for line in action_sequence.splitlines() if line.strip()]
            # Keep only valid action verbs
            actions = [a for a in actions if a.split()[0] in allowed_verbs]

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

        # reset planner for next case
        planner.init_messages(is_reinitialize=True)
        with open(test_log_file_path, "a") as f:
            f.write(f"End of test case {idx}\n\n")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--logdir", type=str, default=None, help="Directory to save run logs")
    parser.add_argument("--num_plan_ex", type=int, default=3, help="Prompt examples for planner")
    parser.add_argument("--num_test", type=int, default=2, help="Number of test scenarios to run")
    parser.add_argument("--max_refine", type=int, default=2, help="Maximum refinement attempts")
    parser.add_argument("--max_temp", type=float, default=0.4, help="Max planning temperature")
    parser.add_argument("--wait_sec", type=float, default=30, help="Wait seconds between API calls")
    parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model")
    parser.add_argument(
        "--plan_prompt_dir", type=str, default="data/cot_style", help="Planner prompt dir"
    )
    parser.add_argument("--domain", type=str, default="household", help="Task domain (only 'household' supported)")
    args = parser.parse_args()

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # setup logdir
    if args.logdir is None:
        args.logdir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "run_log",
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
        )
    os.makedirs(args.logdir, exist_ok=True)

    # init components
    setattr(args, "prompt_example_root", args.plan_prompt_dir)
    planner = Planner(args, is_log_example=True)
    simulator = HouseholdSim()

    # load scenarios
    test_initial_state, test_goal_state = load_test_scenarios(args)
    num_prompt_ex = args.num_plan_ex

    log_path = os.path.join(args.logdir, "test_log.txt")
    with open(log_path, "w") as f:
        f.write("Test log for household domain (no-trans CoT).\n\n")

    # run
    test_no_trans_household(
        simulator=simulator,
        planner=planner,
        test_initial_state=test_initial_state,
        test_goal_state=test_goal_state,
        num_test=args.num_test,
        max_num_refine=args.max_refine,
        max_refine_temperature=args.max_temp,
        num_prompt_examples_dataset=num_prompt_ex,
        test_log_file_path=log_path,
        wait_seconds=args.wait_sec,
    )


if __name__ == "__main__":
    main()