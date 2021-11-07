## Rappels pour les développeurs

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
