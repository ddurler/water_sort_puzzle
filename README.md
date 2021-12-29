# Water Sort Puzzle

`Water Sort Puzzle` is a game starting with several bottles having different colored water in them.  
The goal is to have the same color in each bottle or empty bottles.

At the beginning, a `puzzle` to be solved contains `Bottle`'s.  
Each `Bottle` might have up to max 4 doses of same or different colors.

_In here, this constant MAX_DOSES = 4 is defined in the `Bottle` class._

A bottle can be pored into another bottle only if:

* There is at least one dose of colored water at the top of the source bottle
* There is at least one empty dose in the destination bottle
* In case the destination bottle is not empty, its top color must match the top color in the source bottle

When poured, all possible colored doses from the source bottle go to the destination bottle.

Example :

```
| R |    |   |    | V |   |   |
| R |    |   |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

Here are 4 bottles with max 4 doses of colored water in each.

The first bottle (1) contains 2 doses of B and 2 doses of R on its top.  
One can pour bottle (1) into bottle (2) as there is R in (2).  
One cannot pour bottle (1) into (3) because bottle (3) is already full.  
One cannot pour bottle (1) into (4) because there is V on top of bottle (4) and bottle (1) pours color R.  

The **goal** is to find the moves to finally gets one-color only or empty bottles.

Starting from this example:

```
| R |    |   |    | V |   |   |
| R |    |   |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

Pour (1) into (2) :

```
|   |    | R |    | V |   |   |
|   |    | R |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

 Pour (3) into (4) :

```
|   |    | R |    |   |   | V |
|   |    | R |    |   |   | V |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

 And pour (1) into (3) :

```
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

And it's done...

## Solving using justpy_puzzle_solver

The `justpy_puzzle_solver` module exposes an HTTP server which serves HTML page to help water sort puzzle resolution.

First run the HTTP server using the `python .\justpy_puzzle_solver.py`.  
Then, open a browser and connect to this server. On the local machine, use `localhost` or `127.0.0.1` HTTP address.
Once the page is loaded, follow the instruction to create and solve the puzzle.


## How to solve a puzzle in 'pure python'

To solve a puzzle, proceed as follows with the content of this module;

First, create a new python file in the directory: `my_puzzle.py` for instance.

Edit this file and first, import the required modules:

```
from bottle import Bottle
from puzzle import Puzzle
from puzzle_solver import solve_generic
```

Then, define the puzzle to be solved by describing its bottles content.

_Reminder : Bottle content is defined from bottom to top._

Any object can be used as a color in the bottles.    
As python strings are simple chars sequences, an easy way is to choose a different letter for every color.

The puzzle shown in the introduction chapter would then simply be:

```
puzzle: Puzzle = Puzzle(
    [Bottle("BBRR"), Bottle("RR"), Bottle("BBVV"), Bottle("VV")]
)
```

To computing the solution: `solve_generic(puzzle)`

Thus, the entire `my_puzzle.py` file content is:

```
from bottle import Bottle
from puzzle import Puzzle
from puzzle_solver import solve_generic

puzzle = Puzzle(
    [Bottle("BBRR"), Bottle("RR"), Bottle("BBVV"), Bottle("VV")]
)

solve_generic(puzzle)

```

And the python command to run is: `python my_puzzle.py`


This gives the following output:

```
Solution (0.000 secs):
Step#1: Puzzle::
  Puzzle<#1<['B', 'B', 'R', 'R']>, #2<['R', 'R']>, #3<['B', 'B', 'V', 'V']>, #4<['V', 'V']>>
Step#2: Pour #3 into #4:
  Puzzle<#1<['B', 'B', 'R', 'R']>, #2<['R', 'R']>, #3<['B', 'B']>, #4<['V', 'V', 'V', 'V']>>
Step#3: Pour #1 into #2:
  Puzzle<#1<['B', 'B']>, #2<['R', 'R', 'R', 'R']>, #3<['B', 'B']>, #4<['V', 'V', 'V', 'V']>>
Step#4: Pour #1 into #3:
  Puzzle<#1<[]>, #2<['R', 'R', 'R', 'R']>, #3<['B', 'B', 'B', 'B']>, #4<['V', 'V', 'V', 'V']>>
```

## puzzle_solver

`puzzle_solver` class is for solving `puzzle`:

```
  solver: PuzzleSolver = PuzzleSolver(puzzle)

  solution: Optional[PuzzleChain] = solver.solve(
      nb_chains_without_empty_bottle=nb_chains_without_empty_bottle, verbose_cycle=verbose_cycle
  )

  if solution:
      print(solution.show_puzzle_chains())
  else:
      print(f"Non résolu : {puzzle}\n") 
```

**solve** method parameters:

* **nb_chains_without_empty_bottle** : If not nul, defines the max consecutive possible moves without seing an
  empty bottle in the puzzle. To be used for more human likely solution finding.

* **verbose_cycle** : If not nul, periodical trace (in seconds) of the current solving situation.
  To be used in case of long computations.


## puzzle

A `puzzle` is a list of `bottle's.

```
    GREEN = 0
    PINK = 1
    YELLOW = 2
    DARK_BLUE = 3
    GRAY = 4
    LIGHT_BLUE = 5
    RED = 6
    ORANGE = 7
    VIOLET = 8

    puzzle: Puzzle = Puzzle(
    [
        Bottle([GREEN, PINK, YELLOW, DARK_BLUE]),
        Bottle([GRAY, YELLOW, LIGHT_BLUE, LIGHT_BLUE]),
        Bottle([GRAY, RED, GRAY, RED]),
        Bottle([GREEN, DARK_BLUE, ORANGE, GREEN]),
        Bottle([ORANGE, PINK, PINK, ORANGE]),
        Bottle([YELLOW, VIOLET, GRAY, VIOLET]),
        Bottle([LIGHT_BLUE, PINK, VIOLET, YELLOW]),
        Bottle([LIGHT_BLUE, VIOLET, ORANGE, DARK_BLUE]),
        Bottle([DARK_BLUE, RED, GREEN, RED]),
        Bottle([]),
        Bottle([]),
    ]
),
```

A puzzle is 'consistent' if a solution is possible. This means that moves can be found so that bottles
can be fulled with only one color.  
This check is done with the following rules:

* The sum of each color dose must match the bottle dose size (4)
* Empty doses for the content of at least one empty bottle must exist in the puzzle


## Bottle

The `Bottle` class is used to create and solve a `puzzle`.  
A `Bottle` contains 'dose's of colored water (or 'color').  
The default dose size is set to 4 doses of color per bottle.  
In the `Bottle` class, a color can be any not None object as long it supports the __eq__ operator to be compared
with other colors.

A `Bottle` is defined by specifying its color content from the bottom to the top:

For instance, `bottle: Bottle = Bottle("AABC")` defines the following bottle:

    | C |
    | B |
    | A |
    | A |
    -----

