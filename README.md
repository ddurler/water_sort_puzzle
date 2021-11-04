# Water Sort Puzzle

`Water Sort Puzzle` est un jeu où on doit transvaser des éprouvettes les unes dans les autres pour trier leur
contenu.

Au début du jeu, un `puzzle` à résoudre avec X éprouvettes contenant chacune jusqu'à Y doses
de liquides différents.

_Ici, Y = constante (= 4) définie dans la classe `Eprouvette`._

On ne peut verser une éprouvette dans une autre que si :

* Il y a au moins une dose de liquide dans l'éprouvette d'origine
* L'éprouvette destination contient au moins une dose vide
* Si l'éprouvette destination n'est pas vide, le type de liquide qui va être versé de l'éprouvette d'origine
  vers l'éprouvette destination doit correspondre

Exemple :

```
| R |    |   |    | V |   |   |
| R |    |   |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

On a ici 4 éprouvettes contenant 4 doses au maximum.

La première éprouvette (1) contient 2 doses de B et 2 doses de R au dessus.  
On peut verser le contenu de (1) dans (2) car les il y a du R dans (2).  
On ne peut pas verser (1) dans (3) parce que (3) est déjà rempli.  
On ne peut pas verser (1) dans (4) parce qu'il y a du V dans (4) et que (1) verse du R.  

L'**objectif** est d'effectuer les manipulations nécessaires pour que chaque éprouvette ne contient qu'un
seul même liquide.

Ici, on verse (1) dans (2) :

```
|   |    | R |    | V |   |   |
|   |    | R |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

 On verse (3) dans (4) :

```
|   |    | R |    |   |   | V |
|   |    | R |    |   |   | V |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

 Et on verse (1) dans (3) :

```
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)
```

Et c'est terminé...

## Comment résoudre un puzzle

Voici comment le puzzle ci-dessus peut être résolu.

Il faut créer un nouveau fichier python dans ce répertoire : `mon_puzzle.py` par exemple.

Au début du fichier, on importe les définitions nécessaires :

```
from eprouvette import Eprouvette
from puzzle import Puzzle
from puzzle_solver import PuzzleSolver, solve_generic
```

Puis on définit le puzzle à résoudre par la suite des éprouvettes contenue dans le puzzle.

_Rappel : Le contenu des éprouvettes est défini de bas en haut._

On peut utiliser n'importe quel type d'objet pour identifier les différents liquides dans les éprouvettes.  
Si on choisit une lettre, le contenu d'une éprouvette devient alors une simple chaîne de caractères
puisque qu'une string est itérable.

Pour le puzzle montré en introduction de ce document, on aurait :

```
puzzle: Puzzle = Puzzle(
    [Eprouvette("BBRR"), Eprouvette("RR"), Eprouvette("BBVV"), Eprouvette("VV")]
)
```

Puis, le calcul de résolution de ce puzzle : `solve_generic(puzzle)`

On a donc un fichier `mon_puzzle.py` avec :

```
from eprouvette import Eprouvette
from puzzle import Puzzle
from puzzle_solver import solve_generic

puzzle = Puzzle(
    [Eprouvette("BBRR"), Eprouvette("RR"), Eprouvette("BBVV"), Eprouvette("VV")]
)

solve_generic(puzzle)

```

La résolution est lancée par la commande python `python mon_puzzle.py`.
On a alors le résultat suivant :

```
Solution (0.001 secs) :
Step#1: Puzzle initial:
  Puzzle<#1<['B', 'B', 'R', 'R']>, #2<['R', 'R']>, #3<['B', 'B', 'V', 'V']>, #4<['V', 'V']>>
Step#2: Verser #3 dans #4:
  Puzzle<#1<['B', 'B', 'R', 'R']>, #2<['R', 'R']>, #3<['B', 'B']>, #4<['V', 'V', 'V', 'V']>>
Step#3: Verser #1 dans #2:
  Puzzle<#1<['B', 'B']>, #2<['R', 'R', 'R', 'R']>, #3<['B', 'B']>, #4<['V', 'V', 'V', 'V']>>
Step#4: Verser #1 dans #3:
  Puzzle<#1<[]>, #2<['R', 'R', 'R', 'R']>, #3<['B', 'B', 'B', 'B']>, #4<['V', 'V', 'V', 'V']>>
```

## puzzle_solver

La classe `puzzle_solver` permet de résoudre les `puzzle`:

```
  solver: PuzzleSolver = PuzzleSolver(puzzle)

  solution: PuzzleChain | None = solver.solve(
      nb_chains_sans_vide=nb_chains_sans_vide, verbose_cycle=verbose_cycle
  )

  if solution:
      print(solution.show_puzzle_chains())
  else:
      print(f"Non résolu : {puzzle}\n") 
```

Paramètres de la méthode **solve** :

* **nb_chains_sans_vide** : Si non nul, défini un nombre maximum de mouvements avant d'observer au moins une
  éprouvette vide dans le le puzzle. En activant ce paramètre, on obtient une solution non optimale mais
  plus proche d'une séquence qu'un humain pourrait découvrir

* **verbose_cycle** : Si non nul, défini une période en seconde pour que l'algorithme de recherche donne
  des indications sur son avancement


## puzzle

Les `puzzle` sont des collections d'`eprouvette`.

```
    VERT = 0
    ROSE = 1
    JAUNE = 2
    BLEU_FONCE = 3
    GRIS = 4
    BLEU_CLAIR = 5
    ROUGE = 6
    ORANGE = 7
    VIOLET = 8

    puzzle: Puzzle = Puzzle(
    [
        Eprouvette([VERT, ROSE, JAUNE, BLEU_FONCE]),
        Eprouvette([GRIS, JAUNE, BLEU_CLAIR, BLEU_CLAIR]),
        Eprouvette([GRIS, ROUGE, GRIS, ROUGE]),
        Eprouvette([VERT, BLEU_FONCE, ORANGE, VERT]),
        Eprouvette([ORANGE, ROSE, ROSE, ORANGE]),
        Eprouvette([JAUNE, VIOLET, GRIS, VIOLET]),
        Eprouvette([BLEU_CLAIR, ROSE, VIOLET, JAUNE]),
        Eprouvette([BLEU_CLAIR, VIOLET, ORANGE, BLEU_FONCE]),
        Eprouvette([BLEU_FONCE, ROUGE, VERT, ROUGE]),
        Eprouvette([]),
        Eprouvette([]),
    ]
),
```

Un puzzle est valide pour être résolu s'il contient au moins le contenu une éprouvette vide (mais pas
forcément dans la même éprouvette) et que le nombre de doses des différentes couleurs est un multiple 
de la taille d'une éprouvette (4 doses).

## Eprouvette

La classe `eprouvette` permet de créer et de résoudre les `puzzle`.  
Une `eprouvette` contient des 'doses' de 'liquide'.  
Par défaut, il y a 4 doses maximum par éprouvette.  
Un liquide peut être n'importe quel objet python qui support l'opération __eq__ pour être comparée aux autres.

Quand l'éprouvette est construite, les liquides sont listés 'de bas en haut':

`eprouvette: Eprouvette = Eprouvette("AABC")`

équivaut à l'éprouvette :

    | C |
    | B |
    | A |
    | A |
    -----

## Rappels

### Tests unitaires

#### Unittest
  [`unittest`](https://docs.python.org/3/library/unittest.html) est installé de base avec python.

  `python -m unittest` pour dérouler tous les tests unitaires

  **note** Les tests de ce module ont migrés en `pytest`.

#### Pytest
  [`pytest`](https://docs.pytest.org/) est un package à installer mais il est de + en +
  utilisé en remplacement de `unittest`.  
  En outre, `pytest` exécute parfaitement des des tests prévus pour `unittest`.

  `pip install -U pytest` pour l'installation

  `pytest` pour dérouler les tests unitaires

  `pytest` déroule des différents tests en parallèle.  
  `pytest` est plus simple pour l'écriture de tests unitaires (paramétrages, par exemple)


### VSCode

  VSCode propose un onglet `TEST` dédié à la réalisation et le suivi des tests unitaires.

  Lors de la première utilisation, VSCode propose les menus pour configurer automatiquement les tests unitaires.  
  Cette configuration est faite dans `.vscode\settings.json`

### Coverage

  `pip install coverage` pour installer l'outil  
  `coverage run xyz` pour lancer la couverture de code du module xyz  
  `coverage run -m unittest` pour lancer la couverture de code des tests unitaires avec `unittest`  
  `coverage run -m pytest` pour lancer la couverture de code des tests unitaires avec `pytest`  
  `coverage report` pour un résumé de la couverture de code (console)  
  `coverage report -m` pour un résume de la couverture de code avec les numéros de lignes non couvertes  
  `coverage html` pour générer un rapport complet dans `./htmlcov` (ouvrir `index.html`)

### pytest-cov

  Il existe également `pytest-cov` pour avoir `pytest` et `coverage` en même temps:  
  `pip install pytest-cov`  
  `pytest . --cov` pour avoir la couverture de code directement affichée  
  `pytest . --cov --cov_report=html` pour avoir la couverture de code au format html (idem coverage html)

### cProfile

 `python -m cProfile xyz.py` pour donner des statistiques sur le nombre d'appels de fonctions et la durée
 d'exécution dans les différentes fonctions

### mypy

[mypy](https://mypy.readthedocs.io/en/latest/index.html) est un outil statique pour vérifier les types d'un
programme python.

`pip install mypy` pour installer l'outil (il existe une extension pour VSCode)  
`mypy monfichier.py` pour analyser un fichier source python  
`pypy .` pour analyser tous les fichiers du répertoire courant  

 ### black

 [black](https://github.com/psf/black) est un outil de reformatage du code source python.

 `pip install black` pour installer l'outil  
 `black monfichier.py` pour modifier le code source du fichier conformément aux règles pythoniques  
 `black .` pour modifier tous les codes source d'un répertoire  
 
 ### flake8

 [flake8](https://flake8.pycqa.org/en/latest/) est un autre outil d'analyse statique de code.

 `pip install flake8` pour installer l'outil  
 `flake8 monfichier.py` pour analyser un fichier source python  
 `flake8 .` pour analyser tous les fichiers du répertoire courant  
 `flake8 --ignore=E501 .` pour inhiber tous les warnings concernant les lignes de + de 80 caractères  

 ATTENTION: `black` et `flake8` se contredisent parfois sur certaines règles...
