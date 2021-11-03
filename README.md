# Water Sort Puzzle

`Water Sort Puzzle` est un jeu où on doit transvaser des éprouvettes les unes dans les autres pour trier leur
contenu.

Au début du jeu, on a X éprouvettes contenant chacune jusqu'à Y doses de liquides différents.
Ici, Y = constante (= 4) définie dans la classe `Eprouvette`.

L'ensemble constitue un `puzzle` à résoudre :

On ne peut verser une éprouvette dans l'autre que si :
1 - Il y a au moins une dose de liquide dans l'éprouvette d'origine
2 - L'éprouvette destination contient au moins une dose vide
3 - Si l'éprouvette destination n'est pas vide, le type de liquide qui va être versé de l'éprouvette d'origine
    vers l'éprouvette destination doit correspondre

Exemple :

| R |    |   |    | V |   |   |
| R |    |   |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)

On a ici 4 éprouvettes contenant 4 doses au maximum.
La première éprouvette (1) contient 2 doses de B et 2 doses de R au dessus.
On peut verser le contenu de (1) dans (2) car les il y a du R dans (2).
On ne peut pas verser (1) dans (3) parce que (3) est déjà rempli.
On ne peut pas verser (1) dans (4) parce qu'il y a du V dans (4) et que (1) verse du R.

L'**objectif** est d'effectuer les manipulations nécessaires pour que chaque éprouvette ne contient qu'un
seul même liquide.

Ici, on verse (1) dans (2) :

|   |    | R |    | V |   |   |
|   |    | R |    | V |   |   |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)

 On verse (3) dans (4) :

|   |    | R |    |   |   | V |
|   |    | R |    |   |   | V |
| B |    | R |    | B |   | V |
| B |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)

 Et on verse (1) dans (3) :

|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
|   |    | R |    | B |   | V |
-----    -----    -----   -----
 (1)      (2)      (3)     (4)

 Et c'est terminé...

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

* **verbose_cycle** : Si non num, défini une période en seconde pour que l'algorithme de recherche donne
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

Un puzzle est valide pour être résolu s'il contient au moins une éprouvette vide et que le nombre de
doses des différentes couleurs est un multiple de la taille d'une éprouvette (4 doses).

## Eprouvette

La classe `eprouvette` permet de créer et de résoudre les `puzzle`. Une `eprouvette` contient des 'doses' de
'liquide'.
Par défaut, il y a 4 doses maximum par éprouvette.
Un liquide peut être n'importe quel objet python qui support l'opération __eq__ pour être comparée aux autres.

Quand elle est construire, les liquides sont donnés 'de bas en haut':

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
  Python `unittest` est installé de base avec python.
  [Voir ici](https://docs.python.org/3/library/unittest.html)

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

  CVCode propose un onglet `TEST` dédié pour la réalisation et le suivi des tests unitaires.

  Lors de la première utilisation, VSCode propose les menus pour configurer automatiquement les tests unitaires.
  Cette configuration est faite dans `.vscode\settings.json`

### Coverage

  `pip install coverage` pour installer l'outil
  'coverage --version' pour vérifier la version installée
  `coverage run xyz` pour lancer la couverture de code du module xyz
  `coverage run -m unittest` pour lancer la couverture de code des tests unitaires avec `unittest`
  `coverage run -m pytest` pour lancer la couverture de code des tests unitaires avec `pytest`
  `coverage report` pour un résumé de la couverture de code (console)
  `coverage report -m` pour un résume de la couverture de code avec les numéros de lignes non couvertes
  `coverage html` pour générer un rapport dans ./htmlcov (ouvrir index.html)

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
