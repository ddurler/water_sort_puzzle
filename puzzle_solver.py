#! coding:utf-8

# Import pour pouvoir faire du typing :PuzzleChain dans la classe PuzzleChain
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
import queue
import time

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

    @staticmethod
    def str_second(sec: float) -> str:
        """Convertion d'une durée en secondes en une chaîne heure + minute + seconde."""
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

    def solve(self, verbose=False) -> PuzzleChain | None:
        """Résout le puzzle."""
        # Liste des puzzles à examiner
        # On initialise cette liste avec le puzzle d'origine qui n'a pas de prédécesseur
        time_start = time.time()
        self.puzzle_chains_todo: queue.SimpleQueue[PuzzleChain] = queue.SimpleQueue()
        self.puzzle_chains_todo.put(
            PuzzleChain(
                previous_puzzle_chain=None, puzzle=self.puzzle, message="Puzzle initial"
            )
        )
        # Liste des puzzles déjà examinés (vide au début de la résolution)
        self.puzzle_chains_done: List[PuzzleChain] = []
        nb_loops = 0
        while not self.puzzle_chains_todo.empty():
            nb_loops += 1
            if verbose and nb_loops % 25 == 0:
                current_time = time.time() - time_start
                nb_done = len(self.puzzle_chains_done)
                time_per_done: float = 0
                if nb_done > 0:
                    time_per_done = current_time / nb_done
                nb_todo = self.puzzle_chains_todo.qsize()
                time_todo = nb_todo * time_per_done
                if nb_done + nb_todo > 0:
                    print(
                        f"Solving after {self.str_second(current_time)}: loops=#{nb_loops}, todo={nb_todo}, "
                        f"done={nb_done}, ratio done/todo={(100 *nb_done) / (nb_done + nb_todo):.1f}%, "
                        f"solution in {self.str_second(time_todo)}..."
                    )
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
            if puzzle.is_same_as(puzzle_chain.puzzle):
                return True
        return False

    def _generate_puzzle_chains_todo_from(
        self, puzzle_chain: PuzzleChain
    ) -> PuzzleChain | None:
        """Ajoute tous les puzzles interessants depuis le puzzle de puzzle_chain dans la queue à traiter."""
        puzzle: Puzzle = puzzle_chain.puzzle
        for (i_source, i_destination) in permutations(range(len(puzzle)), 2):
            eprouvette_source: Eprouvette = puzzle[i_source]
            eprouvette_destination: Eprouvette = puzzle[i_destination]
            if eprouvette_source.is_interessant_verser_dans(eprouvette_destination):
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

    def solve_generic(puzzle: Puzzle, verbose=False):
        solver: PuzzleSolver = PuzzleSolver(puzzle)

        time_start = time.time()
        solution: PuzzleChain | None = solver.solve(verbose=verbose)
        time_solving = time.time() - time_start

        if solution:
            print(f"Solution (en {time_solving:.3f} secs) :")
            print(solution.show_puzzle_chains())
        else:
            print(f"Non résolu : {puzzle}\n")

    def solve_puzzle1():
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
            solve_generic((puzzle))

    def solve_puzzle2():
        """
        Puzzle #29 du jeu 'Water Sort Puzzle' sur Andoid OS
        Voir 'solve_puzzle2 output.txt' pour le résultat'
        """
        VERT = 0
        ROSE = 1
        JAUNE = 2
        GRIS_FONCE = 4
        GRIS = 5
        BLEU_CLAIR = 6
        ROUGE = 7
        ORANGE = 8
        VIOLET = 9

        solve_generic(
            Puzzle(
                [
                    Eprouvette([VERT, ROSE, JAUNE, GRIS_FONCE]),
                    Eprouvette([GRIS, JAUNE, BLEU_CLAIR, BLEU_CLAIR]),
                    Eprouvette([GRIS, ROUGE, GRIS, ROUGE]),
                    Eprouvette([VERT, GRIS_FONCE, ORANGE, VERT]),
                    Eprouvette([ORANGE, ROSE, ROSE, ORANGE]),
                    Eprouvette([JAUNE, VIOLET, GRIS, VIOLET]),
                    Eprouvette([BLEU_CLAIR, ROSE, VIOLET, JAUNE]),
                    Eprouvette([BLEU_CLAIR, VIOLET, ORANGE, GRIS_FONCE]),
                    Eprouvette([GRIS_FONCE, ROUGE, VERT, ROUGE]),
                    Eprouvette([]),
                    Eprouvette([]),
                ]
            ),
            verbose=True,
        )

    # Main
    solve_puzzle1()
    solve_puzzle2()
