# cook toast, boil water, cook cupramen
EXHOUSEWORK = {
    "scene": ["home", "exhome"],
    "add_obj": None,
    "add_act": [
        "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
        "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
        "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
        "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
        "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
        "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
        "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
        "wait_cook_bread(<agent>, <bread>, <toaster>, <room>): After turning the toaster on and waiting, the bread inside becomes cooked.",
        "wait_boil_water(<agent>, <kettle>, <stove>, <room>): After turning the stove on and waiting, the water inside the kettle on the stove becomes boiled.",
        "wait_cook_ramen(<agent>, <cup_ramen>, <water_dispenser>, <room>): After turning the dispenser on and waiting, the ramen becomes cooked."
    ],
    "gt_cost": { "home": 26, "exhome": 26 },
    "goal": "Make cook(toast) bread and place it on the desk, Boil water in the kettle and place it on the desk , Cook cup ramen using the water dispenser and place it on the desk ",
    "item_keep": [
        "bread", "toaster", "desk", "kettle", "stove", "cup_ramen", "water_dispenser"
    ],
    "subgoal": [
        "Cook the bread in the toaster", "Move the cooked bread to the desk",
        "Boil the water in the kettle", "Move the boiled kettle to the desk",
        "Cook cup ramen with the water dispenser", "Move the cooked cup ramen to the desk"
    ],
        "subgoal_pddl": [
        """
    (:goal
        (cooked bread)
    )
""",
        """
    (:goal
        (item_on bread desk)
    )
""",
        """
    (:goal
        (boiled kettle)
    )
""",
        """
    (:goal
        (item_on kettle desk)
    )
""",
        """
    (:goal
        (cooked cup_ramen)
    )
""",
        """
    (:goal
        (item_on cup_ramen desk)
    )
"""
    ],
    "env_state": [
        "cooked(bread): bread is cooked.", "item_on(bread, desk): bread is on the desk.",
        "boiled(kettle): kettle contains boiled water.", "item_on(kettle, desk): kettle is on the desk.",
        "cooked(cup_ramen): cup ramen is cooked.", "item_on(cup_ramen, desk): cup ramen is on the desk."
    ]
}


def get_example(domain: str, scene: str = None):
    return eval(domain.upper())


def get_scenes(domain: str):
    return eval(domain.upper())["scene"]