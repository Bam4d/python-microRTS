import logging
import socket
import sys
import json

PLAYER = 0

NONE = 0
MOVE = 1
HARVEST = 2
RETURN = 3
PRODUCE = 4
ATTACK = 5

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Server(object):

    def __init__(self):
        logging.basicConfig()
        self._logger = logging.getLogger('RTSServer')
        self._logger.setLevel(logging.DEBUG)

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _ack(self):
        self._send()

    def _send(self, data=None):
        if data is not None:
            data_string = json.dumps(data)
        else:
            data_string = ''

        self._connection.send(('%s\n' % data_string).encode('utf-8'))

    def _wait_for_message(self):
        environment_message = self._connection.recv(4096).decode('utf-8')
        if environment_message[0] == u'\n':
            return ('ACK')
        self._logger.debug('Message: %s' % environment_message)
        message_parts = environment_message.split('\n')
        self._logger.debug(message_parts[0])
        return message_parts

    def _filter_invalid_actions(self, actions, state):
        '''
        Get the units that are currently performing actions from the state and remove any actions that refer to these
        units
        :return: A filtered list of all the actions that can be applied
        '''
        busy_units = self.get_busy_units(state)
        return [action for action in actions if action['unitID'] not in busy_units]

    def get_action(self, state, gameover):
        '''
        To be implemented by a syper class
        :param state:
        :return:
        '''
        pass

    def _process_state_and_get_action(self, state, gameover):
        self.get_grid_from_state(state)

        actions = self.get_action(state, gameover)

        if gameover:
            return None
        else:
            return self._filter_invalid_actions(actions, state)


    def _wait_for_get_action(self):
        message_parts = self._wait_for_message()

        command = message_parts[0].split()
        if command[0] == 'getAction':

            state = json.loads(message_parts[1])
            self._logger.debug('state: %s' % state)
            gameover = False
        else:
            gameover = True
            state = {}

        return self._process_state_and_get_action(state, gameover)

    def _get_budgets(self):
        _, self._time_budget, self._iteration_budget = self._wait_for_message()[0].split()
        self._ack()

    def _get_utt(self):
        utt = self._wait_for_message()
        self._unit_type_table = json.loads(utt[1])
        self._ack()

    def get_unit_type_table(self):
        return self._unit_type_table

    def get_busy_units(self, state):
        return [unit['ID'] for unit in state['actions']]

    def _get_invalid_move_positions(self, state):
        return set([(unit['x'], unit['y']) for unit in state['pgs']['units']])

    def _get_valid_harvest_positions(self, state):
        return set([(unit['x'], unit['y']) for unit in state['pgs']['units'] if unit['type'] == "Resource"])

    def _get_valid_base_positions(self, state):
        return set([(unit['x'], unit['y']) for unit in state['pgs']['units'] if unit['type'] == "Base" and unit['player'] == PLAYER])

    def _get_valid_attack_positions(self, state):
        return set([(unit['x'], unit['y']) for unit in state['pgs']['units'] if unit['type'] != "Resource" and unit['player'] != PLAYER])


    def get_valid_action_positions_for_state(self, state):
        '''
        Returns a tuple containing the following:
        invalid_move_positions - a set of all the positions that cannot be moved into
        valid_harvest_positions -  a set of all the resource locations
        valid_base_positions - a set of the positions of bases on the current players team
        valid_attack_positions - a set of the positions that can be attacked

        These positions can be cross-referenced with possible actions that units can perform, to make sure no invalid
        actions are sent to the environment
        '''

        return (
            self._get_invalid_move_positions(state),
            self._get_valid_harvest_positions(state),
            self._get_valid_base_positions(state),
            self._get_valid_attack_positions(state)
        )

    def get_valid_actions_for_unit(self, unit, available_actions, valid_positions):
        '''
        Get the actions that are valid for a unit to perform.

        An action is INVALID if the action cannot be performed in the environment.

        For example, if the action is MOVE(left) but the position to the left of the unit is blocked
        '''

        (
            invalid_move_positions,
            valid_harvest_positions,
            valid_base_positions,
            valid_attack_positions
         ) = valid_positions

        valid_actions = []

        self._logger.info('unit [%s] position [%d, %d]' % (unit['type'], unit['x'], unit['y']))

        # For all the actions make sure that those actions are possible
        for action in available_actions:
            position = self.get_action_position(action, unit)
            if action['type'] == MOVE:
                if self._is_on_grid(position) and position not in invalid_move_positions:
                    valid_actions.append(action)

            if action['type'] == HARVEST:
                if self._is_on_grid(position) and position in valid_harvest_positions:
                    valid_actions.append(action)

            if action['type'] == RETURN:
                if self._is_on_grid(position) and position in valid_base_positions:
                    valid_actions.append(action)

            if action['type'] == ATTACK:
                if self._is_on_grid(position) and position in valid_attack_positions:
                    action['x'] = position[0]
                    action['y'] = position[1]
                    valid_actions.append(action)

            if action['type'] == PRODUCE:
                # Unavailable produce positions are the same as unavailable move positions
                if self._is_on_grid(position) and position not in invalid_move_positions:
                    valid_actions.append(action)

        self._logger.info('valid actions for unit [%s]: %s' % (unit['type'], valid_actions))
        return valid_actions

    def get_action_position(self, action, unit):
        if action['parameter'] == UP:
            return (unit['x'], unit['y'] - 1)
        if action['parameter'] == RIGHT:
            return (unit['x'] + 1, unit['y'])
        if action['parameter'] == DOWN:
            return (unit['x'], unit['y'] + 1)
        if action['parameter'] == LEFT:
            return (unit['x'] - 1, unit['y'])

    def _is_on_grid(self, position):
        return position[0] >= 0 and \
               position[1] >= 0 and \
               position[0] < self._max_x and \
               position[1] < self._max_y

    def get_available_actions_by_type_name(self, unit_type_table, type_name):
        '''
        Gets a list of the available actions that can be performed by a particlar unit
        '''

        available_actions = []

        # Get unit type by type name
        unit_type = [unit for unit in unit_type_table['unitTypes'] if unit['name'] == type_name][0]

        # canMove
        if unit_type['canMove']:
            available_actions.extend(self._get_directional_actions(MOVE))

        # canAttack
        if unit_type['canAttack']:
            # This is more complicated because the params have x-y coordinates and a range
            if unit_type['attackRange'] == 1:
                available_actions.extend(self._get_directional_actions(ATTACK))

        # canHarvest
        if unit_type['canHarvest']:
            available_actions.extend(self._get_directional_actions(HARVEST))
            available_actions.extend(self._get_directional_actions(RETURN))

        # If this unit can produce anything
        if len(unit_type['produces']) > 0:
            available_actions.extend([
                {'type': PRODUCE, 'unitType': unit_type_name,'parameter': UP } for unit_type_name in unit_type['produces']
            ])
            available_actions.extend([
                {'type': PRODUCE, 'unitType': unit_type_name, 'parameter': RIGHT} for unit_type_name in unit_type['produces']
            ])
            available_actions.extend([
                {'type': PRODUCE, 'unitType': unit_type_name, 'parameter': DOWN} for unit_type_name in unit_type['produces']
            ])
            available_actions.extend([
                {'type': PRODUCE, 'unitType': unit_type_name, 'parameter': LEFT} for unit_type_name in unit_type['produces']
            ])

        return available_actions

    def get_resources_for_player(self, state, for_player=None):
        '''
        Get the number of resources the player currently has available
        '''

        if not for_player:
            for_player = 0

        for player in state['pgs']['players']:
            if player['ID'] == for_player:
                return player['resources']

    def _get_directional_actions(self, action_type):
        return [{'type': action_type, 'parameter': direction} for direction in [UP, DOWN, LEFT, RIGHT]]

    def get_grid_from_state(self, state):
        '''
        Gets the width and height of the environment
        '''

        self._max_x = state['pgs']['width']
        self._max_y = state['pgs']['height']

        return (self._max_x, self._max_y)

    def get_resource_usage_from_state(self, state):
        '''
        How many resources are currently being used to build units
        '''

        used_resources = 0
        unit_types = self._unit_type_table['unitTypes']
        for action in state['actions']:
            unit_action = action['action']
            if unit_action['type'] == PRODUCE:
                for unit_type in unit_types:
                    if unit_action['unitType'] == unit_type['name']:
                        used_resources += unit_type['cost']

        return used_resources

    def get_resource_usage_from_actions(self, actions):
        '''
        From a list of actions, sum the cost of the actions
        '''

        used_resources = 0
        unit_types = self._unit_type_table['unitTypes']
        for action in actions:
            unit_action = action['unitAction']
            if unit_action['type'] == PRODUCE:
                for unit_type in unit_types:
                    if unit_action['unitType'] == unit_type['name']:
                        used_resources += unit_type['cost']

        return used_resources

    def start(self):
        self._logger.debug('Socket created')

        # Bind socket to local host and port
        try:
            self._s.bind(('localhost', 9898))
        except socket.error as msg:
            self._logger.debug('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            self._s.close()
            sys.exit()

        self._logger.debug('Socket bind complete')

        # Start listening on socket
        self._s.listen(10)
        self._logger.debug('Socket now listening')

        # now keep talking with the client
        self._connection, addr = self._s.accept()
        self._logger.debug(self._connection)
        self._logger.debug(addr)

        self._ack()
        self._logger.debug('Connected with ' + addr[0] + ':' + str(addr[1]))

        # Get the headers
        self._get_budgets()
        self._get_utt()

        gameover = False

        while not gameover:
            action = self._wait_for_get_action()
            if action is not None:
                self._logger.debug('Sending action %s' % action)
                self._send(action)
            else:
                self._logger.debug('Game has ended')
                gameover = True


        self._s.close()