import argparse
import datetime
import os
import random
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

ROOMS = ["kitchen", "bathroom", "bedroom", "livingroom"]

OBJECTS_BY_ROOM: Dict[str, List[str]] = {
    "kitchen": [
        "kitchen_lightswitch", "toaster", "bread", "kettle", "induction",
        "pot", "cup_ramen", "water_dispenser", "food", "microwave",
        "water_bottle", "shelf", "eggs", "egg_container", "stove",
        "dish_1", "dish_2", "dish_3"
    ],
    "bathroom": ["bathroom_lightswitch", "washing_machine"],
    "bedroom": ["bedroom_lightswitch", "clothes", "phone", "charger"],
    "livingroom": ["livingroom_lightswitch", "desk", "dishcloth"],
}

APPLIANCES = {
    "toaster", "microwave", "induction", "water_dispenser",
    "washing_machine", "charger", "stove",
    "kitchen_lightswitch", "bathroom_lightswitch",
    "bedroom_lightswitch", "livingroom_lightswitch"
}

def g_cooked_bread():
    return ["(cooked bread)", "(at bread desk)"]

def g_boiled_water():
    return ["(boiled kettle)", "(at kettle desk)"]

def g_heated_pot():
    return ["(heated pot)", "(at pot desk)"]

def g_washed_clothes():
    return ["(washed clothes)", "(at clothes bedroom)"]

def g_cooked_cup_ramen():
    return ["(cooked cup_ramen)", "(at cup_ramen desk)"]

def g_heated_food():
    return ["(heated food)", "(at food desk)"]

def g_charged_phone():
    return ["(charged phone)", "(at phone desk)"]

def g_placed_water_bottle():
    return ["(at water_bottle desk)"]

def g_wiped_desk():
    return ["(clean_desk desk)"]

def g_turn_on(room: str):
    return [f"(on {room}_lightswitch)"]

def g_turn_off(room: str):
    return [f"(not (on {room}_lightswitch))"]

def g_organized_dishes():
    return [
        "(at dish_1 shelf)",
        "(at dish_2 shelf)",
        "(at dish_3 shelf)",
    ]

def g_stored_eggs():
    return ["(at eggs egg_container)"]

GOAL_POOL_NO_PARAM = [
    g_cooked_bread,
    g_boiled_water,
    g_heated_pot,
    g_washed_clothes,
    g_cooked_cup_ramen,
    g_heated_food,
    g_charged_phone,
    g_placed_water_bottle,
    g_wiped_desk,
    g_organized_dishes,
    g_stored_eggs,
]

def random_initial_state() -> List[str]:
    """Generate predicates for base initial state."""
    preds: List[str] = []

    # robot
    robot_room = random.choice(ROOMS)
    preds.append(f"(at robot1 {robot_room})")

    # object locations
    for room, objs in OBJECTS_BY_ROOM.items():
        for obj in objs:
            preds.append(f"(at {obj} {room})")

    # appliances OFF  -> (not (on X))
    for a in APPLIANCES:
        preds.append(f"(not (on {a}))")

    return preds


def build_goal_predicates(max_goals: int) -> List[str]:
    """Pick 1~max_goals templates."""
    goals: List[str] = []

    pool = GOAL_POOL_NO_PARAM.copy()

    def switch_goal():
        room = random.choice(ROOMS)
        if random.random() < 0.5:
            return g_turn_on(room)
        else:
            return g_turn_off(room)

    for _ in range(4):
        pool.append(switch_goal)

    random.shuffle(pool)

    k = random.randint(1, max_goals)
    picked = 0
    for builder in pool:
        if picked >= k: break
        preds = builder() if builder in GOAL_POOL_NO_PARAM else builder()
        for p in preds:
            if p not in goals:
                goals.append(p)
        picked += 1

    return goals


def generate_case(max_goals: int) -> Tuple[List[str], List[str]]:
    init_state = random_initial_state()
    goal_state = build_goal_predicates(max_goals)
    return init_state, goal_state


def convert_predicates_to_dict(pred_list: List[str]) -> Dict[str, str]:
    result = {}
    for pred in pred_list:
        if pred.startswith("(at robot1 "):
            result['robot_room'] = pred.split()[2][:-1] 
        elif pred.startswith("(at "):
            parts = pred.split()
            obj = parts[1]
            loc = parts[2][:-1]
            result[obj] = loc
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--num_cases", type=int, default=200)
    ap.add_argument("--max_goals", type=int, default=2)
    ap.add_argument("--out_dir", type=str, default="../test_scenario/household")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max_attempts_mul", type=int, default=20,
                    help="max_attempts = num_cases * this")
    args = ap.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    os.makedirs(args.out_dir, exist_ok=True)

    init_list: List[List[str]] = []
    goal_list: List[List[str]] = []
    seen = set()

    max_attempts = args.num_cases * args.max_attempts_mul
    attempts = 0

    while len(init_list) < args.num_cases and attempts < max_attempts:
        attempts += 1
        i_state, g_state = generate_case(args.max_goals)
        key = ("|".join(sorted(i_state)), "|".join(sorted(g_state)))
        if key in seen:
            continue
        seen.add(key)
        init_list.append(i_state)
        goal_list.append(g_state)

    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    base = f"test_scenarios_household_{ts}"
    csv_path = os.path.join(args.out_dir, base + ".csv")
    npy_i = os.path.join(args.out_dir, base + "_initial_state.npy")
    npy_g = os.path.join(args.out_dir, base + "_goal_state.npy")

    # CSV
    df = pd.DataFrame({"initial_state": init_list, "goal_state": goal_list})
    df.to_csv(csv_path, index=False)

    init_dict_list = [convert_predicates_to_dict(preds) for preds in init_list]
    goal_dict_list = [convert_predicates_to_dict(preds) for preds in goal_list]

    np.save(npy_i, np.array(init_dict_list, dtype=object).reshape(-1, 1))
    np.save(npy_g, np.array(goal_dict_list, dtype=object).reshape(-1, 1))

    print(f"Generated {len(init_list)} cases.")
    print(f"Saved:\n  {csv_path}\n  {npy_i}\n  {npy_g}")


if __name__ == "__main__":
    main()
