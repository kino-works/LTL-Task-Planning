from .target import generate_domain_query

EXHOUSEWORK = {
    "scene": ["home", "exhome"],
    "add_obj": None,
    "add_act": [,
        "toast_bread(<agent>, <bread>, <toaster>, <room>): To toast bread, the agent must be in the same room as the bread and the toaster. The bread must be inside the toaster, and the toaster must be turned on. After waiting, the bread becomes toasted.",
        "boil_water(<agent>, <kettle>, <stove>, <room>): To boil water, the kettle must be on the stove, and the stove must be turned on. The agent must be in the same room. After waiting, the water in the kettle becomes boiled.",
        "cook_ramen(<agent>, <cup_ramen>, <water_dispenser>, <room>): To cook cup ramen, the ramen must be placed at the water dispenser, and the dispenser must be turned on to pour hot water. After waiting, the cup ramen becomes cooked."
    ],
    "gt_cost": {
        "home": 26,
        "exhome": 26
    },
    "goal": "Make toast and place it on the desk in the living room, Boil water in the kettle and place it on the desk in the living room, Cook cup ramen using the water dispenser and place it on the desk in the living room.",
    "item_keep": [
        "bread",
        "toaster",
        "desk",
        "kettle",
        "stove",
        "cup_ramen",
        "water_dispenser"
    ],
    "subgoal": [
        "Toast the bread in the toaster",
        "Move the toasted bread to the living room desk",
        "Boil the water in the kettle",
        "Move the boiled kettle to the living room desk",
        "Cook cup ramen with the water dispenser",
        "Move the cooked cup ramen to the living room desk"
    ],
    "subgoal_pddl": [
        "(:goal (and (toasted bread)))",
        "(:goal (and (item_at bread livingroom) (item_on bread desk)))",
        "(:goal (and (boiled kettle)))",
        "(:goal (and (item_at kettle livingroom) (item_on kettle desk)))",
        "(:goal (and (cooked cup_ramen)))",
        "(:goal (and (item_at cup_ramen livingroom) (item_on cup_ramen desk)))"

    ],
    "env_state": [
        "item_is_bread(bread): bread is a food item.",
        "item_is_toaster(toaster): toaster is a kitchen appliance.",
        "toasted(bread): bread is toasted.",
        "item_on(bread, desk): bread is on the desk.",
        "item_is_kettle(kettle): kettle is a container for boiling water.",
        "boiled(kettle): kettle contains boiled water.",
        "item_on(kettle, desk): kettle is on the desk.",
        "item_is_cup_ramen(cup_ramen): cup ramen is a food item.",
        "cooked(cup_ramen): cup ramen is cooked.",
        "item_on(cup_ramen, desk): cup ramen is on the desk."
    ]
}

selected_tasks = ["Heatedfood", "Placedwaterbottle", "Storedeggs"]
HOUSEWORK = generate_domain_query(selected_tasks)["HOUSEWORK"]

def get_example(domain: str, scene: str = None):
    return eval(domain.upper())


def get_scenes(domain: str):
    return eval(domain.upper())["scene"]