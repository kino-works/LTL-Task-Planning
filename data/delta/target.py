from typing import List, Dict, Any

TASK_DEFINITIONS: Dict[str, Dict] = {
    "Cookedtoast": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Make toast and place it on the desk in the living room.",
        "cost": {"home": 9, "exhome": 9},
        "item_keep": ["bread", "toaster", "desk"],
        "subgoal": [
            "Toast the bread in the toaster",
            "Move the toasted bread to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (toasted bread)))",
            "(:goal (and (item_at bread livingroom) (item_on bread desk)))"
        ],
        "env_state": [
            "item_is_bread(bread): bread is a food item.",
            "item_is_toaster(toaster): toaster is a kitchen appliance.",
            "toasted(bread): bread is toasted.",
            "item_on(bread, desk): bread is on the desk."
        ],
    },
    "Boiledwater": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Boil water in the kettle and place it on the desk in the living room.",
        "cost": {"home": 9, "exhome": 9},
        "item_keep": ["kettle", "stove", "desk"],
        "subgoal": [
            "Boil the water in the kettle",
            "Move the boiled kettle to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (boiled kettle)))",
            "(:goal (and (item_at kettle livingroom) (item_on kettle desk)))"
        ],
        "env_state": [
            "item_is_kettle(kettle): kettle is a container for boiling water.",
            "boiled(kettle): kettle contains boiled water.",
            "item_on(kettle, desk): kettle is on the desk."
        ],
    },
    "Heatedpot": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Heat the pot using the induction and place it on the desk in the living room.",
        "cost": {"home": 9, "exhome": 9},
        "item_keep": ["pot", "induction", "desk"],
        "subgoal": [
            "Heat the pot on the induction",
            "Move the heated pot to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (heated pot)))",
            "(:goal (and (item_at pot livingroom) (item_on pot desk)))"
        ],
        "env_state": [
            "item_is_pot(pot): pot is a container for cooking.",
            "heated(pot): pot is heated.",
            "item_on(pot, desk): pot is on the desk."
        ],
    },
    "Washedclothes": {
        "scene": ["home"],
        "add_obj": None,
        "add_act": None,
        "goal": "Wash the clothes in the washing machine and place them back in the bedroom.",
        "cost": {"home": 10},
        "item_keep": ["clothes", "washing_machine"],
        "subgoal": [
            "Wash the clothes using the washing machine",
            "Return the washed clothes to the bedroom"
        ],
        "subgoal_pddl": [
            "(:goal (and (cloth_clean clothes)))",
            "(:goal (and (cloth_clean clothes) (item_at clothes bedroom)))"
        ],
        "env_state": [
            "item_is_clothes(clothes): clothes to be washed.",
            "item_is_washing_machine(washing_machine): washing machine is a laundry appliance.",
            "cloth_clean(clothes): clothes are clean."
        ],
    },
    "Cookedcupramen": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Cook cup ramen using the water dispenser and place it on the desk in the living room.",
        "cost": {"home": 8, "exhome": 8},
        "item_keep": ["cup_ramen", "water_dispenser", "desk"],
        "subgoal": [
            "Cook cup ramen with the water dispenser",
            "Move the cooked cup ramen to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (cooked cup_ramen)))",
            "(:goal (and (item_at cup_ramen livingroom) (item_on cup_ramen desk)))"
        ],
        "env_state": [
            "item_is_cup_ramen(cup_ramen): cup ramen is a food item.",
            "cooked(cup_ramen): cup ramen is cooked.",
            "item_on(cup_ramen, desk): cup ramen is on the desk."
        ],
    },
    "Heatedfood": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Heat the food in the microwave and place it on the desk in the living room.",
        "cost": {"home": 9, "exhome": 9},
        "item_keep": ["food", "microwave", "desk"],
        "subgoal": [
            "Heat the food using the microwave",
            "Move the heated food to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (heated food)))",
            "(:goal (and (item_at food livingroom) (item_on food desk)))"
        ],
        "env_state": [
            "item_is_food(food): food item to be heated.",
            "item_is_microwave(microwave): microwave oven.",
            "heated(food): food is heated.",
            "item_on(food, desk): food is on the desk."
        ],
    },
    "Chargedphone": {
        "scene": ["home"],
        "add_obj": None,
        "add_act": None,
        "goal": "Charge the phone in the bedroom and place it on the desk in the living room.",
        "cost": {"home": 9},
        "item_keep": ["phone", "charger", "desk"],
        "subgoal": [
            "Charge the phone using the charger",
            "Move the charged phone to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (charged phone)))",
            "(:goal (and (item_at phone livingroom) (item_on phone desk)))"
        ],
        "env_state": [
            "item_is_phone(phone): mobile phone.",
            "item_is_charger(charger): charger device.",
            "charged(phone): phone is fully charged.",
            "item_on(phone, desk): phone is on the desk."
        ],
    },
    "Placedwaterbottle": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Place the water bottle from the kitchen onto the desk in the living room.",
        "cost": {"home": 4, "exhome": 4},
        "item_keep": ["water_bottle", "desk"],
        "subgoal": [
            "Pick up the water bottle",
            "Move the water bottle to the living room desk"
        ],
        "subgoal_pddl": [
            "(:goal (and (item_at water_bottle livingroom)))",
            "(:goal (and (item_on water_bottle desk)))"
        ],
        "env_state": [
            "item_is_water_bottle(water_bottle): water bottle.",
            "item_on(water_bottle, desk): water bottle is on the desk."
        ],
    },
    "Wipeddesk": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Wipe the desk in the living room using the dishcloth.",
        "cost": {"home": 3, "exhome": 3},
        "item_keep": ["dishcloth", "desk"],
        "subgoal": [
            "Pick the dishcloth",
            "Wipe the desk in the living room"
        ],
        "subgoal_pddl": [
            "(:goal (and (desk_clean livingroom)))"
        ],
        "env_state": [
            "item_is_dishcloth(dishcloth): cleaning cloth.",
            "desk_clean(livingroom): the desk is clean."
        ],
    },
    "Turnonswitch": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Turn on the light switch in the specified room.",
        "cost": {"home": 2, "exhome": 2},
        "item_keep": ["<room1>_lightswitch"],
        "subgoal": [
            "Go to the room",
            "Turn on the light switch"
        ],
        "subgoal_pddl": [
            "(:goal (and (at agent <room1>)))",
            "(:goal (and (on <room1>_lightswitch)))"
        ],
        "env_state": [
            "item_is_lightswitch(<room1>_lightswitch): light switch in the room.",
            "on(<room1>_lightswitch): the light switch is on."
        ],
    },
    "Turnoffswitch": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Turn off the light switch in the specified room.",
        "cost": {"home": 2, "exhome": 2},
        "item_keep": ["<room1>_lightswitch"],
        "subgoal": [
            "Go to the room",
            "Turn off the light switch"
        ],
        "subgoal_pddl": [
            "(:goal (and (at agent <room1>)))",
            "(:goal (and (not (on <room1>_lightswitch))))"
        ],
        "env_state": [
            "item_is_lightswitch(<room1>_lightswitch): light switch in the room.",
            "on(<room1>_lightswitch): the light switch is on."
        ],
    },
    "Organizeddishes": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Organize all the dishes by placing them onto the shelf in the kitchen.",
        "cost": {"home": 7, "exhome": 7},
        "item_keep": ["dish_1", "dish_2", "dish_3", "shelf"],
        "subgoal": [
            "Pick and place each dish on the shelf"
        ],
        "subgoal_pddl": [
            "(:goal (and (item_on dish_1 shelf) (item_on dish_2 shelf) (item_on dish_3 shelf)))"
        ],
        "env_state": [
            "item_is_dish(dish_1): dish for eating.",
            "item_is_dish(dish_2): dish for eating.",
            "item_is_dish(dish_3): dish for eating.",
            "item_is_shelf(shelf): storage shelf.",
            "item_on(dish_1, shelf): dish 1 is on the shelf."
        ],
    },
    "Storedeggs": {
        "scene": ["home", "exhome"],
        "add_obj": None,
        "add_act": None,
        "goal": "Store the eggs in the egg container in the kitchen.",
        "cost": {"home": 3, "exhome": 3},
        "item_keep": ["eggs", "egg_container"],
        "subgoal": [
            "Pick the eggs",
            "Place the eggs in the egg container"
        ],
        "subgoal_pddl": [
            "(:goal (and (picked eggs)))",
            "(:goal (and (in eggs egg_container)))"
        ],
        "env_state": [
            "item_is_eggs(eggs): eggs for storage.",
            "item_is_egg_container(egg_container): container for eggs.",
            "in(eggs, egg_container): eggs are in the egg container."
        ],
    }
}

def generate_domain_query(task_names: List[str]) -> Dict[str, Dict[str, Any]]:
    selected = [TASK_DEFINITIONS[name] for name in task_names]
    scenes: List[str] = []
    for t in selected:
        for s in t.get("scene", []):
            if s not in scenes:
                scenes.append(s)

    all_add_obj = [t["add_obj"] for t in selected if t.get("add_obj") is not None]
    add_obj = all_add_obj if all_add_obj else None

    all_add_act = [t["add_act"] for t in selected if t.get("add_act") is not None]
    add_act = all_add_act if all_add_act else None

    gt_cost: Dict[str, int] = {}
    for s in scenes:
        gt_cost[s] = sum(t.get("cost", {}).get(s, 0) for t in selected)

    goals = [t.get("goal", "") for t in selected]
    goal = ", ".join(goals)

    item_keep: List[str] = []
    for t in selected:
        for item in t.get("item_keep", []):
            if item not in item_keep:
                item_keep.append(item)

    subgoal: List[str] = []
    subgoal_pddl: List[str] = []
    env_state: List[str] = []
    for t in selected:
        subgoal.extend(t.get("subgoal", []))
        subgoal_pddl.extend(t.get("subgoal_pddl", []))
        env_state.extend(t.get("env_state", []))
    
    composite = {
        "scene": scenes,
        "add_obj": add_obj,
        "add_act": add_act,
        "gt_cost": gt_cost,
        "goal": goal,
        "item_keep": item_keep,
        "subgoal": subgoal,
        "subgoal_pddl": subgoal_pddl,
        "env_state": env_state,
    }

    return {"HOUSEWORK": composite}


def get_example(domain: str, scene: str = None):
    return {"home": HOME, "exhome": EXHOME}[domain]


def get_scenes(domain: str):
    return {"home": HOME["scene"], "exhome": EXHOME["scene"]}[domain]