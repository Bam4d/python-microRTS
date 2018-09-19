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


    def get_action(self, state, gameover):

        if gameover:
            return []

        unit_type_table = self.get_unit_type_table()

        #self._logger.debug(json.dumps(unit_type_table, indent=1, separators=(',', ': ')))

        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        #self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## I AM PLAYER 0
        actions = []
        units = unit_by_player[0]
        busy_units = self.get_busy_units(state)
        available_units = [unit for unit in units if unit['ID'] not in busy_units]
        available_workers = self.get_unit_by_type(available_units, 'Worker')
        available_bases = self.get_unit_by_type(available_units, 'Base')

        available_worker_actions = self.get_available_actions_by_type_name(unit_type_table, 'Worker')
        for worker in available_workers:
            # Assign a random action
            valid_actions = self.get_valid_actions_for_unit(worker, available_worker_actions, state)
            if len(valid_actions) > 0:
                actions.append({'unitID': worker['ID'], 'unitAction': random.choice(valid_actions)})

        available_base_actions = self.get_available_actions_by_type_name(unit_type_table, 'Base')
        for base in available_bases:
            # Assign a random action
            valid_actions = self.get_valid_actions_for_unit(base, available_base_actions, state)
            if len(valid_actions) > 0:
                actions.append({'unitID': base['ID'], 'unitAction': random.choice(valid_actions)})

        if len(actions):
            self._logger.info(json.dumps(actions))

        # For busy units we need to just send NONE action (-1)
        for unit_id in busy_units:
            actions.append({'unitID': unit_id, 'unitAction': {'type': -1}})

        return actions

ai = AI()

if __name__ == '__main__':
    print('server is running')
    ai.start()