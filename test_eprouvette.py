#: coding:utf-8

import pytest

from eprouvette import Eprouvette, EprouvetteError


def test_epouvette_rr():
    e = Eprouvette(["R", "R"])
    assert e.nb_different_liquides == 1
    assert e.liquides == {"R"}
    assert e.nb_doses == 2
    assert e.top_liquide == "R"
    assert e.doses[0] == "R"
    assert e.doses[1] == "R"
    assert e.doses[2] is None
    assert e.doses[3] is None


def test_epouvette_abc():
    e = Eprouvette(["A", "B", "C"])
    assert e.nb_different_liquides == 3
    assert e.liquides == {"A", "B", "C"}
    assert e.nb_doses == 3
    assert e.top_liquide == "C"
    assert e.doses[0] == "A"
    assert e.doses[1] == "B"
    assert e.doses[2] == "C"
    assert e.doses[3] is None


def test_eprouvette_iterable():
    e = Eprouvette(["A", "B", "C"])
    s = ""
    for dose in e.iter_doses():
        s += dose
    assert s == "ABC"


def test_eprouvette_is_pleine():
    # This test is valid only with 4 doses bottles
    assert Eprouvette.MAX_DOSES == 4

    e = Eprouvette(["A", "B", "B", "C"])
    assert e.is_pleine


def test_eprouvette_pop():
    e = Eprouvette(["A", "B", "B", "C"])
    assert e.nb_doses == 4

    c = e.pop_dose()
    assert c == "C"
    assert e.nb_different_liquides == 2
    assert e.nb_doses == 3
    assert e.top_liquide == "B"

    c = e.pop_dose()
    assert c == "B"
    assert e.nb_different_liquides == 2
    assert e.nb_doses == 2
    assert e.top_liquide == "B"

    c = e.pop_dose()
    assert c == "B"
    assert e.nb_different_liquides == 1
    assert e.nb_doses == 1
    assert e.top_liquide == "A"

    c = e.pop_dose()
    assert c == "A"
    assert e.nb_different_liquides == 0
    assert e.nb_doses == 0
    assert e.top_liquide is None
    assert e.is_vide

    with pytest.raises(EprouvetteError):
        e.pop_dose()


def test_eprouvette_push():
    e = Eprouvette(["A"])

    assert e.can_push_dose("A")
    e.push_dose("A")
    assert e.nb_different_liquides == 1
    assert e.nb_doses == 2
    assert e.top_liquide == "A"

    assert not e.can_push_dose("B")
    with pytest.raises(EprouvetteError):
        e.push_dose("B")

    assert not e.can_push_dose(None)
    with pytest.raises(EprouvetteError):
        e.push_dose(None)


def test_eprouvette_push_overflow():
    list_liquides = ["A" for _ in range(Eprouvette.MAX_DOSES)]
    e = Eprouvette(list_liquides)
    assert e.is_pleine
    with pytest.raises(EprouvetteError):
        e.push_dose("A")


@pytest.mark.parametrize(
    "source, destination, expected",
    [
        ("", "", False),
        ("", "A", False),
        ("A", "", False),  # False car le résultat est symétrique
        ("A", "B", False),
        ("A", "A", True),
        ("A", "AAAA", False),  # False car destination pleine
        ("A", "BA", True),
        ("BA", "", True),
        ("BA", "A", True),
        ("AA", "", False),  # False car le résultat est symétrique
        ("AA", "B", False),
        ("AA", "AB", False),
        ("AA", "BA", True),
        ("AA", "A", True),
        ("BAA", "A", True),
        ("AA", "AA", True),
    ],
)
def test_epourvette_is_interessant_verser_dans(source, destination, expected):

    # Ce test est prévu pour des éprouvettes contenant 4 doses
    assert Eprouvette.MAX_DOSES == 4

    e_source = Eprouvette(source)
    e_destination = Eprouvette(destination)
    if expected:
        assert e_source.is_interessant_verser_dans(e_destination)
    else:
        assert not e_source.is_interessant_verser_dans(e_destination)


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
def test_eprouvette_verser(source, destination, possible, nb_doses):

    # Ce test est prévu pour des éprouvettes contenant 4 doses
    assert Eprouvette.MAX_DOSES == 4

    e_source = Eprouvette(source)
    e_destination = Eprouvette(destination)

    len_source_avant = e_source.nb_doses
    len_destination_avant = e_destination.nb_doses

    if possible:
        assert e_source.is_possible_verser_une_dose_dans(e_destination)
        effective_nb_doses = e_source.verser_dans(e_destination)
        assert effective_nb_doses == nb_doses
        assert len_source_avant - nb_doses == e_source.nb_doses
        assert len_destination_avant + nb_doses == e_destination.nb_doses
    else:
        assert not e_source.is_possible_verser_une_dose_dans(e_destination)


@pytest.mark.parametrize(
    "contenu0, contenu1, is_same",
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
def test_eprouvette_is_same_as(contenu0, contenu1, is_same):

    # Ce test est prévu des éprouvettes contenant 4 doses
    assert Eprouvette.MAX_DOSES == 4

    e0 = Eprouvette(contenu0)
    assert e0.is_same_as(e0)
    e1 = Eprouvette(contenu1)
    assert e1.is_same_as(e1)
    if is_same:
        assert e0.is_same_as(e1)
        assert e1.is_same_as(e0)
    else:
        assert not e0.is_same_as(e1)
        assert not e1.is_same_as(e0)


def test_eprouvette_clone():
    list_liquides = ["A", "B", "C"]
    e = Eprouvette(list_liquides)
    clone_e = e.clone()
    assert e.is_same_as(clone_e)
    for i, dose in enumerate(clone_e.iter_doses()):
        assert list_liquides[i] == dose


def test_eprouvette_repr():
    e = Eprouvette(["A", "B", "C"])
    e_repr = f"{e}"
    assert "A" in e_repr
    assert "B" in e_repr
    assert "C" in e_repr


if __name__ == "__main__":

    pytest.main()
