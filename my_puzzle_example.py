"""
Puzzle resolution example.
See README.md file.
"""

# Import required modules
from bottle import Bottle
from puzzle import Puzzle
from puzzle_solver import solve_generic

"""
Puzzle to be solved in this example:

        | R |    |   |    | V |   |   |
        | R |    |   |    | V |   |   |
        | B |    | R |    | B |   | V |
        | B |    | R |    | B |   | V |
        -----    -----    -----   -----
         (1)      (2)      (3)     (4)
"""
puzzle: Puzzle = Puzzle([Bottle("BBRR"), Bottle("RR"), Bottle("BBVV"), Bottle("VV")])

# Solving
solve_generic(puzzle)
