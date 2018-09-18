# python-microRTS

A python client library for microRTS.

## Overview

The python client library makes use of the `SocketAI` interface in the microRTS library.


## How to use

1. Create a class that inherits the `Server` class in  `server.py`

```
from pyrts.server import Server


class AI(server):

....

```

2. Implement the method `get_action`


```

class AI(Server):

    def get_action(state):
        # In here implement the algorithm that takes the state and creates the action

        return [ ..  list of actions]


```

The format of the action should be the following:

```

[
    {
        "unitID": 0 - the unit that you wish to control
        "unitAction": {
            'type': 1 - the type of action (this is defined in the unit type table)
            'parameters': 0 - the parameters for the action (this is defined in the unit type table)
        }
    },
    {
        ... more actions for different unitID s
    }
]


```

#### Note
Actions for agents can take several time steps, `server.py` will automatically filter out any actions that are returned
by the `get_action` method that are currently performing a previous action.

### Useful functions in the Server class

#### get_busy_units(units)

Get a list of the units that are currently busy performing an action

#### get_available_actions_by_type(unit_type_table, type)

Given the unit type and the unit type table, return a complete list of the possible actions that unit can perform

#### get_unit_type_table()

This function returns the unit type table, which describes the environment.

for example, the environment `basesWorkers16x16.xml` will return:

```
{
 "moveConflictResolutionStrategy": 1,
 "unitTypes": [
  {
   "maxDamage": 1,
   "producedBy": [],
   "name": "Resource",
   "produces": [],
   "canAttack": false,
   "hp": 1,
   "moveTime": 10,
   "canMove": false,
   "isResource": true,
   "sightRadius": 0,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 1,
   "produceTime": 10,
   "attackTime": 10,
   "minDamage": 1,
   "canHarvest": false,
   "isStockpile": false,
   "harvestTime": 10,
   "ID": 0,
   "returnTime": 10
  },
  {
   "maxDamage": 1,
   "producedBy": [
    "Worker"
   ],
   "name": "Base",
   "produces": [
    "Worker"
   ],
   "canAttack": false,
   "hp": 10,
   "moveTime": 10,
   "canMove": false,
   "isResource": false,
   "sightRadius": 5,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 10,
   "produceTime": 250,
   "attackTime": 10,
   "minDamage": 1,
   "canHarvest": false,
   "isStockpile": true,
   "harvestTime": 10,
   "ID": 1,
   "returnTime": 10
  },
  {
   "maxDamage": 1,
   "producedBy": [
    "Worker"
   ],
   "name": "Barracks",
   "produces": [
    "Light",
    "Heavy",
    "Ranged"
   ],
   "canAttack": false,
   "hp": 4,
   "moveTime": 10,
   "canMove": false,
   "isResource": false,
   "sightRadius": 3,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 5,
   "produceTime": 200,
   "attackTime": 10,
   "minDamage": 1,
   "canHarvest": false,
   "isStockpile": false,
   "harvestTime": 10,
   "ID": 2,
   "returnTime": 10
  },
  {
   "maxDamage": 1,
   "producedBy": [
    "Base"
   ],
   "name": "Worker",
   "produces": [
    "Base",
    "Barracks"
   ],
   "canAttack": true,
   "hp": 1,
   "moveTime": 10,
   "canMove": true,
   "isResource": false,
   "sightRadius": 3,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 1,
   "produceTime": 50,
   "attackTime": 5,
   "minDamage": 1,
   "canHarvest": true,
   "isStockpile": false,
   "harvestTime": 20,
   "ID": 3,
   "returnTime": 10
  },
  {
   "maxDamage": 2,
   "producedBy": [
    "Barracks"
   ],
   "name": "Light",
   "produces": [],
   "canAttack": true,
   "hp": 4,
   "moveTime": 8,
   "canMove": true,
   "isResource": false,
   "sightRadius": 2,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 2,
   "produceTime": 80,
   "attackTime": 5,
   "minDamage": 2,
   "canHarvest": false,
   "isStockpile": false,
   "harvestTime": 10,
   "ID": 4,
   "returnTime": 10
  },
  {
   "maxDamage": 4,
   "producedBy": [
    "Barracks"
   ],
   "name": "Heavy",
   "produces": [],
   "canAttack": true,
   "hp": 4,
   "moveTime": 12,
   "canMove": true,
   "isResource": false,
   "sightRadius": 2,
   "attackRange": 1,
   "harvestAmount": 1,
   "cost": 2,
   "produceTime": 120,
   "attackTime": 5,
   "minDamage": 4,
   "canHarvest": false,
   "isStockpile": false,
   "harvestTime": 10,
   "ID": 5,
   "returnTime": 10
  },
  {
   "maxDamage": 1,
   "producedBy": [
    "Barracks"
   ],
   "name": "Ranged",
   "produces": [],
   "canAttack": true,
   "hp": 1,
   "moveTime": 10,
   "canMove": true,
   "isResource": false,
   "sightRadius": 3,
   "attackRange": 3,
   "harvestAmount": 1,
   "cost": 2,
   "produceTime": 100,
   "attackTime": 5,
   "minDamage": 1,
   "canHarvest": false,
   "isStockpile": false,
   "harvestTime": 10,
   "ID": 6,
   "returnTime": 10
  }
 ]
}

```