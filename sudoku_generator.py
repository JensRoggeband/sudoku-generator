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

# getting desired difficulty from command line
difficulty = difficulties[sys.argv[2]]

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

# set these before executing!
url = ''
auth = '321321321321321'
timestamp = '2022-00-00T18:00:00.000Z'

url = 'https://firestore.googleapis.com/v1/projects/sudoku-d2d5c/databases/(default)/documents/puzzles'
fields = {
    'cells': generated.map_to_response(),
    'date_added': {
        'timestampValue': '2022-08-28T18:00:00.000Z'
    },
    'difficulty': {
        'stringValue': sys.argv[2]
    }
}
body = {
    'fields': fields
}
headers = {'Authorization': 'Bearer 123'}

print(json.dumps(body))

# response = requests.post(url, data=json.dumps(body), headers=headers)

# response = requests.post(url, json=json, headers=headers)
# print(response)

# printing out board after reduction
print("The generated board after removals was: \r\n\r\n{0}".format(final))
