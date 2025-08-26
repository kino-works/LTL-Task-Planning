import re
from typing import List, Dict, Any

TASK_DEFINITIONS: Dict[str, Dict] = {
    "Cookedtoast": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_cook_bread(<agent>, <bread>, <toaster>, <room>): After turning the toaster on and waiting, the bread inside becomes cooked."
        ],
        "goal": "Make cook(toast) bread and place it on the desk ", "cost": {"home": 9, "exhome": 9},
        "item_keep": ["bread", "toaster", "desk"],
        "subgoal": ["Cook the bread", "Move the bread to the desk"],
        "subgoal_pddl": ["(:goal (and (cooked bread)))", "(:goal (and (item_on bread desk)))"],
        "env_state": ["cooked(bread): bread is cooked.", "item_on(bread, desk): bread is on the desk."]
    },
    "Boiledwater": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_boil_water(<agent>, <kettle>, <stove>, <room>): After turning the stove on and waiting, the water inside the kettle on the stove becomes boiled."
        ],
        "goal": "Boil water in the kettle and place it on the desk ",
        "cost": {"home": 9, "exhome": 9},
        "item_keep": ["kettle", "stove", "desk"],
        "subgoal": ["Boil the water", "Move the kettle to the desk"],
        "subgoal_pddl": ["(:goal (and (boiled kettle)))", "(:goal (and (item_on kettle desk)))"],
        "env_state": ["boiled(kettle): kettle contains boiled water.", "item_on(kettle, desk): kettle is on the desk."]
    },
    "Heatedpot": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_heat_pot(<agent>, <pot>, <induction>, <room>): After turning the induction on and waiting, the pot on it becomes heated."
        ],
        "goal": "Heat the pot using the induction and place it on the desk ", "cost": {"home": 9, "exhome": 9},
        "item_keep": ["pot", "induction", "desk"],
        "subgoal": ["Heat the pot", "Move the pot to the desk"],
        "subgoal_pddl": ["(:goal (and (heated pot)))", "(:goal (and (item_on pot desk)))"],
        "env_state": ["heated(pot): pot is heated.", "item_on(pot, desk): pot is on the desk."]
    },
    "Washedclothes": {
        "scene": ["home"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_wash_clothes(<agent>, <clothes>, <washing_machine>, <room>): After turning the machine on and waiting, the clothes inside become clean."
        ],
        "goal": "Wash the clothes in the washing machine and place them back in the bedroom.", "cost": {"home": 10},
        "item_keep": ["clothes", "washing_machine"],
        "subgoal": ["Wash the clothes", "Return clothes to the bedroom"],
        "subgoal_pddl": ["(:goal (and (clean_cloth clothes)))"],
        "env_state": ["clean_cloth(clothes): clothes are clean."]
    },
    "Cookedcupramen": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_cook_ramen(<agent>, <cup_ramen>, <water_dispenser>, <room>): After turning the dispenser on and waiting, the ramen becomes cooked."
        ],
        "goal": "Cook cup ramen using the water dispenser and place it on the desk ", "cost": {"home": 8, "exhome": 8},
        "item_keep": ["cup_ramen", "water_dispenser", "desk"],
        "subgoal": ["Cook the cup ramen", "Move the ramen to the desk"],
        "subgoal_pddl": ["(:goal (and (cooked cup_ramen)))", "(:goal (and (item_on cup_ramen desk)))"],
        "env_state": ["cooked(cup_ramen): cup ramen is cooked.", "item_on(cup_ramen, desk): cup ramen is on the desk."]
    },
    "Heatedfood": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_heat_food(<agent>, <food>, <microwave>, <room>): After turning the microwave on and waiting, the food inside becomes heated."
        ],
        "goal": "Heat the food in the microwave and place it on the desk ", "cost": {"home": 9, "exhome": 9},
        "item_keep": ["food", "microwave", "desk"],
        "subgoal": ["Heat the food", "Move the food to the desk"],
        "subgoal_pddl": ["(:goal (and (heated food)))", "(:goal (and (item_on food desk)))"],
        "env_state": ["heated(food): food is heated.", "item_on(food, desk): food is on the desk."]
    },
    "Chargedphone": {
        "scene": ["home"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_appliance(<agent>, <item>, <appliance>, <room>): <agent> picks up an <item> that is inside an <appliance> in <room>. The <agent> must be in the same room, hand-free, and the appliance must be turned off. As a result, the <agent> will be holding the <item>, and it will be removed from the appliance.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
            "turn_on_appliance(<agent>, <appliance>, <room>): <agent> turns on an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an item, and the <appliance> state must be 'off'. As a result, the <appliance> state will change to 'on'.",
            "turn_off_appliance(<agent>, <appliance>, <room>): <agent> turns off an <appliance> at <room>. <appliance> must be accessible, the action must be in the <appliance>'s affordance, both <agent> and <appliance> must be in <room>, <agent> must not be holding an appliance, and the <appliance> state must be 'on'. As a result, the <appliance> state will change to 'off'.",
            "wait_charge_phone(<agent>, <phone>, <charger>, <room>): After turning the charger on and waiting, the phone becomes charged."
        ],
        "goal": "Charge the phone in the bedroom and place it on the desk ", "cost": {"home": 9},
        "item_keep": ["phone", "charger", "desk"],
        "subgoal": ["Charge the phone", "Move the phone to the desk"],
        "subgoal_pddl": ["(:goal (and (charged phone)))", "(:goal (and (item_on phone desk)))"],
        "env_state": ["charged(phone): phone is fully charged.", "item_on(phone, desk): phone is on the desk."]
    },
    "Placedwaterbottle": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_on_container(<agent>, <item>, <container>, <room>): <agent> places a held <item> onto a <container> in <room>. The <agent> must be holding the item and located in the same room as the container. As a result, the item will be placed on the container, and the agent's hand will become free.",
        ],
        "goal": "Place the water bottle from the kitchen onto the desk ", "cost": {"home": 4, "exhome": 4},
        "item_keep": ["water_bottle", "desk"],
        "subgoal": ["Pick up the water bottle", "Move it to the desk"],
        "subgoal_pddl": ["(:goal (and (item_on water_bottle desk)))"],
        "env_state": ["item_on(water_bottle, desk): water bottle is on the desk."]
    },
    "Wipeddesk": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "wipe(<agent>, <cloth>, <container>, <room>): The agent uses the held cloth to wipe a dirty container, making it clean."
        ],
        "goal": "Wipe the desk using the dishcloth.", "cost": {"home": 3, "exhome": 3},
        "item_keep": ["dishcloth", "desk"],
        "subgoal": ["Pick the dishcloth", "Wipe the desk"],
        "subgoal_pddl": ["(:goal (and (clean_desk desk)))"],
        "env_state": ["clean_desk(desk): the desk is clean."]
    },
    "Turnonswitch": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "turn_on_appliance(<agent>, <switch>, <room>): The agent turns on an item like a lightswitch."
        ],
        "goal": "Turn on the light switch in the specified room.", "cost": {"home": 2, "exhome": 2},
        "item_keep": ["<room>_lightswitch"],
        "subgoal": ["Go to the room", "Turn on the switch"],
        "subgoal_pddl": ["(:goal (and (appliance_on <room>_lightswitch)))"],
        "env_state": ["on(<room>_lightswitch): the light switch is on."]
    },
    "Turnoffswitch": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "turn_off_appliance(<agent>, <switch>, <room>): The agent turns off an item like a lightswitch."
        ],
        "goal": "Turn off the light switch in the specified room.", "cost": {"home": 2, "exhome": 2},
        "item_keep": ["<room>_lightswitch"], "subgoal": ["Go to the room", "Turn off the switch"],
        "subgoal_pddl": ["(:goal (and (not (appliance_on <room>_lightswitch))))"],
        "env_state": ["on(<room>_lightswitch): the light switch is on."]
    },
    "Organizeddishes": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
        ],
        "goal": "Organize all the dishes by placing them onto the shelf in the kitchen.", "cost": {"home": 7, "exhome": 7},
        "item_keep": ["dish_1", "dish_2", "dish_3", "shelf"],
        "subgoal": ["Place all dishes on the shelf"],
        "subgoal_pddl": ["(:goal (and (item_on dish_1 shelf) (item_on dish_2 shelf) (item_on dish_3 shelf)))"],
        "env_state": ["item_on(dish_1, shelf): dish 1 is on the shelf."]
    },
    "Storedeggs": {
        "scene": ["home", "exhome"], "add_obj": None,
        "add_act": [
            "goto(<agent>, <room_1>, <room_2>): <agent> goes from <room_1> to <room_2>, where <room_1> and <room_2> should be neighbors. As a result, <agent> will leave <room_1> and be located in <room_2>.",
            "pick_from_room(<agent>, <item>, <room>): <agent> picks up an <item> that is located in <room>. The <item> must be accessible and pickable, the <agent> must be hand-free and in the same room. As a result, the <agent> will be holding the <item>, and the <item> will no longer be in the room.",
            "pick_from_container(<agent>, <item>, <container>, <room>): <agent> picks up an <item> that is on <container> in <room>. The <agent> must be in the same room, hand-free. As a result, the <agent> will be holding the <item>, and it will be removed from the container.",
            "place_in_appliance(<agent>, <item>, <appliance>, <room>): <agent> places a held <item> into an <appliance> in <room>. The <agent> must be holding the item and located in the same room as the appliance. As a result, the item will be inside the appliance, and the agent's hand will become free.",
        ],
        "goal": "Place the eggs in the egg container in the kitchen.", "cost": {"home": 3, "exhome": 3},
        "item_keep": ["eggs", "egg_container"],
        "subgoal": ["Pick the eggs", "Place them in the container"],
        "subgoal_pddl": ["(:goal (and (item_in eggs egg_container)))"],
        "env_state": ["item_in(eggs, egg_container): eggs are in the egg container."]
    }
}


def generate_domain_query(task_names: List[str]) -> Dict[str, Dict[str, Any]]:
    selected = [TASK_DEFINITIONS[name] for name in task_names]

    scenes: List[str] = []
    for t in selected:
        for s in t.get("scene", []):
            if s not in scenes:
                scenes.append(s)

    all_add_obj_nested = [t["add_obj"] for t in selected if t.get("add_obj") is not None]
    all_add_obj_flat = [obj for sublist in all_add_obj_nested for obj in sublist]
    add_obj = list(dict.fromkeys(all_add_obj_flat)) if all_add_obj_flat else None

    all_add_act_flat: List[str] = []
    for t in selected:
        if t.get("add_act"):
            all_add_act_flat.extend(t["add_act"])
    add_act = list(dict.fromkeys(all_add_act_flat)) if all_add_act_flat else None

    gt_cost: Dict[str, int] = {s: sum(t.get("cost", {}).get(s, 0) for t in selected) for s in scenes}

    goals = [t.get("goal", "") for t in selected]
    goal = ", ".join(goals)

    item_keep: List[str] = []
    for t in selected:
        for item in t.get("item_keep", []):
            if item not in item_keep:
                item_keep.append(item)

    subgoal: List[str] = []
    raw_pddls: List[str] = []
    env_state: List[str] = []
    for t in selected:
        subgoal.extend(t.get("subgoal", []))
        raw_pddls.extend(t.get("subgoal_pddl", []))
        env_state.extend(t.get("env_state", []))

    formatted_pddls: List[str] = []
    for goal_str in raw_pddls:
        inner = goal_str[len(("(:goal (and ")) : -len("))")]
        conds = re.findall(r'\([^)]+\)', inner)
        block = "(:goal\n"
        for c in conds:
            block += f"    {c}\n"
        block += ")"
        formatted_pddls.append(block)

    composite = {
        "scene": scenes,
        "add_obj": add_obj,
        "add_act": add_act,
        "gt_cost": gt_cost,
        "goal": goal,
        "item_keep": item_keep,
        "subgoal": subgoal,
        "subgoal_pddl": formatted_pddls,
        "env_state": env_state,
    }

    return {"HOUSEWORK": composite}


def get_example(domain: str, scene: str = None):
    return eval(domain.upper())


def get_scenes(domain: str):
    return eval(domain.upper())["scene"]