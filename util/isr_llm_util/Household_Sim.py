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
        #self.time_elapsed = 0
        self.cooked = set()   
        self.boiled = set()   
        self.heated = set()   
        self.charged = set()

    def initialize_state(self, initial_locations):
        self.robot_room = initial_locations.get('robot_room')
        self.holding = None

        self.object_locations.clear()
        self.container_contents = {c: [] for c in self.container_defs}

        for d in self.device_power:
            self.device_power[d] = False
        for s in self.cleanliness:
            self.cleanliness[s] = False
        self.cooked.clear()
        self.boiled.clear()
        self.heated.clear()
        self.charged.clear()

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
        #self.time_elapsed = 0

    def apply_action(self, action_str):
        tokens = action_str.strip("()").split()
        if not tokens:
            return False, "Empty action."
        head = tokens[0].lower()

        # 1) GOTO
        if head == 'goto':
            if len(tokens) != 4:
                return False, "Goto requires: (goto <agent> <from_room> <to_room>)."
            room = tokens[3]
            if room not in self.rooms:
                return False, f"Unknown room '{room}'."
            self.robot_room = room
            return True, f"Moved to {room}."

        # 2) PICK
        if head == 'pick':
            if self.holding is not None:
                return False, f"Already holding {self.holding}."
            
            if len(tokens) == 4:
                agent, obj, loc = tokens[1], tokens[2], tokens[3]
            else:
                return False, "Pick takes one or two parameters."

            if obj not in self.object_locations:
                return False, f"Unknown item '{obj}'."
            
            if loc in self.rooms:
                if self.robot_room != loc:
                    return False, f"Agent not at room {loc}."
                if self.object_locations.get(obj) != loc:
                    return False, f"{obj} not in room {loc}."
            elif loc in self.container_defs:
                cont_room = self.object_locations.get(loc)
                if cont_room != self.robot_room:
                    return False, f"{loc} not in current room {self.robot_room}."
                if self.object_locations.get(obj) != loc:
                    return False, f"{obj} not in {loc}."
                try:
                    self.container_contents[loc].remove(obj)
                except (KeyError, ValueError):
                    pass
            else:
                return False, f"Unknown location '{loc}'."
            self.holding = obj
            self.object_locations[obj] = 'in_hand'
            return True, f"Picked up {obj}."

        # 3) PLACE
        if head == 'place':
            if len(tokens) == 4:
                agent, obj, loc = tokens[1], tokens[2], tokens[3]
            else:
                return False, "Place takes one or two parameters."
            
            if self.holding is None:
                return False, "Not holding any object."
            if self.holding != obj:
                return False, f"Holding {self.holding}, not {obj}."

            for c, lst in self.container_contents.items():
                if obj in lst:
                    lst.remove(obj)

            #curr_loc = self.object_locations.get(obj)
            #if curr_loc == loc and self.holding is None:
            #    return False, f"{obj} already at {loc}."
            
            if loc in self.rooms:
                if self.robot_room != loc:
                    return False, f"Agent not at room {loc}."
                self.object_locations[obj] = loc
            
            elif loc in self.container_defs:
                cont_room = self.object_locations.get(loc)
                if cont_room != self.robot_room:
                    return False, f"{loc} not in current room {self.robot_room}."
                cap = self.container_defs[loc]
                if cap is not None and len(self.container_contents[loc]) >= cap:
                    return False, f"{loc} is full."
                if obj in self.container_contents.get(loc, []):
                    return False, f"{obj} already in {loc}."
                self.container_contents[loc].append(obj)
                self.object_locations[obj] = loc
            else:
                return False, f"Unknown location '{loc}'."
            self.holding = None
            return True, f"Placed {obj} to {loc}."

        # 4) TURNON / TURNOFF
        if head in ('turn_on', 'turn_off', 'turn_on_switch', 'turn_off_switch'):
            device = tokens[2]
            if not device:
                return False, "TurnOn/TurnOff needs a valid device."
            if device not in self.device_power:
                return False, f"Unknown device '{device}'."

            dev_loc = self.object_locations.get(device, self.robot_room)
            if dev_loc != self.robot_room:
                return False, f"{device} not in current room {self.robot_room}."
            
            turn_on = head in ('turn_on', 'turnon', 'turn_on_switch')
            self.device_power[device] = turn_on
            return True, f"{'Turned on' if turn_on else 'Turned off'} {device}."

        # 5) WIPE
        if head == 'wipe':
            if len(tokens) == 5:
                agent, item, room, desk_obj = tokens[1], tokens[2], tokens[3], tokens[4]
            else:
                return False, "Wipe requires: (wipe <agent> <item> <room> <desk>)."

            if self.robot_room != room:
                return False, f"Agent not at room {room}."
            
            if self.holding != item:
                if self.holding is None:
                    return False, "Need to be holding the wiping item."
                return False, f"Holding {self.holding}, not {item}."

            if 'cleanliness' not in self.__dict__:
                self.cleanliness = {}

            if desk_obj not in self.cleanliness:
                self.cleanliness[desk_obj] = False

            self.cleanliness[desk_obj] = True
            return True, f"Wiped {desk_obj} with {item}."


        # 6) WAIT_*
        if head.startswith('wait_'):
            if len(tokens) == 5:
                agent, item, appliance, room = tokens[1], tokens[2], tokens[3], tokens[4]
            else:
                return False, "Place takes one or two parameters."

            if self.robot_room != room:
                return False, f"Agent not at room {room}."

            ap_room = self.object_locations.get(appliance)
            if ap_room != room:
                return False, f"{appliance} not at room {room}."

            if self.object_locations.get(item) != appliance:
                return False, f"{item} not in appliance {appliance}."
            
            if not self.device_power.get(appliance, False):
                return False, f"{appliance} is not on."

            mapping = {
                'wait_cook_bread': ('cooked', self.cooked, "Cooked"),
                'wait_cook_ramen': ('cooked', self.cooked, "Cooked"),
                'wait_boil_water': ('boiled', self.boiled, "Boiled"),
                'wait_heat_food': ('heated', self.heated, "Heated"),
                'wait_heat_pot': ('heated', self.heated, "Heated"),
                'wait_charge_phone': ('charged', self.charged, "Charged"),
            }
            if head not in mapping:
                return False, f"Unknown wait action '{head}'."

            pred_name, pred_set, verb = mapping[head]

            if item in pred_set:
                return False, f"{item} already {pred_name}."

            pred_set.add(item)
            return True, f"{verb} {item}."

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
        #print(f"Time elapsed: {self.time_elapsed} minutes.")
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
            pred_list = input_data

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
