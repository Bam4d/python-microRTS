import json
from collections import defaultdict
from random import choice

from pyrts import Server, Direction


class AI(Server):
    """
    Finds a single worker and moves it randomly
    """

    def __init__(self, player_id):
        super(AI, self).__init__(player_id)

    def get_action(self, state, gameover):
        unit_by_player = defaultdict(list)
        for unit in state['pgs']['units']:
            unit_by_player[unit['player']].append(unit)

        self._logger.debug(json.dumps(state, indent=1, separators=(',', ': ')))

        ## CREATE A TEST ACTION


        unit_id = None
        ## find a unit that we can move
        ## I AM PLAYER 1
        for unit in unit_by_player[self.player_id]:
            if unit['type'] == 'Worker':
                unit_id = unit['ID']

        if unit_id is None:
            return []

        unit_action = {'type': 1, 'parameter': choice(Direction.as_list())}
        test_action = {'unitID': unit_id, 'unitAction': unit_action}

        return [test_action]



if __name__ == '__main__':
    ai = AI(0)
    ai.start()