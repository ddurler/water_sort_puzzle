#! coding:utf-8

# Import pour pouvoir faire du typing :Eprouvette dans la classe Eprouvette
from __future__ import annotations

from typing import Sequence, List, Set, Any


class EprouvetteError(Exception):
    """Toutes les exceptions détectées par la classe Eprouvette."""

    def __init__(self, e=None):
        super().__init__(e)


class Eprouvette:
    """
    Une éprouvette contient jusqu'à 4 doses de liquide.

    Le contenu d'une éprouvette est une séquence d'objets où chaque objet identifie un liquide particulier.

    doses = [None, None, None, None] si l'éprouvette est vide (nb_doses = 0)
    doses = ['X', None, None, None] si l'éprouvette contient une dose de 'X' (nb_doses = 1)
            Ici on a 1 dose d'un liquide dans l'éprouvette
    doses = ['X', 'Y', 'Y', None] si l'éprouvette contient une dose de 'X' et 2 doses de 'Y' au dessus (nb_doses = 3)
            Ici on a 3 doses avec 2 liquides différents dans l'éprouvette
    """

    # Restreint les propriétés des instances pour gagner du temps et de la mémoire
    __slots__ = "doses", "nb_doses"

    MAX_DOSES = 4

    def __init__(self, doses: Sequence):
        self.doses: List[Any] = [
            None,
        ] * Eprouvette.MAX_DOSES
        self.nb_doses = 0
        for dose in doses:
            if dose is not None:
                self.doses[self.nb_doses] = dose
                self.nb_doses += 1

    @property
    def is_vide(self) -> bool:
        """@return True si l'éprouvette est vide."""
        return self.nb_doses == 0

    @property
    def is_pleine(self) -> bool:
        """@return True si l'éprouvette est pleine."""
        return self.nb_doses == Eprouvette.MAX_DOSES

    @property
    def liquides(self) -> Set[Any]:
        """@return Set des différents liquides dans l'éprouvette."""
        return set(self.doses[: self.nb_doses])

    @property
    def nb_different_liquides(self) -> int:
        """Nombre de liquides différents dans l'éprouvette."""
        return len(self.liquides)

    @property
    def top_liquide(self) -> Any | None:
        """Liquide du dessus dans l'éprouvette."""
        if self.nb_doses == 0:
            return None
        return self.doses[self.nb_doses - 1]

    def iter_doses(self):
        """Implémente un itérateur sur toutes les doses de l'éprouvette."""
        for i in range(self.nb_doses):
            yield self.doses[i]

    def is_same_as(self, other: Eprouvette) -> bool:
        """@return True si les éprouvettes sont identiques."""
        if self.nb_doses != other.nb_doses:
            return False
        for i in range(self.nb_doses):
            if self.doses[i] != other.doses[i]:
                return False
        return True

    def pop_dose(self) -> Any:
        """Retire une dose en haut de l'éprouvette."""
        if self.is_vide:
            raise EprouvetteError(
                "On ne peut pas retirer une dose d'une éprouvette vide"
            )
        ret = self.doses[self.nb_doses - 1]
        self.doses[self.nb_doses - 1] = None
        self.nb_doses -= 1
        return ret

    def can_push_dose(self, liquide: Any) -> bool:
        """@return True si liquide peut-être versé dans l'éprouvette."""
        if self.nb_doses == 0:
            return True
        if self.nb_doses == Eprouvette.MAX_DOSES:
            return False
        return self.doses[self.nb_doses - 1] == liquide

    def push_dose(self, liquide: Any) -> None:
        """Ajoute une dose de liquide dans l'éprouvette."""
        if not self.can_push_dose(liquide):
            raise EprouvetteError(
                f"Impossible d'ajouter du {liquide} dans l'éprouvette {self}"
            )
        self.doses[self.nb_doses] = liquide
        self.nb_doses += 1

    def is_possible_verser_une_dose_dans(self, destination: Eprouvette) -> bool:
        """@return True si au moins une dose de liquide peut être versée vers l'éprouvette destination."""
        if self.nb_doses == 0:
            return False
        if destination.nb_doses == 0:
            return True
        if destination.nb_doses == Eprouvette.MAX_DOSES:
            return False
        # Si les liquides sont les mêmes
        return (
            self.doses[self.nb_doses - 1] == destination.doses[destination.nb_doses - 1]
        )

    def is_interessant_verser_dans(self, destination: Eprouvette) -> bool:
        """@return True si verser la source dans la destination est un mouvement possible et interressant à étudier."""
        if destination.nb_doses == Eprouvette.MAX_DOSES:
            return False
        if self.nb_doses == 0:
            return False  # Source vide
        if destination.nb_doses == 0:
            if self.nb_different_liquides == 1:
                return False  # Car la situation est inchangée au final
            return True
        return (
            self.doses[self.nb_doses - 1] == destination.doses[destination.nb_doses - 1]
        )

    def verser_dans(self, destination: Eprouvette) -> int:
        """Verse toutes les doses possibles vers l'éprouvette destination.
        @return le nombre de doses versées
        """
        nb_doses = 0
        while self.is_possible_verser_une_dose_dans(destination):
            liquide = self.pop_dose()
            destination.push_dose(liquide)
            nb_doses += 1
        return nb_doses

    def clone(self) -> Eprouvette:
        """Crée et retourne une copie clone de l'éprouvette."""
        copy_list_doses = self.doses.copy()
        return Eprouvette(copy_list_doses)

    def __repr__(self):
        return f"<{self.doses[:self.nb_doses]}>"
