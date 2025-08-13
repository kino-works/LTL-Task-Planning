from pathlib import Path
import os
import glob
import re
import numpy as np

HOUSEHOLD_VALID_ACTIONS = {
    "goto",
    "pick",
    "place",
    "turn_on",
    "turn_off",
    "wait_cook_bread",
    "wait_boil_water",
    "wait_cook_ramen",
    "wait_heat_food",
    "wait_charge_phone",
    "wait_heat_pot",
    "turn_on_switch",
    "turn_off_switch",
    "wipe",
}

def load_test_scenarios(args):
    project_root = Path(__file__).resolve().parents[2]
    test_file_root = Path(
        getattr(args, "scenario_dir", project_root / "test_scenario")
    ).resolve()

    def pick_latest(pattern: str) -> str:
        files = glob.glob(str(test_file_root / pattern))
        if not files:
            raise FileNotFoundError(f"No files matching {pattern} in {test_file_root}")
        return max(files, key=os.path.getmtime)

    init_path = getattr(args, "initial_file", None) or pick_latest("*_initial_state.npy")
    goal_path = getattr(args, "goal_file",   None) or pick_latest("*_goal_state.npy")

    print(f"Loading household scenarios:\n  init: {init_path}\n  goal: {goal_path}")

    initial_state = np.load(init_path, allow_pickle=True)
    goal_state    = np.load(goal_path,  allow_pickle=True)
    return initial_state, goal_state


def extract_state_pddl(pddl_problem: str, domain: str = "household"):
    m_init = re.search(r"\(:init\s*(.*?)(?=\)\s*\(:goal)", 
                       pddl_problem, flags=re.S | re.I)
    if not m_init:
        m_init = re.search(r"\(:init\s*(.*)", pddl_problem, flags=re.S | re.I)
    if not m_init:
        raise ValueError("Could not find (:init ...) block in PDDL.")
    pddl_init_state = m_init.group(1).strip()

    start = pddl_problem.find("(:goal")
    if start == -1:
        raise ValueError("Could not find (:goal ...) block in PDDL.")
    depth = 0
    end_idx = None
    for idx, ch in enumerate(pddl_problem[start:], start=start):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if depth == 0:
            end_idx = idx + 1
            break

    if end_idx is None:
        goal_block = pddl_problem[start:].strip() + ")"
    else:
        goal_block = pddl_problem[start:end_idx].strip()

    m_and = re.match(
        r"\(:goal\s*\(\s*and\s*(.*)\)\s*\)$", 
        goal_block, flags=re.S | re.I
    )
    if m_and:
        inner = m_and.group(1).strip()
        if not inner.endswith(")"):
            inner += ")"
        pddl_goal_state = inner
    else:
        pddl_goal_state = goal_block

    return pddl_init_state, pddl_goal_state


def extract_action_description(action_sequence: str, domain: str = "household"):
    lines = []
    for ln in action_sequence.strip().splitlines():
        ln = ln.strip()
        if not (ln.startswith("(") and ln.endswith(")")):
            continue
        toks = ln[1:-1].split()
        head = toks[0].lower().replace("-", "").replace("_", "")
        if head in HOUSEHOLD_VALID_ACTIONS:
            lines.append(ln)
    return "\n".join(lines) + ("\n" if lines else "")
