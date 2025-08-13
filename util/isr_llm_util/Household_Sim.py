import re
from collections import defaultdict

class HouseholdSim(object):
    def __init__(self):
        self.rooms = ['kitchen', 'bathroom', 'bedroom', 'livingroom']
        self.robot_room = None
        self.holding = None
        self.object_locations = {}
        self.container_defs = {
            'toaster': 1, 'induction': 1, 'microwave': 1, 'water_dispenser': 1,
            'washing_machine': 1, 'charger': 1, 'stove': 1,
            'desk': None, 'shelf': None, 'egg_container': None
        }
        self.container_contents = {c: [] for c in self.container_defs}
        devices = [
            'kitchen_lightswitch',
            'bathroom_lightswitch',
            'bedroom_lightswitch',
            'livingroom_lightswitch',
            'toaster',
            'induction',
            'microwave',
            'water_dispenser',
            'washing_machine',
            'charger',
            'stove'
        ]
        self.device_power = {d: False for d in devices}
        self.cleanliness = {'desk': False}
        self.time_elapsed = 0
        self.toasted = set()   
        self.boiled = set()   
        self.heated = set()   
        self.cooked = set()  
        self.charged = set()

    def initialize_state(self, initial_locations):
        self.robot_room = initial_locations.get('robot_room')
        self.holding = None
        for obj, loc in initial_locations.items():
            if obj == 'robot_room':
                continue
            if loc in self.container_defs:
                self.object_locations[obj] = loc
                self.container_contents[loc].append(obj)
            elif loc in self.rooms:
                self.object_locations[obj] = loc
            else:
                raise ValueError(f"Unknown location '{loc}' for object '{obj}'")
        self.time_elapsed = 0
        for d in self.device_power:
            self.device_power[d] = False
        for s in self.cleanliness:
            self.cleanliness[s] = False
        self.toasted.clear()
        self.boiled.clear()
        self.heated.clear()
        self.cooked.clear()
        self.charged.clear()

    def apply_action(self, action_str):
        tokens = action_str.strip("()").split()
        if not tokens:
            return False, "Empty action."
        head = tokens[0].lower()

        # 1) GOTO
        if head == 'goto':
            if len(tokens) != 4:
                return False, "Goto requires exactly one room parameter."
            room = tokens[1]
            if room not in self.rooms:
                return False, f"Unknown room '{room}'."
            self.robot_room = room
            return True, f"Moved to {room}."

        # 2) PICK
        if head == 'pick':
            if self.holding is None:
                return False, "Not holding any object."
            obj, container = self._extract_pick_place_args(tokens[1:])
            if obj is None:
                return False, "Place needs an identifiable object."
            if self.holding != obj:
                return False, f"Holding {self.holding}, not {obj}."
            if container:
                if container not in self.container_defs:
                    return False, f"Unknown container '{container}'."
                cont_loc = self.object_locations.get(container, self.robot_room)
                if cont_loc != self.robot_room:
                    return False, f"{container} not in current room {self.robot_room}."
                cap = self.container_defs[container]
                if cap is not None and len(self.container_contents[container]) >= cap:
                    return False, f"{container} is full."
                self.container_contents[container].append(obj)
                self.object_locations[obj] = container
            else:
                self.object_locations[obj] = self.robot_room
            self.holding = None
            return True, f"Placed {obj} to {container or self.robot_room}."

        # 3) PLACE
        if head == 'place':
            if self.holding is None:
                return False, "Not holding any object."
            obj, container = self._extract_pick_place_args(tokens[1:])
            if obj is None:
                return False, "Place needs an identifiable object."
            if self.holding != obj:
                return False, f"Holding {self.holding}, not {obj}."
            if container:
                if container not in self.container_defs:
                    return False, f"Unknown container '{container}'."
                cont_loc = self.object_locations.get(container, self.robot_room)
                if cont_loc != self.robot_room:
                    return False, f"{container} not in current room {self.robot_room}."
                cap = self.container_defs[container]
                if cap is not None and len(self.container_contents[container]) >= cap:
                    return False, f"{container} is full."
                self.container_contents[container].append(obj)
                self.object_locations[obj] = container
            else:
                self.object_locations[obj] = self.robot_room
            self.holding = None
            return True, f"Placed {obj} to {container or self.robot_room}."

        # 4) TURNON / TURNOFF
        if head in ('turn_on', 'turn_off', 'turn_on_switch', 'turn_off_switch'):
            device = self._pick_device_from_tokens(tokens[1:])
            if not device:
                return False, "TurnOn/TurnOff needs a valid device."
            if device not in self.device_power:
                return False, f"Unknown device '{device}'."

            dev_loc = self.object_locations.get(device, self.robot_room)
            if dev_loc != self.robot_room:
                return False, f"{device} not in current room {self.robot_room}."
            
            turn_on = head in ('turn_on', 'turnon', 'turn_on_switch')
            self.device_power[device] = turn_on
            return True, f"{'Turned on' if head=='turn_on' else 'Turned off'} {device}."

        # 5) WIPE
        if head == 'wipe':
            cloth = None
            surface = None
            for t in tokens[1:]:
                if cloth is None and t in self.object_locations and t != 'desk':
                    cloth = t
                if t == 'desk':
                    surface = 'desk'

            if cloth is None or surface is None:
                return False, "Wipe requires a cloth item and a 'desk' surface."
            if self.holding is not None:
                return False, "Need free hand to wipe."
            if self.object_locations.get(cloth) != self.robot_room:
                return False, f"{cloth} not in room {self.robot_room}."

            self.cleanliness['desk'] = True
            return True, f"Wiped desk with {cloth}."


        # 6) WAIT_*
        if head.startswith('wait_'):
            item = None
            appliance = None
            for t in tokens[1:]:
                if item is None and t in self.object_locations and t not in self.container_defs:
                    item = t
                if appliance is None and t in self.container_defs:
                    appliance = t

            if item is None or appliance is None:
                return False, "wait_* needs item and appliance."

            if self.object_locations.get(item) != appliance:
                return False, f"{item} not in appliance {appliance}."
            if not self.device_power.get(appliance, False):
                return False, f"{appliance} is not on."

            durations = {
                'wait_cook_bread': 3,
                'wait_cook_ramen': 3,
                'wait_boil_water': 5,
                'wait_heat_food': 3,
                'wait_heat_pot': 5,
                'wait_charge_phone': 10,
            }
            minutes = durations.get(head, 3)
            self.time_elapsed += minutes

            if head == 'wait_cook_bread':
                self.toasted.add(item)
                return True, f"Toasted {item}."
            if head == 'wait_cook_ramen':
                self.cooked.add(item)
                return True, f"Cooked {item}."
            if head == 'wait_boil_water':
                self.boiled.add(item)
                return True, f"Boiled {item}."
            if head in ('wait_heat_food', 'wait_heat_pot'):
                self.heated.add(item)
                return True, f"Heated {item}."
            if head == 'wait_charge_phone':
                self.charged.add(item)
                return True, f"Charged {item}."

            return False, f"Unknown wait action '{head}'."


        return False, f"Unknown action '{tokens[0]}'."

    def simulate_actions(self, actions, log_file=None):
        for i, act in enumerate(actions, 1):
            success, msg = self.apply_action(act)
            entry = f"Step {i}: {act} -> {msg}"
            if log_file:
                with open(log_file, 'a') as f:
                    f.write(entry + "\n")
            print(entry)
            if not success:
                print("The action sequence is wrong.")
                return False, True, msg, act 
        print("Simulation completed successfully.")
        print(f"Time elapsed: {self.time_elapsed} minutes.")
        return True, False, "", ""

    def generate_scene_description(self, input_data):
        rooms = defaultdict(list)
        robot_room = "unknown"
        devices_on, devices_off = [], []

        if isinstance(input_data, dict):
            pred_list = []
            for obj, loc in input_data.items():
                if obj == "robot_room":
                    pred_list.append(f"(at robot1 {loc})")
                else:
                    pred_list.append(f"(at {obj} {loc})")
        else:
            pred_list = input_data  # list[str]

        for p in pred_list:
            p = p.strip()
            m = re.findall(r"\((?:at|robot-at)\s+([^\s]+)\s+([^\s\)]+)\)", p)
            if m:
                obj, loc = m[0]
                if obj == "robot1":
                    robot_room = loc
                else:
                    rooms[loc].append(obj)
                continue

            if p.startswith("(on "):
                devices_on.append(p[4:-1].strip())
            elif p.startswith("(not (on "):
                devices_off.append(p[9:-2].strip())
            elif p.startswith("(off "):
                devices_off.append(p[5:-1].strip())

        lines = [f"The robot is in the {robot_room}."]
        for r, objs in rooms.items():
            if objs:
                lines.append(f"In the {r}: " + ", ".join(sorted(objs)) + ".")
        if devices_on:
            lines.append("Turned on: " + ", ".join(sorted(devices_on)) + ".")
        if devices_off:
            lines.append("Turned off: " + ", ".join(sorted(devices_off)) + ".")

        return "\\n".join(lines)
