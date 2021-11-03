# Water Sort Puzzle

`Water Sort Puzzle` est un jeu où on doit transvaser des éprouvettes les unes dans les autres pour trier leur
contenu.

Au début du jeu, on a X éprouvettes contenant chacune jusqu'à Y doses de liquides différents.
Ici, Y = constante (= 4) définie dans la classe 'Eprouvette'

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


## Rappels

### Tests unitaires

#### Unittest
  Python `unittest` est installé de base avec python.

  `python -m unittest` pour dérouler tous les tests unitaires

#### Pytest
  `pytest` est un package à installer mais il est de + en + utilisé en remplacement de `unittest`
  En outre, `pytest` exécute parfaitement des des tests prévus pour `unittest`.

  `pip install -U pytest` pour l'installation

  `pytest` pour dérouler les tests unitaires

  `pytest` déroule des différents tests en parallèle.
  `pytest` est plus élaboré pour l'écriture des fichiers de tests unitaires (paramétrages, par exemple)

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
