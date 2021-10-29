#! coding:utf-8

# Import pour pouvoir faire du typing :PuzzleChain dans la classe PuzzleChain
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
import queue
from typing import List

from eprouvette import Eprouvette
from puzzle import Puzzle


@dataclass
class PuzzleChain:
    """
    Un puzzle chain permet de chaîner les puzzles entre un previous_puzzle (précédent) qui peut
    se transformer en un puzzle
    """

    previous_puzzle_chain: PuzzleChain | None
    puzzle: Puzzle
    message: str

    def show_puzzle_chains(self) -> str:
        """Affiche la liste des puzzles chaînés."""

        # Reconstitue la liste des puzzles (queue)
        q: queue.LifoQueue = queue.LifoQueue()
        q.put(self)
        previous = self.previous_puzzle_chain
        while previous is not None:
            q.put(previous)
            previous = previous.previous_puzzle_chain

        # Reconstitue les étapes de résolution
        ret = ""
        while not q.empty():
            puzzle_chain: PuzzleChain = q.get()
            ret += f"{puzzle_chain.message}:\n  {puzzle_chain.puzzle}\n"
        return ret


class PuzzleSolver:
    """
    Un puzzle solver permet la résolution d'un puzzle.

    La résolution se fait en explorant toutes les combinaisons possibles depuis chaque situation.
    La situation initiale étant le puzzle d'origine.
    """

    def __init__(self, puzzle: Puzzle) -> None:
        if not puzzle.is_consistant:
            raise ValueError(f"Puzzle inconsistant : {puzzle}")
        self.puzzle: Puzzle = puzzle.clone()

    def solve(self) -> PuzzleChain | None:
        """Résout le puzzle."""
        # Liste des puzzles à examiner
        # On initialise cette liste avec le puzzle d'origine qui n'a pas de prédécesseur
        self.puzzle_chains_todo: queue.SimpleQueue[PuzzleChain] = queue.SimpleQueue()
        self.puzzle_chains_todo.put(
            PuzzleChain(
                previous_puzzle_chain=None, puzzle=self.puzzle, message="Puzzle initial"
            )
        )
        # Liste des puzzles déjà examinés (vide au début de la résolution)
        self.puzzle_chains_done: List[PuzzleChain] = []
        while not self.puzzle_chains_todo.empty():
            p = self.puzzle_chains_todo.get()
            if (ret := self._explore_puzzle_chain(p)) is not None:
                return ret  # Solution found
        return None  # No solution

    def _explore_puzzle_chain(self, puzzle_chain: PuzzleChain) -> PuzzleChain | None:
        """Explore les combinaisons depuis un puzzle."""
        if self.is_puzzle_already_done(puzzle_chain.puzzle):
            return None
        self.puzzle_chains_done.append(puzzle_chain)
        return self._generate_puzzle_chains_todo_from(puzzle_chain)

    def is_puzzle_already_done(self, puzzle: Puzzle) -> bool:
        for puzzle_chain in self.puzzle_chains_done:
            if puzzle == puzzle_chain.puzzle:
                return True
        return False

    def _generate_puzzle_chains_todo_from(
        self, puzzle_chain: PuzzleChain
    ) -> PuzzleChain | None:
        """Ajoute tous les puzzles possibles depuis le puzzle de puzzle_chain dans la queue à traiter."""
        puzzle: Puzzle = puzzle_chain.puzzle
        for (i_source, i_destination) in permutations(range(len(puzzle)), 2):
            eprouvette_source: Eprouvette = puzzle[i_source]
            eprouvette_destination: Eprouvette = puzzle[i_destination]
            if eprouvette_source.is_possible_verser_une_dose_dans(
                eprouvette_destination
            ):
                new_puzzle = puzzle.clone()
                eprouvette_source = new_puzzle[i_source]
                eprouvette_destination = new_puzzle[i_destination]
                eprouvette_source.verser_dans(eprouvette_destination)
                new_puzzle_chain = PuzzleChain(
                    previous_puzzle_chain=puzzle_chain,
                    puzzle=new_puzzle,
                    message=f"Verser #{i_source + 1} dans #{i_destination + 1}",
                )
                self.puzzle_chains_todo.put(new_puzzle_chain)
                if new_puzzle.is_done:
                    return new_puzzle_chain
        return None


if __name__ == "__main__":

    """
    Ici, chaque puzzle est représenté par une séquence de chaînes de caractères.
    Chaque lettre d'une chaîne de caractère représente une dose d'un liquide identifié par la lettre.

    Par exemple:
        {"AABB", "BBAA", ""}
        représente un puzzle avec 3 éprouvettes.
        Dans la première éprouvette "AABB", on a 2 doses de liquide 'A' et 2 doses de liquide 'B' au dessus.
        La deuxième éprouvette "BBAA" contient l'inverse.
        La troisième et dernière éprouvette du puzzle est vide ""
    """

    puzzles = [
        ["AABB", "BBAA", ""],
        ["AABC", "BCCA", "ABBC", ""],
    ]

    for str_puzzle in puzzles:
        puzzle: Puzzle = Puzzle()
        for str_eprouvette in str_puzzle:
            eprouvette: Eprouvette = Eprouvette(str_eprouvette)
            puzzle.add_eprouvette(eprouvette)

        solver: PuzzleSolver = PuzzleSolver(puzzle)
        solution: PuzzleChain | None = solver.solve()

        if solution:
            print("Solution :")
            print(solution.show_puzzle_chains())
        else:
            print(f"Non résolu : {puzzle}\n")
