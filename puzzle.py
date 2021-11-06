#! coding:utf-8

# Import to do typing :Puzzle inside class Puzzle
from __future__ import annotations

from typing import Any, List, Sequence, Tuple, Generator
from collections import Counter
from itertools import permutations

from bottle import Bottle


class Puzzle:
    """
    A puzzle contains @see Bottle.

    A puzzle can be created by specifying a sequence of Bottles.
    Bottle can further be added to the puzzle @see add_bottle.

    Property @see is_consistent verifies the puzzle is correctly defined with bottle contents and
    might have a possible solving solution.
    """

    # Speedup properties for this class
    __slots__ = "_bottles"

    def __init__(self, bottles: Sequence[Bottle] | None = None) -> None:
        self._bottles: List[Bottle] = []
        if bottles:
            for bottle in bottles:
                self.add_bottle(bottle)

    def add_bottle(self, bottle: Bottle) -> None:
        """Add a bottle to the puzzle."""
        self._bottles.append(bottle)

    def __len__(self) -> int:
        """@return number of bottles in the puzzle."""
        return len(self._bottles)

    def __getitem__(self, index: int) -> Bottle:
        """@return i-nd bottle of the puzzle."""
        return self._bottles[index]

    def is_same_as(self, other: Puzzle) -> bool:
        """
        @return True when the puzzles are the same.
        (same bottles even if not in the same order).
        @see __equ__ for strict equality.
        """
        if len(self) != len(other):
            return False
        table: List[bool] = [
            False for _ in range(len(self))
        ]  # Identified bottles in other puzzle
        for self_bottle in self.iter_bottles():
            found_in_other = False
            for i, other_bottle in enumerate(other.iter_bottles()):
                if not table[i] and self_bottle.is_same_as(other[i]):
                    table[i] = True
                    found_in_other = True
                    break
            if not found_in_other:
                return False
        return True

    def iter_bottles(self):
        """Iterates on every bottle in the puzzle."""
        for bottle in self._bottles:
            yield bottle

    def iter_permutations(self) -> Generator[Tuple[Any, ...], None, None]:
        """Iterator on all Tuple[Bottle, Bottle] of the puzzle bottles."""
        for permutation in permutations(self.iter_bottles(), 2):
            yield permutation

    @property
    def is_consistent(self) -> bool:
        """
        Check for puzzle consistency.
        @return True if puzzle is likely to be solved, else False.

        A solution is possible when bottles can be fulled with only one color.
        Empty doses for the content of at least one empty bottle must exist in the puzzle.
        """

        # Sum colors in bottles
        color_counters: Counter = Counter()
        for bottle in self.iter_bottles():
            for color_dose in bottle.iter_doses():
                color_counters[color_dose] += 1

        # Check color counters are correctly bottle sized
        for nb_color_doses in color_counters.values():
            if nb_color_doses % Bottle.MAX_DOSES != 0:
                return False

        # Sum empty doses in bottles
        nb_empty_doses = 0
        for bottle in self.iter_bottles():
            nb_empty_doses += Bottle.MAX_DOSES - bottle.nb_doses

        # At least one bottle size should be empty
        if nb_empty_doses < Bottle.MAX_DOSES:
            return False

        # All correct
        return True

    @property
    def is_done(self) -> bool:
        """@return True when the puzzle is solved."""
        bottle: Bottle
        for bottle in self.iter_bottles():
            if not (bottle.is_empty or (bottle.is_full and len(bottle.colors) == 1)):
                return False
        return True

    def clone(self) -> Puzzle:
        """@return Create a copy clone of the puzzle."""
        copy_list_bottles: List[Bottle] = []
        for bottle in self.iter_bottles():
            copy_list_bottles.append(bottle.clone())

        return Puzzle(copy_list_bottles)

    def contains_empty_bottle(self) -> bool:
        """@return True if at least one bottle is empty in the puzzle."""
        for bottle in self.iter_bottles():
            if bottle.is_empty:
                return True
        return False

    def __repr__(self):
        ret = ""
        for n, bottle in enumerate(self.iter_bottles()):
            if ret:
                ret += ", "
            ret += f"#{n + 1}{bottle}"
        return f"Puzzle<{ret}>"
