from data.delta.scene_graph import collapsed_sg, update_sg, EXHOME


def sayplan_output_format():
    return {
        "chain_of_thought": "break your problem down into a series of intermediate reasoning steps to help you determine your next command",
        "reasoning": "justify why the next action is important",
        "plan": "high-level task plan using only EXHOME domain actions"
    }


def sayplan_search_exp(goal: str):

    csg = collapsed_sg(EXHOME)
    output = f"""
    Instruction: {goal}
    3D scene graph (exhome): {csg}
    Memory: []
    Output: {{
        "mode": "search",
        "chain_of_thought": "The kitchen likely contains the toaster and bread needed to cook bread.",
        "reasoning": "I'll expand the kitchen.",
        "command": ("expand", "kitchen")
    }}
    3D scene graph: {update_sg(csg, EXHOME, "expand", "kitchen")}
    Memory: ["kitchen"]

    Output: {{
        "mode": "search",
        "chain_of_thought": "I see 'bread' and 'toaster' in the kitchen -> sufficient for cooking bread.",
        "reasoning": "No further rooms needed for cooking, but I need the livingroom for the final placement.",
        "command": ("expand", "livingroom")
    }}
    3D scene graph: {update_sg(csg, EXHOME, "expand", "livingroom")}
    Memory: ["kitchen", "livingroom"]

    Output: {{
        "mode": "search",
        "chain_of_thought": "Found all relevant items and destination -> switching to planning mode.",
        "reasoning": "Proceed to generate the cooking plan.",
        "command": "Switch to planning"
    }}
    """
    return output


def sayplan_plan_exp():
    plan_steps = [
        "(goto robot livingroom kitchen)",
        "(pick robot bread kitchen)",
        "(place robot bread toaster)",
        "(turnOn robot toaster)",
        "(wait robot)",
        "(turnOff robot toaster)",
        "(pick robot bread toaster)",
        "(goto robot kitchen livingroom)",
        "(place robot bread desk)"
    ]
    output = {
        "mode": "planning",
        "chain_of_thought": (
            "I have located the bread, toaster and destination desk -> "
            "will generate step-by-step actions to cook the bread and place it."
        ),
        "reasoning": "Each action is needed to move, operate device, and place the item.",
        "plan": """(goto robot livingroom kitchen)
            (pick robot bread kitchen)
            (place robot bread toaster)
            (turnOn robot toaster)
            (wait robot)
            (turnOff robot toaster)
            (pick robot bread toaster)
            (goto robot kitchen livingroom)
            (place robot bread desk)
        """
    }
    return output
