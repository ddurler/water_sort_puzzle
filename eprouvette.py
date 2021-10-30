#! coding:utf-8

# Import pour pouvoir faire du typing :Eprouvette dans la classe Eprouvette
from __future__ import annotations

from typing import Sequence, Set, Any


class EprouvetteError(Exception):
    """Toutes les exceptions détectées par la classe Eprouvette."""

    def __init__(self, e=None):
        super().__init__(e)


class Eprouvette:
    """
    Une éprouvette contient des doses de liquide.

    Le contenu d'une éprouvette est une séquence d'objets où chaque objet identifie un liquide particulier.

    Le nombre de doses avec du liquide est donné par la fonction len().
    Le nombre max de doses avant que l'éprouvette ne déborde est donné par la propriété max_len.
    Par défaut, max_len vaut None, ce qui signifie que l'éprouvette ne débordera jamais.

    _doses = [] si l'éprouvette est vide
    _doses = ['X'] si l'éprouvette contient une dose de 'X'
            Ici on a 1 dose d'un liquide dans l'éprouvette
    _doses = ['X', 'Y', 'Y'] si l'éprouvette contient une dose de 'X' et 2 doses de 'Y' au dessus
            Ici on a 3 doses avec 2 liquides différents dans l'éprouvette
    """

    def __init__(self, doses: Sequence, max_len=None):
        self._max_len = None
        self._doses = [dose for dose in doses if dose is not None]
        self._len_doses = len(self._doses)  # speeding further computation
        if max_len is not None:
            self.max_len = max_len

    @property
    def max_len(self) -> int | None:
        return self._max_len

    @max_len.setter
    def max_len(self, value: int | None):
        if value is None:
            self._max_len = None
        else:
            value = int(value)
            if value < 0:
                raise EprouvetteError(
                    f"max_len = {value} impossible pour une éprouvette"
                )
            self._max_len = int(value)
            if value < len(self):
                raise EprouvetteError(
                    f"max_len = {value} impossible, il y a déjà {len(self)} doses dans l'éprouvette"
                )
            self._max_len = value

    @property
    def is_vide(self) -> bool:
        """@return True si l'éprouvette est vide."""
        return self._len_doses == 0

    @property
    def is_pleine(self) -> bool:
        """@return True si l'éprouvette est pleine."""
        if self.max_len is None:
            return False
        return self._len_doses == self.max_len

    def __len__(self) -> int:
        """Implémente len() pour une éprouvette -> Nombre de doses dans l'éprouvette."""
        return self._len_doses

    @property
    def liquides(self) -> Set[Any]:
        """@return Set des différents liquides dans l'éprouvette."""
        return set(self._doses)

    @property
    def nb_different_liquides(self) -> int:
        """Nombre de liquides différents dans l'éprouvette."""
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
        if self.max_len is not None and index >= self.max_len:
            raise EprouvetteError(
                f"Index = {index} : On ne peut pas avoir plus de {self.max_len} dans l'éprouvette"
            )
        if index >= len(self):
            return None
        return self._doses[index]

    def __iter__(self):
        """Implémente un itérateur sur toutes les doses de l'éprouvette."""
        return self._doses.__iter__()

    def __eq__(self, other: object) -> bool:
        """Implémente l'opérateur == entre 2 éprouvettes."""
        if not isinstance(other, Eprouvette):
            return False
        if len(self) != len(other):
            return False
        # + pythonique (mais non optimisé):  for liquide1, liquide2 in zip(self, other):
        for i in range(self._len_doses):
            if self[i] != other[i]:
                return False
        return True

    def pop_dose(self) -> Any:
        """Retire une dose en haut de l'éprouvette."""
        if self.is_vide:
            raise EprouvetteError(
                "On ne peut pas retirer une dose d'une éprouvette vide"
            )
        self._len_doses -= 1
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
        self._len_doses += 1
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
        return Eprouvette(copy_list_doses, max_len=self.max_len)

    def __repr__(self):
        return f"<{self._doses}>"
