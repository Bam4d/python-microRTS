from pyrts import Server
import json
from collections import defaultdict
from random import randint

class AI(Server):
    """
    Finds a single worker and moves it randomly
    """

    def __init__(self):
        super(AI, self).__init__()

    def get_action(self, state):

        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## CREATE A TEST ACTION

        ## find a unit that we can move
        ## I AM PLAYER 1
        for unit in unit_by_player[1]:
            if unit['type'] == 'Worker':
                unit_id = unit['ID']

        if not unit_id:
            return []

        unit_action = {'type': 1, 'parameter': randint(1,4)}
        test_action = {'unitID': unit_id, 'unitAction': unit_action}

        return [test_action]


ai = AI()

if __name__ == '__main__':
    print('server is running')
    ai.start()