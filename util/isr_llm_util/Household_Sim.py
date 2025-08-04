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
            'washing_machine': 1, 'charger': 1,
            'desk': None, 'shelf': None, 'egg_container': None
        }
        self.container_contents = {c: [] for c in self.container_defs}
        devices = [
            'kitchen_lightswitch', 'bathroom_lightswitch', 'bedroom_lightswitch', 'livingroom_lightswitch',
            'toaster', 'induction', 'microwave', 'water_dispenser', 'washing_machine', 'charger'
        ]
        self.device_power = {d: False for d in devices}
        self.cleanliness = {'desk': False}
        self.time_elapsed = 0

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

    def apply_action(self, action_str):
        tokens = action_str.strip("()").split()
        if not tokens:
            return False, "Empty action."
        head = tokens[0].lower()

        # 1) GOTO
        if head == 'goto':
            if len(tokens) != 2:
                return False, "Goto requires exactly one room parameter."
            room = tokens[1]
            if room not in self.rooms:
                return False, f"Unknown room '{room}'."
            self.robot_room = room
            return True, f"Moved to {room}."

        # 2) WAIT
        if head == 'wait':
            if len(tokens) != 2 or not tokens[1].isdigit():
                return False, "Wait requires exactly one numeric duration."
            minutes = int(tokens[1])
            self.time_elapsed += minutes
            return True, f"Waited {minutes} minutes."

        # 3) PICK
        if head == 'pick':
            if self.holding is not None:
                prev = self.holding
                self.object_locations[prev] = self.robot_room
                self.holding = None
            if len(tokens) == 2:
                obj, container = tokens[1], None
            elif len(tokens) == 3:
                obj, container = tokens[1], tokens[2]
            else:
                return False, "Pick takes one or two parameters."
            loc = self.object_locations.get(obj)
            if container:
                # container에 들어있는 obj 집기
                if container not in self.container_defs:
                    return False, f"Unknown container '{container}'."
                if loc != container:
                    return False, f"{obj} not in container {container}."
                self.container_contents[container].remove(obj)
            else:
                # 같은 방에 있는 obj만 집기
                if loc != self.robot_room:
                    return False, f"{obj} not in room {self.robot_room}."
            self.holding = obj
            self.object_locations[obj] = 'in_hand'
            return True, f"Picked up {obj}."

        # 4) PLACE
        if head == 'place':
            if self.holding is None:
                return False, "Not holding any object."
            if len(tokens) == 2:
                obj, container = tokens[1], None
            elif len(tokens) == 3:
                obj, container = tokens[1], tokens[2]
            else:
                return False, "Place takes one or two parameters."
            if self.holding != obj:
                return False, f"Holding {self.holding}, not {obj}."
            if container:
                if container not in self.container_defs:
                    return False, f"Unknown container '{container}'."
                # 컨테이너 위치 확인 (없으면 현재 방)
                cont_loc = self.object_locations.get(container, self.robot_room)
                if cont_loc != self.robot_room:
                    return False, f"{container} not in current room {self.robot_room}."
                cap = self.container_defs[container]
                if cap is not None and len(self.container_contents[container]) >= cap:
                    return False, f"{container} is full."
                self.container_contents[container].append(obj)
                self.object_locations[obj] = container
            else:
                # 바닥/기본 위치에 놓기
                self.object_locations[obj] = self.robot_room
            self.holding = None
            return True, f"Placed {obj} to {container or self.robot_room}."

        # 5) TURNON / TURNOFF
        if head in ('turnon', 'turnoff'):
            if len(tokens) != 2:
                return False, "TurnOn/TurnOff requires exactly one device parameter."
            device = tokens[1]
            if device not in self.device_power:
                return False, f"Unknown device '{device}'."
            # device 위치 확인
            dev_loc = self.object_locations.get(device, self.robot_room)
            if dev_loc != self.robot_room:
                return False, f"{device} not in current room {self.robot_room}."
            self.device_power[device] = (head == 'turnon')
            return True, f"{'Turned on' if head=='turnon' else 'Turned off'} {device}."

        # 6) WIPE
        if head == 'wipe':
            if len(tokens) != 3:
                return False, "Wipe requires exactly two parameters: cloth and surface."
            cloth, surface = tokens[1], tokens[2]
            if self.holding is not None:
                return False, "Need free hand to wipe."
            if cloth not in self.object_locations or \
               self.object_locations[cloth] != self.robot_room:
                return False, f"{cloth} not in room {self.robot_room}."
            if surface not in self.cleanliness:
                return False, f"Unknown surface '{surface}'."
            # 닦기
            self.cleanliness[surface] = True
            return True, f"Wiped {surface} with {cloth}."

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
        # … (기존 그대로 유지) …
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
