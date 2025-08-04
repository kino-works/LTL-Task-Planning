import copy

HOME = {
    "name": "home",
    "rooms": {
        "kitchen": {
            "items": {
                "kitchen_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "toaster": {
                    "accessible": True,
                    "affordance": ["pick", "place", "turnOn", "turnOff"],
                    "state": "off"
                },
                "bread": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "kettle": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "induction": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "cup_ramen": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "water_dispenser": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "food": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "microwave": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "water_bottle": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_1": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_2": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_3": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "shelf": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "empty",
                    "content": {}
                },
                "eggs": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "egg_container": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "empty",
                    "content": {}
                }
            },
            "neighbor": []
        },
        "bathroom": {
            "items": {
                "bathroom_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "washing_machine": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                }
            },
            "neighbor": []
        },
        "bedroom": {
            "items": {
                "bedroom_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "clothes": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "dirty"
                },
                "phone": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "charger": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                }
            },
            "neighbor": []
        },
        "livingroom": {
            "items": {
                "livingroom_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "desk": {
                    "accessible": True,
                    "affordance": ["place", "wipe"],
                    "state": "dirty",
                    "content": []
                },
                "dishcloth": {
                    "accessible": True,
                    "affordance": ["pick", "place", "wipe"],
                    "state": "clean"
                }
            },
            "neighbor": []
        }
    },
    "agent": {
        "position": "livingroom",
        "state": "hand-free",
        "holding": None
    }
}

EXHOME = {
    "name": "exhome",
    "rooms": {
        "kitchen": {
            "items": {
                "kitchen_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "toaster": {
                    "accessible": True,
                    "affordance": ["pick", "place", "turnOn", "turnOff"],
                    "state": "off"
                },
                "bread": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "kettle": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "induction": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "cup_ramen": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "water_dispenser": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "food": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "microwave": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "water_bottle": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_1": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_2": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "dish_3": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "shelf": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "empty",
                    "content": {}
                },
                "eggs": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "free"
                },
                "egg_container": {
                    "accessible": True,
                    "affordance": ["pick", "place"],
                    "state": "empty",
                    "content": {}
                }
            },
            "neighbor": []
        },
        "livingroom": {
            "items": {
                "livingroom_lightswitch": {
                    "accessible": True,
                    "affordance": ["turnOn", "turnOff"],
                    "state": "off"
                },
                "desk": {
                    "accessible": True,
                    "affordance": ["place", "wipe"],
                    "state": "dirty",
                    "content": []
                },
                "dishcloth": {
                    "accessible": True,
                    "affordance": ["pick", "place", "wipe"],
                    "state": "clean"
                }
            },
            "neighbor": []
        }
    },
    "agent": {
        "position": "livingroom",
        "state": "hand-free",
        "holding": None
    }
}


def load_scene_graph(scene: str):
    return copy.deepcopy(eval(scene.upper()))


def extract_accessible_items_from_sg(sg: dict):
    accessible_items = []
    for room_name, room_data in sg["rooms"].items():
        if "assets" in room_data:
            assets = room_data.get("assets", {})
            for asset_name, asset_data in assets.items():
                if asset_data.get("accessible", True):
                    accessible_items_asset = []
                    items = asset_data.get("items", {})
                    for item_name, item_data in items.items():
                        if item_data.get("accessible", True):
                            accessible_items_asset.append(item_name)
                    accessible_items.append(
                        {"asset": asset_name, "items": accessible_items_asset})
        else:
            items = room_data.get("items", {})
            for item_name, item_data in items.items():
                if item_data.get("accessible", True):
                    accessible_items.append(item_name)
    return accessible_items


def prune_sg_with_item(sg: dict, item_keep: list):
    pruned_sg = copy.deepcopy(sg)
    for room_name, room_data in pruned_sg["rooms"].items():
        pruned_items = {}
        if "assets" in room_data and any("asset" in elem for elem in item_keep):
            pruned_assets = {}
            assets = room_data.get("assets", {})
            for asset_name, asset_data in assets.items():
                if any(asset_name in elem["asset"] for elem in item_keep):
                    pruned_assets[asset_name] = {}
                    asset_items = asset_data.get("items", {})
                    for item_name, item_data in asset_items.items():
                        if any(item_name in elem["items"] for elem in item_keep):
                            pruned_assets[asset_name][item_name] = item_data
                room_data["assets"] = pruned_assets
        else:
            room_items = room_data.get("items", {})
            for item_name, item_data in room_items.items():
                if item_name in item_keep:
                    pruned_items[item_name] = item_data
            room_data["items"] = pruned_items

    return pruned_sg


def count_rooms(sg: dict):
    return len(sg["rooms"])


def count_items(sg: dict):
    count = 0
    for room_name, room_data in sg["rooms"].items():
        if "assets" in room_data:
            assets = room_data.get("assets", {})
            for asset_name, asset_data in assets.items():
                items = asset_data.get("items", {})
                count += len(items)
        else:
            items = room_data.get("items", {})
            count += len(items)
    return count


def collapsed_sg(sg: dict):
    cg = {}
    cg["name"] = sg["name"]
    cg["rooms"] = {}
    cg["agent"] = sg["agent"]
    for room_name, room_data in sg["rooms"].items():
        cg["rooms"][room_name] = {"items": {},
                                  "neighbor": room_data["neighbor"]}
    return cg


def update_sg(sg: dict, orig_sg: dict, command: str, room: str):
    if command == "expand":
        assert sg["rooms"][room]["items"] == {}, "Room is not empty!"
        sg["rooms"][room]["items"] = orig_sg["rooms"][room]["items"]
    elif command == "contract":
        # assert sg["rooms"][room]["items"] != {}, "Room is empty!"
        sg["rooms"][room]["items"] = {}
    else:
        raise Exception("Invalid command!")
    return sg
