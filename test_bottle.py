#: coding:utf-8

import pytest

from bottle import Bottle, BottleError


def test_bottle_rr():
    e = Bottle(["R", "R"])
    assert e.nb_different_colors == 1
    assert e.colors == {"R"}
    assert e.nb_doses == 2
    assert e.top_color == "R"
    assert e.doses[0] == "R"
    assert e.doses[1] == "R"
    assert e.doses[2] is None
    assert e.doses[3] is None


def test_bottle_abc():
    e = Bottle(["A", "B", "C"])
    assert e.nb_different_colors == 3
    assert e.colors == {"A", "B", "C"}
    assert e.nb_doses == 3
    assert e.top_color == "C"
    assert e.doses[0] == "A"
    assert e.doses[1] == "B"
    assert e.doses[2] == "C"
    assert e.doses[3] is None


def test_bottle_iterable():
    e = Bottle(["A", "B", "C"])
    s = ""
    for dose in e.iter_doses():
        s += dose
    assert s == "ABC"


def test_bottle_is_full():
    # This test is valid only with 4 doses bottles
    assert Bottle.MAX_DOSES == 4

    e = Bottle(["A", "B", "B", "C"])
    assert e.is_full


def test_bottle_pop():
    e = Bottle(["A", "B", "B", "C"])
    assert e.nb_doses == 4

    c = e.pop_dose()
    assert c == "C"
    assert e.nb_different_colors == 2
    assert e.nb_doses == 3
    assert e.top_color == "B"

    c = e.pop_dose()
    assert c == "B"
    assert e.nb_different_colors == 2
    assert e.nb_doses == 2
    assert e.top_color == "B"

    c = e.pop_dose()
    assert c == "B"
    assert e.nb_different_colors == 1
    assert e.nb_doses == 1
    assert e.top_color == "A"

    c = e.pop_dose()
    assert c == "A"
    assert e.nb_different_colors == 0
    assert e.nb_doses == 0
    assert e.top_color is None
    assert e.is_empty

    with pytest.raises(BottleError):
        e.pop_dose()


def test_bottle_push():
    e = Bottle(["A"])

    assert e.can_push_dose("A")
    e.push_dose("A")
    assert e.nb_different_colors == 1
    assert e.nb_doses == 2
    assert e.top_color == "A"

    assert not e.can_push_dose("B")
    with pytest.raises(BottleError):
        e.push_dose("B")

    assert not e.can_push_dose(None)
    with pytest.raises(BottleError):
        e.push_dose(None)


def test_bottle_push_overflow():
    list_colors = ["A" for _ in range(Bottle.MAX_DOSES)]
    e = Bottle(list_colors)
    assert e.is_full
    with pytest.raises(BottleError):
        e.push_dose("A")


@pytest.mark.parametrize(
    "source, destination, expected",
    [
        ("", "", False),
        ("", "A", False),
        ("A", "", False),  # False because result would be the same
        ("A", "B", False),
        ("A", "A", True),
        ("A", "AAAA", False),  # False because destination is full
        ("A", "BA", True),
        ("BA", "", True),
        ("BA", "A", True),
        ("AA", "", False),  # False because result would be the same
        ("AA", "B", False),
        ("AA", "AB", False),
        ("AA", "BA", True),
        ("AA", "A", True),
        ("BAA", "A", True),
        ("AA", "AA", True),
    ],
)
def test_bottle_is_interesting_to_pour_into(source, destination, expected):

    # This test is valid only with 4 doses bottles
    assert Bottle.MAX_DOSES == 4

    e_source = Bottle(source)
    e_destination = Bottle(destination)
    if expected:
        assert e_source.is_interesting_to_pour_into(e_destination)
    else:
        assert not e_source.is_interesting_to_pour_into(e_destination)


@pytest.mark.parametrize(
    "source, destination, possible, nb_doses",
    [
        ("", "", False, -1),
        ("A", "", True, 1),
        ("A", "B", False, -1),
        ("A", "A", True, 1),
        ("AA", "A", True, 2),
        ("AA", "AA", True, 2),
        ("AAA", "A", True, 3),
        ("A", "AAAA", False, -1),
        ("BBA", "A", True, 1),
        ("BBAA", "BA", True, 2),
        ("BBAA", "BB", False, -1),
    ],
)
def test_bottle_pouring_into(source, destination, possible, nb_doses):

    # This test is valid only with 4 doses bottles
    assert Bottle.MAX_DOSES == 4

    e_source = Bottle(source)
    e_destination = Bottle(destination)

    len_source_before = e_source.nb_doses
    len_destination_before = e_destination.nb_doses

    if possible:
        assert e_source.is_possible_to_pour_one_dose_into(e_destination)
        effective_nb_doses = e_source.pour_into(e_destination)
        assert effective_nb_doses == nb_doses
        assert len_source_before - nb_doses == e_source.nb_doses
        assert len_destination_before + nb_doses == e_destination.nb_doses
    else:
        assert not e_source.is_possible_to_pour_one_dose_into(e_destination)


@pytest.mark.parametrize(
    "content0, content1, is_same",
    [
        ("", "", True),
        ("", "A", False),
        ("A", "", False),
        ("A", "A", True),
        ("A", "AB", False),
        ("A", "B", False),
        ("ABC", "A", False),
        ("ABC", "AB", False),
        ("ABC", "ABB", False),
        ("ABC", "ABC", True),
        ("ABC", "ABCD", False),
    ],
)
def test_bottle_is_same_as(content0, content1, is_same):

    # This test is valid only with 4 doses bottles
    assert Bottle.MAX_DOSES == 4

    e0 = Bottle(content0)
    assert e0.is_same_as(e0)
    e1 = Bottle(content1)
    assert e1.is_same_as(e1)
    if is_same:
        assert e0.is_same_as(e1)
        assert e1.is_same_as(e0)
    else:
        assert not e0.is_same_as(e1)
        assert not e1.is_same_as(e0)


def test_bottle_clone():
    list_colors = ["A", "B", "C"]
    e = Bottle(list_colors)
    clone_e = e.clone()
    assert e.is_same_as(clone_e)
    for i, dose in enumerate(clone_e.iter_doses()):
        assert list_colors[i] == dose


def test_bottle_repr():
    e = Bottle(["A", "B", "C"])
    e_repr = f"{e}"
    assert "A" in e_repr
    assert "B" in e_repr
    assert "C" in e_repr


if __name__ == "__main__":

    pytest.main()
