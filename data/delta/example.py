from .target import generate_domain_query

EXHOUSEWORK = {
    "scene": ["home", "exhome"],
    "add_obj": None,
    "add_act": [
        "pick_from_room(<agent>, <item>, <room>): The agent picks up an item from a general location in a room.",
        "pick_from_appliance(<agent>, <item>, <appliance>, <room>): The agent picks up an item from inside an appliance. The appliance must be turned off.",
        "place_in_appliance(<agent>, <item>, <appliance>, <room>): The agent places a held item into an appliance.",
        "place_on_surface(<agent>, <item>, <surface>, <room>): The agent places a held item onto a surface like a desk.",
        "turnon(<agent>, <appliance>, <room>): The agent turns on an appliance.",
        "turnoff(<agent>, <appliance>, <room>): The agent turns off an appliance.",
        "toast_bread(<agent>, <bread>, <toaster>, <room>): After turning the toaster on and waiting, the bread inside becomes toasted.",
        "boil_water(<agent>, <kettle>, <stove>, <room>): After turning the stove on and waiting, the water inside the kettle on the stove becomes boiled.",
        "cook_ramen(<agent>, <cup_ramen>, <water_dispenser>, <room>): After turning the dispenser on and waiting, the ramen becomes cooked."
    ],
    "gt_cost": { "home": 26, "exhome": 26 },
    "goal": "Make toast and place it on the desk in the living room, Boil water in the kettle and place it on the desk in the living room, Cook cup ramen using the water dispenser and place it on the desk in the living room.",
    "item_keep": [
        "bread", "toaster", "desk", "kettle", "stove", "cup_ramen", "water_dispenser"
    ],
    "subgoal": [
        "Toast the bread in the toaster", "Move the toasted bread to the living room desk",
        "Boil the water in the kettle", "Move the boiled kettle to the living room desk",
        "Cook cup ramen with the water dispenser", "Move the cooked cup ramen to the living room desk"
    ],
    "subgoal_pddl": [
        "(:goal (and (toasted bread) (item_on bread desk) (boiled kettle) (item_on kettle desk) (cooked cup_ramen) (item_on cup_ramen desk)))"
    ],
    "env_state": [
        "toasted(bread): bread is toasted.", "item_on(bread, desk): bread is on the desk.",
        "boiled(kettle): kettle contains boiled water.", "item_on(kettle, desk): kettle is on the desk.",
        "cooked(cup_ramen): cup ramen is cooked.", "item_on(cup_ramen, desk): cup ramen is on the desk."
    ]
}




selected_tasks = ["Heatedfood", "Placedwaterbottle", "Storedeggs"]
HOUSEWORK = generate_domain_query(selected_tasks)["HOUSEWORK"]

def get_example(domain: str, scene: str = None):
    return eval(domain.upper())


def get_scenes(domain: str):
    return eval(domain.upper())["scene"]