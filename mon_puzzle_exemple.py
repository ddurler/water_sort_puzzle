"""
Exemple de résolution du puzzle.
Voir le fichier README.md pour les explications
"""

# Import des définitions nécessaires
from eprouvette import Eprouvette
from puzzle import Puzzle
from puzzle_solver import solve_generic

"""
Définition du puzzle à résoudre
Ici :
        | R |    |   |    | V |   |   |
        | R |    |   |    | V |   |   |
        | B |    | R |    | B |   | V |
        | B |    | R |    | B |   | V |
        -----    -----    -----   -----
         (1)      (2)      (3)     (4)
"""
puzzle: Puzzle = Puzzle(
    [Eprouvette("BBRR"), Eprouvette("RR"), Eprouvette("BBVV"), Eprouvette("VV")]
)

# Résolution
solve_generic(puzzle)
