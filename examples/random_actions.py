import json
import random
from collections import defaultdict

import pyrts
from pyrts import Server


class AI(Server):
    """
    Randomly selects actions for each unit
    """

    def __init__(self, player_id):
        super(AI, self).__init__(player_id)

    def get_unit_by_type(self, units, unit_type):
        return [unit for unit in units if unit['type'] == unit_type]

    def get_action(self, state, gameover):
        unit_type_table = self.get_unit_type_table()

        #self._logger.debug(json.dumps(unit_type_table, indent=1, separators=(',', ': ')))

        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        #self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## I AM PLAYER 0
        actions = []
        units = unit_by_player[self.player_id]

        # Gets all the units that are currently busy performing an action
        busy_units = self.get_busy_units(state)

        # Get all the units that we control
        available_units = [unit for unit in units if unit['ID'] not in busy_units]

        # Get all the workers that we control and are not busy
        available_workers = self.get_unit_by_type(available_units, 'Worker')

        # Get all the bases that we can control and are not busy
        available_bases = self.get_unit_by_type(available_units, 'Base')

        # Get positions within the state that are valid or invalid for each action type
        valid_action_positions_for_state = self.get_valid_action_positions_for_state(state)

        # Get all the actions that are available for a worker
        available_worker_actions = self.get_available_actions_by_type_name(unit_type_table, 'Worker')
        for worker in available_workers:
            # Get the valid actions for a particular worker
            valid_actions = self.get_valid_actions_for_unit(worker, available_worker_actions, valid_action_positions_for_state)

            # If we have some valid actions, choose a random one
            if len(valid_actions) > 0:
                actions.append({'unitID': worker['ID'], 'unitAction': random.choice(valid_actions)})

        # Get all the actions that are available for a base
        available_base_actions = self.get_available_actions_by_type_name(unit_type_table, 'Base')
        for base in available_bases:
            # Get the valid actions for a particular base
            valid_actions = self.get_valid_actions_for_unit(base, available_base_actions, valid_action_positions_for_state)

            # If we have some valid actions, choose a random one
            if len(valid_actions) > 0:
                actions.append({'unitID': base['ID'], 'unitAction': random.choice(valid_actions)})

        if len(actions):
            self._logger.info(json.dumps(actions))

        resources_being_used = self.get_resource_usage_from_state(state)
        resources_used_in_new_actions = self.get_resource_usage_from_actions(actions)

        # Potential resource usage
        potential_resource_usage = resources_being_used + resources_used_in_new_actions

        # If we dont have enought resources to run some commands, we remove those commands
        if potential_resource_usage > self.get_resources_for_player(state):
            for action in actions:
                if action['unitAction']['type'] == pyrts.Action.PRODUCE:
                    action['unitAction'] = {'type': pyrts.Action.NONE}

        # For busy units we need to just send NONE action (-1)
        for unit_id in busy_units:
            actions.append({'unitID': unit_id, 'unitAction': {'type': pyrts.Action.NONE}})

        return actions


if __name__ == '__main__':
    ai = AI(0)
    ai.start()
