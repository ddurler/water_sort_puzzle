#! coding:utf-8

# Import to do typing :PuzzleChain inside class PuzzleChain
from __future__ import annotations

from itertools import permutations
import collections
import time
import math
from typing import Optional

from bottle import Bottle
from puzzle import Puzzle


class PuzzleChain:
    """
    PuzzleChain links puzzle move from a previous PuzzleChain to a new puzzle.

    It could be a dataclass but it also has the responsability of counting the consecutive moves
    without having an empty bottle in the chained puzzles.

    Showing the whole chain results is also in the scope of this class.
    """

    # Speedup properties for this class
    __slots__ = (
        "previous_puzzle_chain",
        "puzzle",
        "message",
        "nb_chains_without_empty_bottle",
    )

    def __init__(
        self, previous_puzzle_chain: Optional[PuzzleChain], puzzle: Puzzle, message: str
    ) -> None:
        """
        PuzzleChain containing the previous puzzle or None for the first one
        Puzzle in chain
        Message indicating the move to do from the previous puzzle that leads to this puzzle
        """
        self.previous_puzzle_chain = previous_puzzle_chain
        self.puzzle = puzzle
        self.message = message

        # Number of previous PuzzleChain with having at least one empty bottle
        if previous_puzzle_chain is None:
            self.nb_chains_without_empty_bottle = 0
        elif puzzle.contains_empty_bottle():
            self.nb_chains_without_empty_bottle = 0
        else:
            self.nb_chains_without_empty_bottle = (
                previous_puzzle_chain.nb_chains_without_empty_bottle + 1
            )

    def show_puzzle_chains(self) -> str:
        """Show the full PuzzleChain's from the start given one end PuzzleChain."""

        # Create list of puzzles in the chain
        q: collections.deque[PuzzleChain] = collections.deque()
        q.append(self)
        previous = self.previous_puzzle_chain
        while previous is not None:
            q.append(previous)
            previous = previous.previous_puzzle_chain

        # Show all moves
        ret = ""
        step = 1
        while len(q):
            puzzle_chain: PuzzleChain = q.pop()
            ret += f"Step#{step}: {puzzle_chain.message}:\n  {puzzle_chain.puzzle}\n"
            step += 1
        return ret


class PuzzleSolver:
    """
    PuzzleSolver is for one Puzzle solving.

    The solving uses 'brut force' to compute all possible moves from each possible situation.
    The initial situation is the puzzle to solve.

    It is possible to specify a maximum number of consecutive moves having an empty bottle
    in the puzzle.
    When used, this option will not give the optimal solution but it is likely to find a solution
    that matches human ways of solving the puzzle.

    If computing takes long times, it is also possible to activate the verbose mode that prints
    regular data on actual computation.
    """

    def __init__(self, puzzle: Puzzle) -> None:
        if not puzzle.is_consistent:
            raise ValueError(f"Bad puzzle: {puzzle}")
        self.puzzle: Puzzle = puzzle.clone()

    @staticmethod
    def str_second(sec: float) -> str:
        """Convert second duration into hours, minutes and seconds to be printed."""
        sec_value = int(sec) % (24 * 3600)
        hour_value = sec_value // 3600
        sec_value %= 3600
        min_value = sec_value // 60
        sec_value %= 60
        if hour_value:
            return f"{hour_value} h {min_value:02d} mn {sec_value:02d} s"
        elif min_value:
            return f"{min_value} mn {sec_value:02d} s"
        else:
            return f"{sec_value} secs"

    @staticmethod
    def estimated_time(nb_todo: int, nb_done: int, time_done: float) -> float:
        """
        @return estimated duration to compute nb_todo given time_done for computing nb_done.
        This model used here is an exponential one: t = math.exp(a * nb)
        """
        try:
            a: float = math.log(time_done) / nb_done
            total_time = math.exp(a * (nb_done + nb_todo))
            return total_time - time_done
        except (ValueError, ZeroDivisionError, OverflowError):
            return 0

    def solve(
        self, nb_chains_without_empty_bottle: int = 0, verbose_cycle: float = 0.0
    ) -> Optional[PuzzleChain]:
        """
        Solve the puzzle.
        nb_chains_without_empty_bottle: If not nul, defines the max consecutive possible moves without seing an
            empty bottle in the puzzle.
            To be used for more human likely solution finding.
        verbose_cycle: If not nul, periodical trace (in seconds) of the current solving situation.
            To be used in case of long computations.
        """
        time_start = time.time()
        next_time_verbose: float = verbose_cycle

        # List of Puzzles to do
        # The first item in this list is the initial puzzle to solve which has no previous puzzle.
        self.puzzle_chains_todo: collections.deque[PuzzleChain] = collections.deque()
        self.puzzle_chains_todo.append(
            PuzzleChain(
                previous_puzzle_chain=None, puzzle=self.puzzle, message="Puzzle:"
            )
        )

        # List of puzzles that have been computed (empty at the begining)
        self.puzzle_chains_done: collections.deque[PuzzleChain] = collections.deque()

        # Examination loop
        nb_loops: int = 0
        nb_dropped_puzzles: int = 0

        while len(self.puzzle_chains_todo):
            nb_loops += 1
            current_time = time.time() - time_start

            # Verbosity ?
            if verbose_cycle and current_time > next_time_verbose:
                next_time_verbose += verbose_cycle
                nb_done = len(self.puzzle_chains_done)
                nb_todo = len(self.puzzle_chains_todo)
                time_todo = self.estimated_time(nb_todo, nb_done, current_time)
                if nb_done + nb_todo > 0:
                    print(
                        f"Computation after {self.str_second(current_time)}: loops=#{nb_loops}, todo={nb_todo}, "
                        f"done={nb_done}, ratio done/todo={(100 *nb_done) / (nb_done + nb_todo):.1f}%, "
                        f"dropped={nb_dropped_puzzles}, "
                        f"solution in {self.str_second(time_todo)}..."
                    )

            # Next puzzle in the todo list
            p = self.puzzle_chains_todo.pop()

            # Drop it if too many moves without an empty bottle
            if (
                nb_chains_without_empty_bottle
                and p.nb_chains_without_empty_bottle >= nb_chains_without_empty_bottle
            ):
                nb_dropped_puzzles += 1
                continue

            # Compute this puzzle
            if (ret := self._explore_a_puzzle_chain(p)) is not None:
                return ret  # Solution found

        # No more puzzle in the todo list
        return None  # No solution

    def _explore_a_puzzle_chain(
        self, puzzle_chain: PuzzleChain
    ) -> Optional[PuzzleChain]:
        """Considering all possible moves from puzzle in this PuzzleChain."""
        if self.is_puzzle_already_done(puzzle_chain.puzzle):
            return None
        self.puzzle_chains_done.append(puzzle_chain)
        return self._generate_puzzle_chains_todo_from(puzzle_chain)

    def is_puzzle_already_done(self, puzzle: Puzzle) -> bool:
        """Return True if a similar puzzle is already in the done list"""
        for puzzle_chain in self.puzzle_chains_done:
            if puzzle.is_same_as(puzzle_chain.puzzle):
                return True
        return False

    def _generate_puzzle_chains_todo_from(
        self, puzzle_chain: PuzzleChain
    ) -> Optional[PuzzleChain]:
        """Add all interesting possible moves from the puzzle in this PuzzleChain in the todo queue."""
        puzzle: Puzzle = puzzle_chain.puzzle

        # Consider every 2-bottles permutations in the puzzle
        for (i_source, i_destination) in permutations(range(len(puzzle)), 2):
            bottle_source: Bottle = puzzle[i_source]
            bottle_destination: Bottle = puzzle[i_destination]

            if bottle_source.is_interesting_to_pour_into(bottle_destination):
                # Create a copy for this new possible intereting move
                new_puzzle = puzzle.clone()
                bottle_source = new_puzzle[i_source]
                bottle_destination = new_puzzle[i_destination]
                bottle_source.pour_into(bottle_destination)
                new_puzzle_chain = PuzzleChain(
                    previous_puzzle_chain=puzzle_chain,
                    puzzle=new_puzzle,
                    message=f"Pour #{i_source + 1} into #{i_destination + 1}",
                )
                self.puzzle_chains_todo.append(new_puzzle_chain)
                if new_puzzle.is_done:
                    return new_puzzle_chain
        return None


def solve_generic(
    puzzle: Puzzle, nb_chains_without_empty_bottle: int = 0, verbose_cycle: float = 0
) -> None:
    """Generic function for a puzzle solving and result printing."""

    solver: PuzzleSolver = PuzzleSolver(puzzle)

    time_start = time.time()
    solution: Optional[PuzzleChain] = solver.solve(
        nb_chains_without_empty_bottle=nb_chains_without_empty_bottle,
        verbose_cycle=verbose_cycle,
    )
    time_solving = time.time() - time_start

    if solution:
        print(f"Solution ({time_solving:.3f} secs):")
        print(solution.show_puzzle_chains())
    else:
        print(f"No solution: {puzzle}\n")


def main():
    """Some puzzles solving for test/validation purpose."""

    def solve_puzzle0() -> None:
        """
        Hereafter, bottles are defined using strings.
        Every chars in the string is a color for one dose in a bottle (from bottom to top).

        Example:
            {"AABB", "BBAA", ""} is for a puzzle hodling 3 bottles:
            The first bottle "AABB" contains 2 doses of color 'A' and 2 doses of color 'B' on top.
            The next bottle "BBAA" contains the revert.
            The last bottle of the puzzle is empty.
        """

        puzzles = [
            ["AABB", "BBAA", ""],
            ["AABC", "BCCA", "ABBC", ""],
        ]

        for str_puzzle in puzzles:
            puzzle: Puzzle = Puzzle()
            for str_bottle in str_puzzle:
                bottle: Bottle = Bottle(str_bottle)
                puzzle.add_bottle(bottle)
            solve_generic(puzzle)

    # Puzzle colors
    GREEN = 0
    PINK = 1
    YELLOW = 2
    DARK_BLUE = 3
    GRAY = 4
    LIGHT_BLUE = 5
    RED = 6
    ORANGE = 7
    VIOLET = 8

    def solve_puzzle29() -> None:
        """
        Puzzle #29 in 'Water Sort Puzzle' (Andoid OS)
        """

        solve_generic(
            Puzzle(
                [
                    Bottle([GREEN, PINK, YELLOW, DARK_BLUE]),
                    Bottle([GRAY, YELLOW, LIGHT_BLUE, LIGHT_BLUE]),
                    Bottle([GRAY, RED, GRAY, RED]),
                    Bottle([GREEN, DARK_BLUE, ORANGE, GREEN]),
                    Bottle([ORANGE, PINK, PINK, ORANGE]),
                    Bottle([YELLOW, VIOLET, GRAY, VIOLET]),
                    Bottle([LIGHT_BLUE, PINK, VIOLET, YELLOW]),
                    Bottle([LIGHT_BLUE, VIOLET, ORANGE, DARK_BLUE]),
                    Bottle([DARK_BLUE, RED, GREEN, RED]),
                    Bottle([]),
                    Bottle([]),
                ]
            ),
            nb_chains_without_empty_bottle=4,
            verbose_cycle=10,
        )

    def solve_puzzle37() -> None:
        """
        Puzzle #37 in 'Water Sort Puzzle' (Andoid OS)
        """

        solve_generic(
            Puzzle(
                [
                    Bottle([PINK, LIGHT_BLUE, RED, ORANGE]),
                    Bottle([VIOLET, GREEN, GRAY, DARK_BLUE]),
                    Bottle([ORANGE, GRAY, RED, VIOLET]),
                    Bottle([DARK_BLUE, LIGHT_BLUE, LIGHT_BLUE, RED]),
                    Bottle([PINK, LIGHT_BLUE, GREEN, PINK]),
                    Bottle([VIOLET, YELLOW, GREEN, GREEN]),
                    Bottle([DARK_BLUE, ORANGE, YELLOW, GRAY]),
                    Bottle([YELLOW, PINK, ORANGE, VIOLET]),
                    Bottle([GRAY, YELLOW, DARK_BLUE, RED]),
                    Bottle([]),
                    Bottle([]),
                ]
            ),
            nb_chains_without_empty_bottle=4,
            verbose_cycle=10,
        )

    # Résolution des puzzles
    solve_puzzle0()
    solve_puzzle29()
    solve_puzzle37()


if __name__ == "__main__":

    main()
