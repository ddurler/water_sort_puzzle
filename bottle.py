#! coding:utf-8

"""
The bottle module defines the Bottle class that is one element in
a water sort puzzle.
"""

# Import to do typing :Bottle inside class Bottle
from __future__ import annotations

from typing import Sequence, Optional, List, Set, Any


class BottleError(Exception):
    """Exception from the Bottle class."""


class Bottle:
    """
    A bottle contains doses of colored water (up to Bottle.MAX_DOSES)

    The content of a bottle is a List of objects where each objet identifies a color.

    doses = [None, None, None, None] in case of empty bottle (nb_doses = 0)
    doses = ['X', None, None, None] where the bottle contains only one dose of 'X' (nb_doses = 1)
    doses = ['X', 'Y', 'Y', None] where the bottle contains one dose of 'X' at the bottom and
            2 doses of 'Y' at the top (nb_doses = 3)
            In this situation, the bottle contains 3 doses with 2 different colors
    """

    # Speedup properties for this class
    __slots__ = "doses", "nb_doses"

    MAX_DOSES = 4

    def __init__(self, doses: Sequence):
        self.doses: List[Any] = [
            None,
        ] * Bottle.MAX_DOSES
        self.nb_doses = 0
        for dose in doses:
            if dose is not None:
                self.doses[self.nb_doses] = dose
                self.nb_doses += 1

    @property
    def is_empty(self) -> bool:
        """@return True if the bottle is empty."""
        return self.nb_doses == 0

    @property
    def is_full(self) -> bool:
        """@return True if the bottle is full."""
        return self.nb_doses == Bottle.MAX_DOSES

    @property
    def colors(self) -> Set[Any]:
        """@return Set of the different colors in the bottle."""
        return set(self.doses[: self.nb_doses])

    @property
    def nb_different_colors(self) -> int:
        """Number of different colors in the bottle."""
        return len(self.colors)

    @property
    def top_color(self) -> Optional[Any]:
        """Top color in the bottle."""
        if self.nb_doses == 0:
            return None
        return self.doses[self.nb_doses - 1]

    def iter_doses(self):
        """Iterator on every dose holding a color in the bottle."""
        for i in range(self.nb_doses):
            yield self.doses[i]

    def is_same_as(self, other: Bottle) -> bool:
        """
        @return True if bottles are the same.
        (same as __eq__ but not checking isinstance of the other bottle to speedup computation)
        """
        if self.nb_doses != other.nb_doses:
            return False
        for i in range(self.nb_doses):
            if self.doses[i] != other.doses[i]:
                return False
        return True

    def pop_dose(self) -> Any:
        """Pop the top dose in the bottle and return its color."""
        if self.is_empty:
            raise BottleError("Cannot pop dose from an empty bottle")
        ret = self.doses[self.nb_doses - 1]
        self.doses[self.nb_doses - 1] = None
        self.nb_doses -= 1
        return ret

    def can_push_dose(self, color: Any) -> bool:
        """@return True if one dose of the color can be poured into the bottle."""
        if self.nb_doses == 0:
            return True
        if self.nb_doses == Bottle.MAX_DOSES:
            return False
        return self.doses[self.nb_doses - 1] == color

    def push_dose(self, color: Any) -> None:
        """Pour one dose of the color into the bottle."""
        if not self.can_push_dose(color):
            raise BottleError(f"Cannot pour {color} into {self}")
        self.doses[self.nb_doses] = color
        self.nb_doses += 1

    def is_possible_to_pour_one_dose_into(self, destination: Bottle) -> bool:
        """
        @return True if at least one dose of the top color can be poured into
        the destination bottle.
        """
        if self.nb_doses == 0:
            return False
        if destination.nb_doses == 0:
            return True
        if destination.nb_doses == Bottle.MAX_DOSES:
            return False
        # Same top colors ?
        return (
            self.doses[self.nb_doses - 1] == destination.doses[destination.nb_doses - 1]
        )

    def is_interesting_to_pour_into(self, destination: Bottle) -> bool:
        """
        @return True if pouring into destination leads to an interesting situation.
        (Quite the same as is_possible_to_pour_one_dose_into but also checking for
        interesting resulting situation)
        """
        if destination.nb_doses == Bottle.MAX_DOSES:
            return False  # destination is full
        if self.nb_doses == 0:
            return False  # Source empty
        if destination.nb_doses == 0:
            if self.nb_different_colors == 1:
                return False  # Because de resulting situation would be the same
            return True
        # Same top colors ?
        return (
            self.doses[self.nb_doses - 1] == destination.doses[destination.nb_doses - 1]
        )

    def pour_into(self, destination: Bottle) -> int:
        """Pour all possible doses of top color into the destination bottle.
        @return number of poured doses
        """
        nb_doses = 0
        while self.is_possible_to_pour_one_dose_into(destination):
            color = self.pop_dose()
            destination.push_dose(color)
            nb_doses += 1
        return nb_doses

    def clone(self) -> Bottle:
        """@return Create a copy clone of the bottle."""
        copy_list_doses = self.doses.copy()
        return Bottle(copy_list_doses)

    def __repr__(self):
        return f"<{self.doses[:self.nb_doses]}>"
