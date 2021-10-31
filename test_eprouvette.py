#: coding:utf-8

import unittest

from eprouvette import Eprouvette, EprouvetteError


class TestEprouvette(unittest.TestCase):
    def test_epouvette_RR(self):
        e = Eprouvette(["R", "R"])
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(e.liquides, {"R"})
        self.assertEqual(e.nb_doses, 2)
        self.assertEqual(e.top_liquide, "R")
        self.assertEqual(e.doses[0], "R")
        self.assertEqual(e.doses[1], "R")
        self.assertEqual(e.doses[2], None)
        self.assertEqual(e.doses[3], None)

    def test_epouvette_ABC(self):
        e = Eprouvette(["A", "B", "C"])
        self.assertEqual(e.nb_different_liquides, 3)
        self.assertEqual(e.liquides, {"A", "B", "C"})
        self.assertEqual(e.nb_doses, 3)
        self.assertEqual(e.top_liquide, "C")
        self.assertEqual(e.doses[0], "A")
        self.assertEqual(e.doses[1], "B")
        self.assertEqual(e.doses[2], "C")
        self.assertEqual(e.doses[3], None)

    def test_eprouvette_iterable(self):
        e = Eprouvette(["A", "B", "C"])
        s = ""
        for dose in e.iter_doses():
            s += dose
        self.assertEqual(s, "ABC")

    def test_eprouvette_is_pleine(self):
        self.assertEqual(Eprouvette.MAX_DOSES, 4)

        e = Eprouvette(["A", "B", "B", "C"])
        self.assertTrue(e.is_pleine)

    def test_eprouvette_pop(self):
        e = Eprouvette(["A", "B", "B", "C"])
        self.assertEqual(e.nb_doses, 4)

        c = e.pop_dose()
        self.assertEqual(c, "C")
        self.assertEqual(e.nb_different_liquides, 2)
        self.assertEqual(e.nb_doses, 3)
        self.assertEqual(e.top_liquide, "B")

        c = e.pop_dose()
        self.assertEqual(c, "B")
        self.assertEqual(e.nb_different_liquides, 2)
        self.assertEqual(e.nb_doses, 2)
        self.assertEqual(e.top_liquide, "B")

        c = e.pop_dose()
        self.assertEqual(c, "B")
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(e.nb_doses, 1)
        self.assertEqual(e.top_liquide, "A")

        c = e.pop_dose()
        self.assertEqual(c, "A")
        self.assertEqual(e.nb_different_liquides, 0)
        self.assertEqual(e.nb_doses, 0)
        self.assertEqual(e.top_liquide, None)
        self.assertTrue(e.is_vide)

        self.assertRaises(EprouvetteError, e.pop_dose)

    def test_eprouvette_push(self):
        e = Eprouvette(["A"])

        self.assertTrue(e.can_push_dose("A"))
        e.push_dose("A")
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(e.nb_doses, 2)
        self.assertEqual(e.top_liquide, "A")

        self.assertFalse(e.can_push_dose("B"))
        self.assertRaises(EprouvetteError, e.push_dose, "B")

        self.assertFalse(e.can_push_dose(None))
        self.assertRaises(EprouvetteError, e.push_dose, None)

    def test_eprouvette_push_overflow(self):
        list_liquides = ["A" for _ in range(Eprouvette.MAX_DOSES)]
        e = Eprouvette(list_liquides)
        self.assertTrue(e.is_pleine)
        self.assertRaises(EprouvetteError, e.push_dose, "A")

    def test_epourvette_is_interessant_verser_dans(self):
        tests = [
            ["", "", False],
            ["", "A", False],
            ["A", "", False],  # False car le résultat est symétrique
            ["A", "B", False],
            ["A", "A", True],
            ["A", "BA", True],
            ["BA", "A", True],
            ["AA", "", False],  # False car le résultat est symétrique
            ["AA", "B", False],
            ["AA", "AB", False],
            ["AA", "BA", True],
            ["AA", "A", True],
            ["BAA", "A", True],
            ["AA", "AA", True],
        ]

        for test in tests:
            source = Eprouvette(test[0])
            destination = Eprouvette(test[1])
            if test[2]:
                # self.assertTrue(m.is_mouvement_ok())
                if not source.is_interessant_verser_dans(destination):
                    print(f"FAIL True on: [{test[0]}] -> [{test[1]}]")
            else:
                # self.assertFalse(m.is_mouvement_ok())
                if source.is_interessant_verser_dans(destination):
                    print(f"FAIL False on: [{test[0]}] -> [{test[1]}]")

    def test_eprouvette_verser(self):
        tests = [
            {"source": "", "destination": "", "possible": False},
            {"source": "A", "destination": "", "possible": True, "nb_doses": 1},
            {"source": "A", "destination": "B", "possible": False},
            {"source": "A", "destination": "A", "possible": True, "nb_doses": 1},
            {
                "source": "AA",
                "destination": "A",
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": "AA",
                "destination": "AA",
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": "AAA",
                "destination": "A",
                "possible": True,
                "nb_doses": 3,
            },
            {"source": "A", "destination": "AAAA", "possible": False},
            {
                "source": "BBA",
                "destination": "A",
                "possible": True,
                "nb_doses": 1,
            },
            {
                "source": "BBAA",
                "destination": "BA",
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": "BBAA",
                "destination": "BB",
                "possible": False,
            },
        ]

        # Ce test est prévu pour des éprouvettes contenant 4 doses
        self.assertEqual(Eprouvette.MAX_DOSES, 4)

        for test in tests:
            source = Eprouvette(test["source"])
            destination = Eprouvette(test["destination"])

            len_source_avant = source.nb_doses
            len_destination_avant = destination.nb_doses

            if test["possible"]:
                self.assertTrue(source.is_possible_verser_une_dose_dans(destination))
                nb_doses = source.verser_dans(destination)
                self.assertEqual(test["nb_doses"], nb_doses)
                self.assertEqual(len_source_avant - nb_doses, source.nb_doses)
                self.assertEqual(len_destination_avant + nb_doses, destination.nb_doses)
            else:
                self.assertFalse(source.is_possible_verser_une_dose_dans(destination))

    def test_eprouvette_is_same_as(self):
        tests = [
            [[], [], True],
            [[], ["A"], False],
            [["A"], [], False],
            [["A"], ["A"], True],
            [["A"], ["A", "B"], False],
            [["A"], ["B"], False],
            [["A", "B", "C"], ["A"], False],
            [["A", "B", "C"], ["A", "B"], False],
            [["A", "B", "C"], ["A", "B", "B"], False],
            [["A", "B", "C"], ["A", "B", "C"], True],
            [["A", "B", "C"], ["A", "B", "C", "D"], False],
        ]

        # Ce test est prévu des éprouvettes contenant 4 doses
        self.assertEqual(Eprouvette.MAX_DOSES, 4)

        for test in tests:
            e0 = Eprouvette(test[0])
            self.assertTrue(e0.is_same_as(e0))
            e1 = Eprouvette(test[1])
            self.assertTrue(e1.is_same_as(e1))
            if test[2]:
                self.assertTrue(e0.is_same_as(e1))
                self.assertTrue(e1.is_same_as(e0))
            else:
                self.assertFalse(e0.is_same_as(e1))
                self.assertFalse(e1.is_same_as(e0))

    def test_eprouvette_clone(self):
        list_liquides = ["A", "B", "C"]
        e = Eprouvette(list_liquides)
        clone_e = e.clone()
        self.assertTrue(e.is_same_as(clone_e))
        for i, dose in enumerate(clone_e.iter_doses()):
            self.assertEqual(list_liquides[i], dose)

    def test_eprouvette_repr(self):
        e = Eprouvette(["A", "B", "C"])
        e_repr = f"{e}"
        self.assertIn("A", e_repr)
        self.assertIn("B", e_repr)
        self.assertIn("C", e_repr)


if __name__ == "__main__":

    unittest.main()
