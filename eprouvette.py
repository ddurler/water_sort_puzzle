#! coding:utf-8

# Import pour pouvoir faire du typing :Eprouvette dans la classe Eprouvette
from __future__ import annotations

from typing import List, Set, Any

"""
Une éprouvette contient MAX_DOSES doses de liquide.

Le contenu d'une éprouvette est une List[Any] où Any est un objet qui identifie un liquide particulier.

Contenu = [] si l'éprouvette est vide
Contenu = ['X'] si l'éprouvette contient une dose de 'X'
Contenu = ['X', 'Y', 'Y'] si l'éprouvette contient une dose de 'X' et 2 doses de 'Y' au dessus
"""


class EprouvetteError(Exception):
    """Toutes les exceptions détectées par la classe Eprouvette."""

    def __init__(self, e=None):
        super().__init__(e)


class Eprouvette:

    MAX_DOSES: int = 4  # Nombre max de doses par éprouvettes

    def __init__(self, doses: List[Any]):
        if len(doses) > self.MAX_DOSES:
            raise EprouvetteError(
                f"{doses} : On ne peut pas avoir plus de {self.MAX_DOSES} dans l'éprouvette"
            )
        self._doses = [dose for dose in doses if dose is not None]

    @property
    def is_vide(self) -> bool:
        """@return True si l'éprouvette est vide."""
        return len(self._doses) == 0

    @property
    def is_pleine(self) -> bool:
        """@return True si l'éprouvette est pleine."""
        return len(self._doses) == self.MAX_DOSES

    @property
    def nb_total_doses(self) -> int:
        """Nombre total de doses dans l'éprouvette [entre 0 et MAX_DOSES]."""
        return len(self._doses)

    @property
    def liquides(self) -> Set[Any]:
        """@return Set des différents liquides dans l'éprouvette."""
        return set(self._doses)

    @property
    def nb_different_liquides(self) -> int:
        """Nombre de liquides différents dans l'éprouvette [entre 0 et MAX_DOSES]."""
        return len(self.liquides)

    @property
    def top_liquide(self) -> Any | None:
        """Liquide du dessus dans l'éprouvette."""
        if self.is_vide:
            return None
        return self._doses[-1]

    def __getitem__(self, index: int) -> Any | None:
        """Liquide dans la i-eme dose de l'éprouvette."""
        if index < 0:
            return self._doses[-1]
        if index >= self.MAX_DOSES:
            raise EprouvetteError(
                f"Index = {index} : On ne peut pas avoir plus de {self.MAX_DOSES} dans l'éprouvette"
            )
        if index >= self.nb_total_doses:
            return None
        return self._doses[index]

    def __iter__(self):
        """Implémente un itérateur sur toutes les doses de l'éprouvette."""
        return self._doses.__iter__()

    def pop_dose(self) -> Any:
        """Retire une dose en haut de l'éprouvette."""
        if self.is_vide:
            raise EprouvetteError(
                "On ne peut pas retirer une dose d'une éprouvette vide"
            )
        return self._doses.pop()

    def can_push_dose(self, liquide: Any) -> bool:
        """@return True si liquide peut-être versé dans l'éprouvette."""
        if liquide is None:  # Cas trivial
            return False
        if self.is_vide:
            return True
        elif self.is_pleine:
            return False
        # Sinon selon liquide au sommet de l'éprouvette
        return liquide == self.top_liquide

    def push_dose(self, liquide: Any) -> None:
        """Ajoute une dose de liquide dans l'éprouvette."""
        if liquide is None:
            raise EprouvetteError(f"Impossible d'ajouter None dans l'éprouvette {self}")
        if not self.can_push_dose(liquide):
            raise EprouvetteError(
                f"Impossible d'ajouter du {liquide} dans l'éprouvette {self}"
            )
        self._doses.append(liquide)

    def is_possible_verser_une_dose_dans(self, destination: Eprouvette) -> bool:
        """@return True si au moins une dose de liquide peut être versée vers l'éprouvette destination."""
        assert isinstance(destination, Eprouvette)
        if self.is_vide:
            return False
        if destination.is_vide:
            return True
        if destination.is_pleine:
            return False
        # Si les liquides sont les mêmes
        return self.top_liquide == destination.top_liquide

    def verser_dans(self, destination: Eprouvette) -> int:
        """Verse toutes les doses possibles vers l'éprouvette destination.
        @return le nombre de doses versées
        """
        assert isinstance(destination, Eprouvette)
        nb_doses = 0
        while self.is_possible_verser_une_dose_dans(destination):
            liquide = self.pop_dose()
            destination.push_dose(liquide)
            nb_doses += 1
        return nb_doses

    def clone(self) -> Eprouvette:
        """Crée et retourne une copie clone de l'éprouvette."""
        copy_list_doses = self._doses.copy()
        return Eprouvette(copy_list_doses)

    def __repr__(self):
        return f"Eprouvette<{self._doses}>"
