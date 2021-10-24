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
  `python -m unittest` pour dérouler tous les tests unitaires

### Coverage

  `pip install coverage` pour installer l'outil
  'coverage --version' pour vérifier la version installée
  `coverage run xyz` pour lancer la couverture de code du module xyz
  `coverage run -m unittest` pour lancer la couverture de code sur tous les tests unitaires
  `coverage report` pour un résumé de la couverture de code (console)
  `coverage report -m` pour un résume de la couverture de code avec les numéros de lignes non couvertes
  'coverage html' pour générer un rapport dans ./htmpcov (ouvrir index.html)

 