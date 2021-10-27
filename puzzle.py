#! coding:utf-8

# Import pour pouvoir faire du typing :Puzzle dans la classe Puzzle
from __future__ import annotations

from typing import List
from collections import Counter

from eprouvette import Eprouvette


class Puzzle:
    """
    Un puzzle contient des @see Eprouvette.

    On peut créer le puzzle en indiquant une liste d'éprouvette.
    On peut compléter le puzzle avec la méthode @see add_eprouvette

    La méthode @see is_consistant permet de vérifier que le puzzle est consistant par rapport au
    contenu des éprouvettes
    """

    def __init__(self, epouvettes: List[Eprouvette] | None = None) -> None:
        self._eprouvettes: List[Eprouvette] = []
        if epouvettes:
            for eprouvette in epouvettes:
                self.add_eprouvette(eprouvette)

    def add_eprouvette(self, eprouvette: Eprouvette) -> None:
        """Ajoute une éprouvette au puzzle."""
        assert isinstance(eprouvette, Eprouvette)
        self._eprouvettes.append(eprouvette)

    def __len__(self) -> int:
        """Implémente l'opération len() pour un puzzle -> Nombre d'éprouvettes du puzzle."""
        return len(self._eprouvettes)

    def __eq__(self, other: object) -> bool:
        """Implémente l'opérateur == entre les puzzles."""
        if not isinstance(other, Puzzle):
            return False
        if len(self) != len(other):
            return False
        for e0, e1 in zip(self, other):
            if e0 != e1:
                return False
        return True

    def __iter__(self):
        """Implémente un itérateur sur toutes les éprouvettes du puzzle."""
        return self._eprouvettes.__iter__()

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
        for eprouvette in self:
            for dose_liquide in eprouvette:
                compteur[dose_liquide] += 1

        # Vérifie que la somme des doses pour chaque liquide est un multiple de la taille des éprouvettes
        for nb_doses_liquide in compteur.values():
            if nb_doses_liquide % Eprouvette.MAX_DOSES != 0:
                return False

        # Décompte des doses vides dans les éprouvettes
        nb_doses_vides = 0
        for eprouvette in self:
            nb_doses_vides += Eprouvette.MAX_DOSES - len(eprouvette)

        # Vérifie qu'on a au moins le contenu d'une éprouvette vide
        if nb_doses_vides < Eprouvette.MAX_DOSES:
            return False

        # Tout est OK
        return True

    def clone(self) -> Puzzle:
        """Crée et retourne une copie clone du puzzle."""
        copy_list_eprouvettes = []
        for eprouvette in self:
            copy_list_eprouvettes.append(eprouvette.clone())

        return Puzzle(copy_list_eprouvettes)

    def __repr__(self):
        ret = ""
        for eprouvette in self:
            if ret:
                ret += ", "
            ret += f"{eprouvette}"
        return f"Puzzle<{ret}>"
