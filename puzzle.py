#! coding:utf-8

# Import pour pouvoir faire du typing :Puzzle dans la classe Puzzle
from __future__ import annotations

from typing import Any, List, Tuple, Generator
from collections import Counter
from itertools import permutations

from eprouvette import Eprouvette


class Puzzle:
    """
    Un puzzle contient des @see Eprouvette.

    On peut créer le puzzle en indiquant une liste d'éprouvette.
    Par défaut la taille (nombre de doses) des éprouvettes est de 4 mais on peut redéfinir ce nombre pour
    toutes les éprouvettes du puzzle.
    On peut compléter le puzzle avec la méthode @see add_eprouvette

    La propriété @see is_consistant permet de vérifier que le puzzle est consistant par rapport au
    contenu des éprouvettes
    """

    def __init__(
        self, epouvettes: List[Eprouvette] | None = None, eprouvette_max_len: int = 4
    ) -> None:
        self.eprouvette_max_len: int = int(eprouvette_max_len)
        self._eprouvettes: List[Eprouvette] = []
        if epouvettes:
            for eprouvette in epouvettes:
                self.add_eprouvette(eprouvette)
                eprouvette.max_len = eprouvette_max_len

    def add_eprouvette(self, eprouvette: Eprouvette) -> None:
        """Ajoute une éprouvette au puzzle."""
        assert isinstance(eprouvette, Eprouvette)
        eprouvette.max_len = self.eprouvette_max_len
        self._eprouvettes.append(eprouvette)

    def __len__(self) -> int:
        """Implémente l'opération len() pour un puzzle -> Nombre d'éprouvettes du puzzle."""
        return len(self._eprouvettes)

    def __getitem__(self, index: int) -> Eprouvette:
        """i-eme eprouvette du puzzle."""
        return self._eprouvettes[index]

    def __eq__(self, other: object) -> bool:
        """Implémente l'opérateur == entre les puzzles."""
        if not isinstance(other, Puzzle) or len(self) != len(other):
            return False
        for e0, e1 in zip(self, other):
            if e0 != e1:
                return False
        return True

    def is_same_as(self, other: object) -> bool:
        """
        @return True si les 2 puzzles sont similaires
        (mêmes éprouvettes mais pas forcement dans le même ordre).
        @see __equ__ pour une stricte identité.
        """
        if not isinstance(other, Puzzle) or len(self) != len(other):
            return False
        # Table des éprouvettes identifiées idem dans other puzzle
        table: List[bool] = [False for _ in range(len(self))]
        for e0 in self:
            found_in_other = False
            for i, e1 in enumerate(other):
                if not table[i] and e0 == other[i]:
                    table[i] = True
                    found_in_other = True
                    break
            if not found_in_other:
                return False
        return True

    def __iter__(self):
        """Implémente un itérateur sur toutes les éprouvettes du puzzle."""
        return self._eprouvettes.__iter__()

    def iter_permutations(self) -> Generator[Tuple[Any, ...], None, None]:
        """Iterator sur toutes les combinaisons Tuple[Eprouvette, Eprouvette] du puzzle."""
        for permutation in permutations(self, 2):
            yield permutation

    @property
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
            if nb_doses_liquide % self.eprouvette_max_len != 0:
                return False

        # Décompte des doses vides dans les éprouvettes
        nb_doses_vides = 0
        for eprouvette in self:
            nb_doses_vides += self.eprouvette_max_len - len(eprouvette)

        # Vérifie qu'on a au moins le contenu d'une éprouvette vide
        if nb_doses_vides < self.eprouvette_max_len:
            return False

        # Tout est OK
        return True

    @property
    def is_done(self) -> bool:
        """@return True si le puzzle est terminé."""
        eprouvette: Eprouvette
        for eprouvette in self:
            if not (
                eprouvette.is_vide
                or (eprouvette.is_pleine and len(eprouvette.liquides) == 1)
            ):
                return False
        return True

    def clone(self) -> Puzzle:
        """Crée et retourne une copie clone du puzzle."""
        copy_list_eprouvettes: List[Eprouvette] = []
        for eprouvette in self:
            copy_list_eprouvettes.append(eprouvette.clone())

        return Puzzle(copy_list_eprouvettes, eprouvette_max_len=self.eprouvette_max_len)

    def __repr__(self):
        ret = ""
        for n, eprouvette in enumerate(self):
            if ret:
                ret += ", "
            ret += f"#{n + 1}{eprouvette}"
        return f"Puzzle<{ret}>"
