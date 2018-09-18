from pyrts import Server
import json
from collections import defaultdict
from random import randint

class AI(Server):

    def __init__(self):
        super(AI, self).__init__()

    def evaluate(self, state):


    def get_unit_by_type(self, units, type):
        return [unit for unit in units if unit['type'] == type]



    def get_action(self, state):

        unit_types = self.get_unit_type_table()

        self._logger.debug(json.dumps(unit_types, indent=1, separators=(',', ': ')))

        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## I AM PLAYER 0
        units = unit_by_player[0]
        busy_units = self.get_busy_units(state)
        available_units = [unit for unit in units if unit['ID'] not in busy_units]
        available_workers = self.get_unit_by_type(available_units, "Worker")
        available_bases = self.get_unit_by_type(available_units, "Base")

        for worker in available_workers:
            # assign a random action

        for base in available_bases:
            # Assign a random action



        unit_action = {'type': 1, 'parameter': randint(1,4)}
        test_action = {'unitID': unit_id, 'unitAction': unit_action}

        return [test_action]


ai = AI()

if __name__ == "__main__":
    print("server is running")
    ai.start()