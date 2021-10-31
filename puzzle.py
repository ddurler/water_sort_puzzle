#! coding:utf-8

# Import pour pouvoir faire du typing :Puzzle dans la classe Puzzle
from __future__ import annotations

from typing import Any, List, Tuple, Generator
from collections import Counter
from itertools import permutations

from eprouvette import Eprouvette


class Puzzle:
    """
    Un puzzle contient des @see Eprouvette.

    On peut créer le puzzle en indiquant une liste d'éprouvette.
    On peut compléter le puzzle avec la méthode @see add_eprouvette

    La propriété @see is_consistant permet de vérifier que le puzzle est consistant par rapport au
    contenu des éprouvettes
    """

    # Restreint les propriétés des instances pour gagner du temps et de la mémoire
    __slots__ = "_eprouvettes"

    def __init__(self, epouvettes: List[Eprouvette] | None = None) -> None:
        self._eprouvettes: List[Eprouvette] = []
        if epouvettes:
            for eprouvette in epouvettes:
                self.add_eprouvette(eprouvette)

    def add_eprouvette(self, eprouvette: Eprouvette) -> None:
        """Ajoute une éprouvette au puzzle."""
        self._eprouvettes.append(eprouvette)

    def __len__(self) -> int:
        """Implémente l'opération len() pour un puzzle -> Nombre d'éprouvettes du puzzle."""
        return len(self._eprouvettes)

    def __getitem__(self, index: int) -> Eprouvette:
        """i-eme eprouvette du puzzle."""
        return self._eprouvettes[index]

    def is_same_as(self, other: Puzzle) -> bool:
        """
        @return True si les 2 puzzles sont similaires
        (mêmes éprouvettes mais pas forcement dans le même ordre).
        @see __equ__ pour une stricte identité.
        """
        if len(self) != len(other):
            return False
        # Table des éprouvettes identifiées idem dans other puzzle
        table: List[bool] = [False for _ in range(len(self))]
        for e0 in self.iter_eprouvettes():
            found_in_other = False
            for i, e1 in enumerate(other.iter_eprouvettes()):
                if not table[i] and e0.is_same_as(other[i]):
                    table[i] = True
                    found_in_other = True
                    break
            if not found_in_other:
                return False
        return True

    def iter_eprouvettes(self):
        """Implémente un itérateur sur toutes les éprouvettes du puzzle."""
        for eprouvette in self._eprouvettes:
            yield eprouvette

    def iter_permutations(self) -> Generator[Tuple[Any, ...], None, None]:
        """Iterator sur toutes les combinaisons Tuple[Eprouvette, Eprouvette] du puzzle."""
        for permutation in permutations(self.iter_eprouvettes(), 2):
            yield permutation

    @property
    def is_consistant(self) -> bool:
        """
        Vérifie la consistance du puzzle.
        @return True si une solution est envisageable pour le puzzle, False sinon.

        Une solution est envisageable si la somme des doses d'un même liquide dans toutes
        les éprouvettes est un multiple du nombre de doses dans chaque éprouvette.
        Ce qui indique qu'une fois résolu, on aura bien des éprouvettes remplies d'un même liquide

        On vérifie également qu'il y a au moins le contenu d'une éprouvette vide dans le puzzle
        """

        # Somme toutes les doses de liquides dans toutes les éprouvettes
        compteur: Counter = Counter()
        for eprouvette in self.iter_eprouvettes():
            for dose_liquide in eprouvette.iter_doses():
                compteur[dose_liquide] += 1

        # Vérifie que la somme des doses pour chaque liquide est un multiple de la taille des éprouvettes
        for nb_doses_liquide in compteur.values():
            if nb_doses_liquide % Eprouvette.MAX_DOSES != 0:
                return False

        # Décompte des doses vides dans les éprouvettes
        nb_doses_vides = 0
        for eprouvette in self.iter_eprouvettes():
            nb_doses_vides += Eprouvette.MAX_DOSES - eprouvette.nb_doses

        # Vérifie qu'on a au moins le contenu d'une éprouvette vide
        if nb_doses_vides < Eprouvette.MAX_DOSES:
            return False

        # Tout est OK
        return True

    @property
    def is_done(self) -> bool:
        """@return True si le puzzle est terminé."""
        eprouvette: Eprouvette
        for eprouvette in self.iter_eprouvettes():
            if not (
                eprouvette.is_vide
                or (eprouvette.is_pleine and len(eprouvette.liquides) == 1)
            ):
                return False
        return True

    def clone(self) -> Puzzle:
        """Crée et retourne une copie clone du puzzle."""
        copy_list_eprouvettes: List[Eprouvette] = []
        for eprouvette in self.iter_eprouvettes():
            copy_list_eprouvettes.append(eprouvette.clone())

        return Puzzle(copy_list_eprouvettes)

    def __repr__(self):
        ret = ""
        for n, eprouvette in enumerate(self.iter_eprouvettes()):
            if ret:
                ret += ", "
            ret += f"#{n + 1}{eprouvette}"
        return f"Puzzle<{ret}>"
