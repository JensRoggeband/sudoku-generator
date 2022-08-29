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

# applying logical reduction with corresponding difficulty cutoff
gen.reduce_via_logical(difficulty[0])

# catching zero case
if difficulty[1] != 0:
    # applying random reduction with corresponding difficulty cutoff
    gen.reduce_via_random(difficulty[1])


# getting copy after reductions are completed
final = gen.board.copy()

# set these before executing!
url = ''
auth = '321321321321321'
timestamp = '2022-00-00T18:00:00.000Z'

fields = {
    'cells': final.mapToResponse(),
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

response = requests.post(url, json=body, headers=headers)
print(response)
