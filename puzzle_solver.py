#! coding:utf-8

# Import pour pouvoir faire du typing :PuzzleChain dans la classe PuzzleChain
from __future__ import annotations

from itertools import permutations
import queue
import time
import math

from typing import List

from eprouvette import Eprouvette
from puzzle import Puzzle


class PuzzleChain:
    """
    Un puzzle chain permet de chaîner les puzzles entre un previous_puzzle (précédent) qui peut
    se transformer en un puzzle
    """

    __slots__ = "previous_puzzle_chain", "puzzle", "message", "nb_chains_sans_vide"

    def __init__(
        self, previous_puzzle_chain: PuzzleChain | None, puzzle: Puzzle, message: str
    ) -> None:
        """
        PuzzleChain contenant le puzzle précédent ou None pour le 1e
        Puzzle courant de la chaîne
        Message indiquant la construction du puzzle courant depuis le précédent
        """
        self.previous_puzzle_chain = previous_puzzle_chain
        self.puzzle = puzzle
        self.message = message

        # Nombre de PuzzleChain qui se suivent sans que le puzzle contienne au moins une éprouvetee vide
        if previous_puzzle_chain is None:
            self.nb_chains_sans_vide = 0
        elif puzzle.contains_eprouvette_vide():
            self.nb_chains_sans_vide = 0
        else:
            self.nb_chains_sans_vide = previous_puzzle_chain.nb_chains_sans_vide + 1

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

    @staticmethod
    def estimated_time(nb_todo: int, nb_done: int, time_done: float) -> float:
        """
        @return temps estimé pour calculer nb_todo sachant que le temps pour nb_done est time_done
        On considère ici qu'on est dans un modèle exponentiel : t = math.exp(a * nb)
        """
        try:
            a: float = math.log(time_done) / nb_done
            total_time = math.exp(a * (nb_done + nb_todo))
            return total_time - time_done
        except (ValueError, ZeroDivisionError, OverflowError):
            return 0

    def solve(
        self, nb_chains_sans_vide: int = 0, verbose_cycle: float = 0.0
    ) -> PuzzleChain | None:
        """
        Résout le puzzle.
        nb_chains_sans_vide : Si non nul, nombre max de mouvements consécutifs sans constater une éprouvette vide.
        verbose_cycle : Si non nul, trace périodique (en secondes) de l'état d'avancement
        """
        # Liste des puzzles à examiner
        # On initialise cette liste avec le puzzle d'origine qui n'a pas de prédécesseur
        time_start = time.time()
        next_time_verbose: float = verbose_cycle
        self.puzzle_chains_todo: queue.SimpleQueue[PuzzleChain] = queue.SimpleQueue()
        self.puzzle_chains_todo.put(
            PuzzleChain(
                previous_puzzle_chain=None, puzzle=self.puzzle, message="Puzzle initial"
            )
        )
        # Liste des puzzles déjà examinés (vide au début de la résolution)
        self.puzzle_chains_done: List[PuzzleChain] = []
        nb_loops: int = 0
        nb_dropped_puzzles: int = 0
        while not self.puzzle_chains_todo.empty():
            nb_loops += 1
            current_time = time.time() - time_start
            if verbose_cycle and current_time > next_time_verbose:
                next_time_verbose += verbose_cycle
                nb_done = len(self.puzzle_chains_done)
                time_per_done: float = 0
                if nb_done > 0:
                    time_per_done = current_time / nb_done
                nb_todo = self.puzzle_chains_todo.qsize()
                time_todo = self.estimated_time(nb_todo, nb_done, current_time)
                if nb_done + nb_todo > 0:
                    print(
                        f"Solving after {self.str_second(current_time)}: loops=#{nb_loops}, todo={nb_todo}, "
                        f"done={nb_done}, ratio done/todo={(100 *nb_done) / (nb_done + nb_todo):.1f}%, "
                        f"dropped={nb_dropped_puzzles}, "
                        f"solution in {self.str_second(time_todo)}..."
                    )
            p = self.puzzle_chains_todo.get()
            if nb_chains_sans_vide and p.nb_chains_sans_vide >= nb_chains_sans_vide:
                nb_dropped_puzzles += 1
                continue
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

    def solve_generic(
        puzzle: Puzzle, nb_chains_sans_vide: int = 0, verbose_cycle: float = 0
    ) -> None:
        solver: PuzzleSolver = PuzzleSolver(puzzle)

        time_start = time.time()
        solution: PuzzleChain | None = solver.solve(
            nb_chains_sans_vide=nb_chains_sans_vide, verbose_cycle=verbose_cycle
        )
        time_solving = time.time() - time_start

        if solution:
            print(f"Solution (en {time_solving:.3f} secs) :")
            print(solution.show_puzzle_chains())
        else:
            print(f"Non résolu : {puzzle}\n")

    def solve_puzzle0() -> None:
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
            solve_generic(puzzle)

    # Couleurs des puzzles
    VERT = 0
    ROSE = 1
    JAUNE = 2
    BLEU_FONCE = 3
    GRIS = 4
    BLEU_CLAIR = 5
    ROUGE = 6
    ORANGE = 7
    VIOLET = 8

    def solve_puzzle29() -> None:
        """
        Puzzle #29 du jeu 'Water Sort Puzzle' sur Andoid OS
        Voir 'solve_puzzle2 output.txt' pour le résultat'
        """

        solve_generic(
            Puzzle(
                [
                    Eprouvette([VERT, ROSE, JAUNE, BLEU_FONCE]),
                    Eprouvette([GRIS, JAUNE, BLEU_CLAIR, BLEU_CLAIR]),
                    Eprouvette([GRIS, ROUGE, GRIS, ROUGE]),
                    Eprouvette([VERT, BLEU_FONCE, ORANGE, VERT]),
                    Eprouvette([ORANGE, ROSE, ROSE, ORANGE]),
                    Eprouvette([JAUNE, VIOLET, GRIS, VIOLET]),
                    Eprouvette([BLEU_CLAIR, ROSE, VIOLET, JAUNE]),
                    Eprouvette([BLEU_CLAIR, VIOLET, ORANGE, BLEU_FONCE]),
                    Eprouvette([BLEU_FONCE, ROUGE, VERT, ROUGE]),
                    Eprouvette([]),
                    Eprouvette([]),
                ]
            ),
            nb_chains_sans_vide=4,
            verbose_cycle=10,
        )

    def solve_puzzle37() -> None:
        """
        Puzzle #37 du jeu 'Water Sort Puzzle' sur Andoid OS
        Voir 'solve_puzzle2 output.txt' pour le résultat'
        """

        solve_generic(
            Puzzle(
                [
                    Eprouvette([ROSE, BLEU_CLAIR, ROUGE, ORANGE]),
                    Eprouvette([VIOLET, VERT, GRIS, BLEU_FONCE]),
                    Eprouvette([ORANGE, GRIS, ROUGE, VIOLET]),
                    Eprouvette([BLEU_FONCE, BLEU_CLAIR, BLEU_CLAIR, ROUGE]),
                    Eprouvette([ROSE, BLEU_CLAIR, VERT, ROSE]),
                    Eprouvette([VIOLET, JAUNE, VERT, VERT]),
                    Eprouvette([BLEU_FONCE, ORANGE, JAUNE, GRIS]),
                    Eprouvette([JAUNE, ROSE, ORANGE, VIOLET]),
                    Eprouvette([GRIS, JAUNE, BLEU_FONCE, ROUGE]),
                    Eprouvette([]),
                    Eprouvette([]),
                ]
            ),
            nb_chains_sans_vide=5,
            verbose_cycle=10,
        )

    # Résolution des puzzles
    # solve_puzzle0()
    solve_puzzle29()
    # solve_puzzle37()
