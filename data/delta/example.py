from .target import generate_domain_query

EXHOUSEWORK = {
    "scene": ["home", "exhome"],
    "add_obj": None,
    "add_act": [
        "pick(<agent>, <item>, <room>): <agent> picks up an <item> at <room>. <item> must be accessible, located in <room>, the 'pick' action must be in the <item>'s affordance, and <agent> state must be 'hand-free'. As a result, <agent> state will change to 'holding', and the <item> is now held by the agent.",
        "place(<agent>, <item>, <surface>, <room>): <agent> places an <item> it is holding onto a <surface> in a <room>. The 'place' action must be in the <item>'s affordance, <agent> must be in <room> and holding the <item>. As a result, the <item> will be on the <surface>, and the <agent> state will change to 'hand-free'.",
        "turnon(<agent>, <item>, <room>): <agent> turns on an <item> at <room>. <item> must be accessible, the 'turnOn' action must be in the <item>'s affordance, both <agent> and <item> must be in <room>, <agent> must not be holding an item, and the <item> state must be 'off'. As a result, the <item> state will change to 'on'.",
        "turnoff(<agent>, <item>, <room>): <agent> turns off an <item> at <room>. <item> must be accessible, the 'turnOff' action must be in the <item>'s affordance, both <agent> and <item> must be in <room>, <agent> must not be holding an item, and the <item> state must be 'on'. As a result, the <item> state will change to 'off'.",
        "wait(<agent>): <agent> waits for a process to complete. This is often necessary after starting an appliance like a toaster or washing machine. As a result, the state of the item being processed changes (e.g., bread becomes 'toasted')."
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