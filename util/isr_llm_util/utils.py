from pathlib import Path
import os
import glob
import re
import numpy as np

# 모든 액션 헤드는 lowercase, 하이픈/언더바 제거 상태로 비교합니다.
HOUSEHOLD_VALID_ACTIONS = {
    "goto",
    "wait",
    "pick",
    "place",
    "turnon",
    "turnoff",
    "wipe"
}

def load_test_scenarios(args):
    """
    Look for *_initial_state.npy / *_goal_state.npy under:
      args.scenario_dir  (if given)
      else <project_root>/test_scenario
    """
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
    """
    PDDL에서 (:init ...) 블록과 (:goal (and ... )) 블록을
    정확히 depth를 세어 잘라 리턴합니다.
    """
    # ----- INIT 파싱 -----
    m_init = re.search(r"\(:init\s*(.*?)(?=\)\s*\(:goal)", 
                       pddl_problem, flags=re.S | re.I)
    if not m_init:
        m_init = re.search(r"\(:init\s*(.*)", pddl_problem, flags=re.S | re.I)
    if not m_init:
        raise ValueError("Could not find (:init ...) block in PDDL.")
    pddl_init_state = m_init.group(1).strip()

    # ----- GOAL 파싱 (depth 세기) -----
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
        # 닫는 괄호를 못 찾았으면 끝까지 긁고 하나 추가
        goal_block = pddl_problem[start:].strip() + ")"
    else:
        goal_block = pddl_problem[start:end_idx].strip()

    # ----- AND 내부만 떼기 -----
    m_and = re.match(
        r"\(:goal\s*\(\s*and\s*(.*)\)\s*\)$", 
        goal_block, flags=re.S | re.I
    )
    if m_and:
        inner = m_and.group(1).strip()
        # 안쪽 마지막에 ')' 누락 시 보충
        if not inner.endswith(")"):
            inner += ")"
        pddl_goal_state = inner
    else:
        # AND 블록이 아니면 전체 goal_block 반환
        pddl_goal_state = goal_block

    return pddl_init_state, pddl_goal_state


def extract_action_description(action_sequence: str, domain: str = "household"):
    """
    action_sequence: raw plan (one action per 라인)
    반환: validator에 넘길 “허용된” 액션만 줄 단위로 모아서 리턴
    """
    lines = []
    for ln in action_sequence.strip().splitlines():
        ln = ln.strip()
        # "(...)" 형태가 아니면 스킵
        if not (ln.startswith("(") and ln.endswith(")")):
            continue
        # 토큰화 후 헤드만 비교 (lower, 하이픈·언더바 제거)
        toks = ln[1:-1].split()
        head = toks[0].lower().replace("-", "").replace("_", "")
        if head in HOUSEHOLD_VALID_ACTIONS:
            lines.append(ln)
    # 한 줄씩 모아서, 마지막에 개행 추가
    return "\n".join(lines) + ("\n" if lines else "")
