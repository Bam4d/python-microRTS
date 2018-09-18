from pyrts import Server
import json
from collections import defaultdict
import random

class AI(Server):

    def __init__(self):
        super(AI, self).__init__()

    def evaluate(self, state):
        # Given the state, evaluate how how this is going..
        pass

    def get_unit_by_type(self, units, type):
        return [unit for unit in units if unit['type'] == type]


    def get_action(self, state):

        unit_type_table = self.get_unit_type_table()

        self._logger.debug(json.dumps(unit_type_table, indent=1, separators=(',', ': ')))

        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## I AM PLAYER 0

        actions = []
        units = unit_by_player[0]
        busy_units = self.get_busy_units(state)
        available_units = [unit for unit in units if unit['ID'] not in busy_units]
        available_workers = self.get_unit_by_type(available_units, "Worker")
        available_bases = self.get_unit_by_type(available_units, "Base")

        available_worker_actions = self.get_available_actions_by_type(unit_type_table, "Worker")
        for worker in available_workers:
            # Assign a random action
            actions.append({'unitID': worker['ID'], 'unitAction': random.choice(available_worker_actions)})

        available_base_actions = self.get_available_actions_by_type(unit_type_table, "Base")
        for base in available_bases:
            # Assign a random action
            actions.append({'unitID': base['ID'], 'unitAction': random.choice(available_base_actions)})

        return actions


ai = AI()

if __name__ == "__main__":
    print("server is running")
    ai.start()