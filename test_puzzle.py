#: coding:utf-8

import pytest

from eprouvette import Eprouvette
from puzzle import Puzzle


def test_puzzle():
    p = Puzzle([Eprouvette(["R", "R"]), Eprouvette(["R"])])
    p.add_eprouvette(Eprouvette(["R"]))


def test_puzzle_len():
    p = Puzzle()
    assert len(p) == 0
    p.add_eprouvette(Eprouvette(["R"]))
    assert len(p) == 1


def test_puzzle_items():
    e_0 = Eprouvette(["A"])
    e_1 = Eprouvette(["B"])
    e_2 = Eprouvette(["C"])
    p = Puzzle([e_0, e_1, e_2])
    assert p[0] == e_0
    assert p[1] == e_1
    assert p[2] == e_2


def test_puzzle_repr():
    p = Puzzle([Eprouvette(["A", "B"]), Eprouvette(["C"])])
    puzzle_repr = f"{p}"
    assert "A" in puzzle_repr
    assert "B" in puzzle_repr
    assert "C" in puzzle_repr


@pytest.mark.parametrize(
    "contenu0, contenu1, same",
    [
        ([""], [""], True),
        ([""], ["A"], False),
        (["A"], [""], False),
        (["A"], ["A"], True),
        (["A"], ["B"], False),
        (["A"], ["AB", "C"], False),
        (["AB"], ["B"], False),
        (["AB", "B"], ["AB", "B"], True),
        (["AB", "B"], ["B", "AB"], True),
        (["", "AB", "B"], ["B", "", "AB"], True),
    ],
)
def test_puzzle_is_same_as(contenu0, contenu1, same):

    assert not Puzzle().is_same_as("Objet_qui_n_est_pas_un_puzzle")

    p0 = Puzzle()
    for list_liquide in contenu0:
        e = Eprouvette(list_liquide)
        p0.add_eprouvette(e)

    p1 = Puzzle()
    for list_liquide in contenu1:
        e = Eprouvette(list_liquide)
        p1.add_eprouvette(e)

    if same:
        assert p0.is_same_as(p1)
        assert p1.is_same_as(p0)
    else:
        assert not p0.is_same_as(p1)
        assert not p1.is_same_as(p0)


def test_puzzle_clone():
    p = Puzzle([Eprouvette(["A", "A"]), Eprouvette(["B"])])
    p2 = p.clone()
    assert p.is_same_as(p2)


def test_puzzle_permutations():
    e_a = Eprouvette(["A"])
    e_b = Eprouvette(["B"])
    e_c = Eprouvette(["C"])
    p = Puzzle([e_a, e_b, e_c])
    permutations = [perm for perm in p.iter_permutations()]
    assert len(permutations) == 6
    assert (e_a, e_b) in permutations
    assert (e_a, e_c) in permutations
    assert (e_b, e_a) in permutations
    assert (e_b, e_c) in permutations
    assert (e_c, e_a) in permutations
    assert (e_c, e_b) in permutations


def test_puzzle_is_consistant_nb_doses_liquide():
    p = Puzzle()
    for nb_doses in range(Eprouvette.MAX_DOSES):
        p.add_eprouvette(Eprouvette(["A"]))
        if nb_doses == Eprouvette.MAX_DOSES - 1:
            assert p.is_consistant
        else:
            assert not p.is_consistant


def test_puzzle_is_consistant_nb_doses_vides():
    list_liquides = ["A" for _ in range(Eprouvette.MAX_DOSES)]
    e = Eprouvette(list_liquides)
    p = Puzzle([e])
    assert not p.is_consistant


@pytest.mark.parametrize(
    "contenu, done",
    [
        ([""], True),
        (["A"], False),
        (["AA"], False),
        (["AAA"], False),
        (["AAAA"], True),
        (["AABB"], False),
        (["AAAA", ""], True),
        (["AAAA", "AABB"], False),
        (["AAAA", "AABB"], False),
        (["AAAA", "BBBB", ""], True),
    ],
)
def test_puzzle_is_done(contenu, done):

    # Ce test est prévu pour des éprouvettes de 4 doses
    assert Eprouvette.MAX_DOSES == 4

    p = Puzzle()
    for list_strings in contenu:
        e = Eprouvette(list_strings)
        p.add_eprouvette(e)

    if done:
        assert p.is_done
    else:
        assert not p.is_done


def test_puzzle_contains_eprouvette_vide():

    p = Puzzle()
    assert not p.contains_eprouvette_vide()

    p.add_eprouvette(Eprouvette("ABC"))
    assert not p.contains_eprouvette_vide()

    p.add_eprouvette(Eprouvette(""))
    assert p.contains_eprouvette_vide()


if __name__ == "__main__":

    pytest.main()
