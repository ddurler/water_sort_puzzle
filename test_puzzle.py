#: coding:utf-8

import pytest

from bottle import Bottle
from puzzle import Puzzle


def test_puzzle():
    p = Puzzle([Bottle(["R", "R"]), Bottle(["R"])])
    p.add_bottle(Bottle(["R"]))


def test_puzzle_len():
    p = Puzzle()
    assert len(p) == 0
    p.add_bottle(Bottle(["R"]))
    assert len(p) == 1


def test_puzzle_items():
    e_0 = Bottle(["A"])
    e_1 = Bottle(["B"])
    e_2 = Bottle(["C"])
    p = Puzzle([e_0, e_1, e_2])
    assert p[0] == e_0
    assert p[1] == e_1
    assert p[2] == e_2


def test_puzzle_repr():
    p = Puzzle([Bottle(["A", "B"]), Bottle(["C"])])
    puzzle_repr = f"{p}"
    assert "A" in puzzle_repr
    assert "B" in puzzle_repr
    assert "C" in puzzle_repr


@pytest.mark.parametrize(
    "content0, content1, same",
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
def test_puzzle_is_same_as(content0, content1, same):

    assert not Puzzle().is_same_as("Objet_that_is_not_a_puzzle")

    p0 = Puzzle()
    for list_colors in content0:
        e = Bottle(list_colors)
        p0.add_bottle(e)

    p1 = Puzzle()
    for list_colors in content1:
        e = Bottle(list_colors)
        p1.add_bottle(e)

    if same:
        assert p0.is_same_as(p1)
        assert p1.is_same_as(p0)
    else:
        assert not p0.is_same_as(p1)
        assert not p1.is_same_as(p0)


def test_puzzle_clone():
    p = Puzzle([Bottle(["A", "A"]), Bottle(["B"])])
    p2 = p.clone()
    assert p.is_same_as(p2)


def test_puzzle_permutations():
    e_a = Bottle(["A"])
    e_b = Bottle(["B"])
    e_c = Bottle(["C"])
    p = Puzzle([e_a, e_b, e_c])
    permutations = [perm for perm in p.iter_permutations()]
    assert len(permutations) == 6
    assert (e_a, e_b) in permutations
    assert (e_a, e_c) in permutations
    assert (e_b, e_a) in permutations
    assert (e_b, e_c) in permutations
    assert (e_c, e_a) in permutations
    assert (e_c, e_b) in permutations


def test_puzzle_is_consistent_full_dose():
    p = Puzzle()
    for nb_doses in range(Bottle.MAX_DOSES):
        p.add_bottle(Bottle(["A"]))
        if nb_doses == Bottle.MAX_DOSES - 1:
            assert p.is_consistent
        else:
            assert not p.is_consistent


def test_puzzle_is_consistent_empty_dose():
    list_colors = ["A" for _ in range(Bottle.MAX_DOSES)]
    e = Bottle(list_colors)
    p = Puzzle([e])
    assert not p.is_consistent


@pytest.mark.parametrize(
    "content, done",
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
def test_puzzle_is_done(content, done):

    # This test is valid only with 4 doses bottles
    assert Bottle.MAX_DOSES == 4

    p = Puzzle()
    for list_strings in content:
        e = Bottle(list_strings)
        p.add_bottle(e)

    if done:
        assert p.is_done
    else:
        assert not p.is_done


def test_puzzle_contains_empty_bottle():

    p = Puzzle()
    assert not p.contains_empty_bottle()

    p.add_bottle(Bottle("ABC"))
    assert not p.contains_empty_bottle()

    p.add_bottle(Bottle(""))
    assert p.contains_empty_bottle()


if __name__ == "__main__":

    pytest.main()
