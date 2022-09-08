# !/usr/bin/python
import sys
import requests
import json
from Sudoku.Generator import *

# setting difficulties and their cutoffs for each solve method
difficulties = {
    'easy': (81, 5), 
    'medium': (81, 10), 
    'hard': (81, 15)
}

# set these before executing!
url = ''
auth = ''
id = -1000 # check latest ID online first 
timestamp = ''
# set these before executing!

# getting desired difficulty from command line
difficulty = difficulties[sys.argv[2]]

if len(sys.argv) > 3:
    amount_of_puzzles = int(sys.argv[3])
else:
    amount_of_puzzles = 1

print("We are going to generate " + str(amount_of_puzzles) + " puzzle(s)")

for x in range(amount_of_puzzles):
    id = id + 1

    # constructing generator object from puzzle file (space delimited columns, line delimited rows)
    gen = Generator(sys.argv[1])

    # applying 100 random transformations to puzzle
    gen.randomize(100)

    # getting a copy before slots are removed
    initial = gen.board.copy()

    print("The generated board: \r\n\r\n{0}".format(initial))

    # applying logical reduction with corresponding difficulty cutoff
    gen.reduce_via_logical(difficulty[0])

    # catching zero case
    if difficulty[1] != 0:
        # applying random reduction with corresponding difficulty cutoff
        gen.reduce_via_random(difficulty[1])

    # getting copy after reductions are completed
    final = gen.board.copy()

    generated = initial.set_zeros_to_soft_value(final)

    fields = {
        'id': {
            'stringValue': str(id)
        },
        'cells': generated.map_to_response(),
        'date_added': {
            'timestampValue': timestamp
        },
        'difficulty': {
            'stringValue': sys.argv[2]
        }
    }
    body = {
        'fields': fields
    }
    headers = {'Authorization': 'Bearer ' + auth}

    # print(json.dumps(body))

    response = requests.post(url, json=body, headers=headers)
    print(response)

    # printing out board after reduction
    print("The generated board after removals was: \r\n\r\n{0}".format(final))
