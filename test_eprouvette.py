#: coding:utf-8

import unittest

from eprouvette import Eprouvette, EprouvetteError


class TestEprouvette(unittest.TestCase):
    def test_epouvette_RR(self):
        e = Eprouvette(["R", "R"], max_len=4)
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(e.liquides, {"R"})
        self.assertEqual(len(e), 2)
        self.assertEqual(e.top_liquide, "R")
        self.assertEqual(e[0], "R")
        self.assertEqual(e[1], "R")
        self.assertEqual(e[2], None)
        self.assertEqual(e[3], None)
        self.assertEqual(e[-1], "R")

        def get_index(_e, i):
            return _e[i]

        self.assertRaises(EprouvetteError, get_index, e, 4)

    def test_epouvette_ABC(self):
        e = Eprouvette(["A", "B", "C"], max_len=4)
        self.assertEqual(e.nb_different_liquides, 3)
        self.assertEqual(e.liquides, {"A", "B", "C"})
        self.assertEqual(len(e), 3)
        self.assertEqual(e.top_liquide, "C")
        self.assertEqual(e[0], "A")
        self.assertEqual(e[1], "B")
        self.assertEqual(e[2], "C")
        self.assertEqual(e[3], None)

    def test_eprouvette_iterable(self):
        e = Eprouvette(["A", "B", "C"])
        s = ""
        for dose in e:
            s += dose
        self.assertEqual(s, "ABC")

    def test_eprouvette_max_len(self):

        # max_len n'est pas défini si pas explicite à la création
        e = Eprouvette("12")
        self.assertIsNone(e.max_len)

        def set_max_len(eprouvette, value):
            eprouvette.max_len = value

        # Un exception est levée si on tente de définir un max_len incohérent (ici au moins 2)
        self.assertRaises(EprouvetteError, set_max_len, e, -1)
        self.assertRaises(EprouvetteError, set_max_len, e, 0)
        self.assertRaises(EprouvetteError, set_max_len, e, 1)

        # On peut définir max_len si cohérent
        e.max_len = 4
        self.assertEqual(e.max_len, 4)

        # Et annuler cette définition
        e.max_len = None
        self.assertIsNone(e.max_len)

    def test_eprouvette_is_pleine(self):
        e = Eprouvette(["A", "B", "B", "C"], max_len=4)
        self.assertTrue(e.is_pleine)
        e.max_len = None
        self.assertFalse(e.is_pleine)

    def test_eprouvette_pop(self):
        e = Eprouvette(["A", "B", "B", "C"])

        c = e.pop_dose()
        self.assertEqual(c, "C")
        self.assertEqual(e.nb_different_liquides, 2)
        self.assertEqual(len(e), 3)
        self.assertEqual(e.top_liquide, "B")

        c = e.pop_dose()
        self.assertEqual(c, "B")
        self.assertEqual(e.nb_different_liquides, 2)
        self.assertEqual(len(e), 2)
        self.assertEqual(e.top_liquide, "B")

        c = e.pop_dose()
        self.assertEqual(c, "B")
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(len(e), 1)
        self.assertEqual(e.top_liquide, "A")

        c = e.pop_dose()
        self.assertEqual(c, "A")
        self.assertEqual(e.nb_different_liquides, 0)
        self.assertEqual(len(e), 0)
        self.assertEqual(e.top_liquide, None)

        self.assertRaises(EprouvetteError, e.pop_dose)

    def test_eprouvette_push(self):
        e = Eprouvette(["A"], max_len=4)

        self.assertTrue(e.can_push_dose("A"))
        e.push_dose("A")
        self.assertEqual(e.nb_different_liquides, 1)
        self.assertEqual(len(e), 2)
        self.assertEqual(e.top_liquide, "A")

        self.assertFalse(e.can_push_dose("B"))
        self.assertRaises(EprouvetteError, e.push_dose, "B")

        self.assertFalse(e.can_push_dose(None))
        self.assertRaises(EprouvetteError, e.push_dose, None)

    def test_eprouvette_push_overflow(self):
        list_liquides = ["A" for _ in range(4)]
        e = Eprouvette(list_liquides, max_len=4)
        self.assertTrue(e.is_pleine)
        self.assertRaises(EprouvetteError, e.push_dose, "A")

    def test_eprouvette_verser(self):
        tests = [
            {"source": [], "destination": [], "possible": False},
            {"source": ["A"], "destination": [], "possible": True, "nb_doses": 1},
            {"source": ["A"], "destination": ["B"], "possible": False},
            {"source": ["A"], "destination": ["A"], "possible": True, "nb_doses": 1},
            {
                "source": ["A", "A"],
                "destination": ["A"],
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": ["A", "A"],
                "destination": ["A", "A"],
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": ["A", "A", "A"],
                "destination": ["A", "A"],
                "possible": True,
                "nb_doses": 2,
            },
            {
                "source": ["A", "A", "A"],
                "destination": ["A", "A", "A"],
                "possible": True,
                "nb_doses": 1,
            },
            {"source": ["A"], "destination": ["A", "A", "A", "A"], "possible": False},
            {
                "source": ["B", "B", "A"],
                "destination": ["A"],
                "possible": True,
                "nb_doses": 1,
            },
            {
                "source": ["B", "B", "A", "A"],
                "destination": ["B", "A"],
                "possible": True,
                "nb_doses": 2,
            },
        ]

        # Ce test est prévu pour des éprouvettes contenant 4 doses

        for test in tests:
            source = Eprouvette(test["source"], max_len=4)
            destination = Eprouvette(test["destination"], max_len=4)

            len_source_avant = len(source)
            len_destination_avant = len(destination)

            if test["possible"]:
                self.assertTrue(source.is_possible_verser_une_dose_dans(destination))
                nb_doses = source.verser_dans(destination)
                self.assertEqual(test["nb_doses"], nb_doses)
                self.assertEqual(len_source_avant - nb_doses, len(source))
                self.assertEqual(len_destination_avant + nb_doses, len(destination))
            else:
                self.assertFalse(source.is_possible_verser_une_dose_dans(destination))

    def test_eprouvette_eq(self):
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

        self.assertFalse(Eprouvette(["A"]) == "Objet_qui_n_est_pas_une_eprouvette")

        for test in tests:
            e0 = Eprouvette(test[0], max_len=4)
            e1 = Eprouvette(test[1], max_len=4)
            if test[2]:
                self.assertTrue(e0 == e1)
                self.assertFalse(e0 != e1)
            else:
                self.assertFalse(e0 == e1)
                self.assertTrue(e0 != e1)

    def test_eprouvette_clone(self):
        list_liquides = ["A", "B", "C"]
        e = Eprouvette(list_liquides)
        clone_e = e.clone()
        self.assertTrue(e == clone_e)
        self.assertFalse(e != clone_e)
        for i, dose in enumerate(clone_e):
            self.assertEqual(list_liquides[i], dose)

    def test_eprouvette_repr(self):
        e = Eprouvette(["A", "B", "C"])
        e_repr = f"{e}"
        self.assertIn("A", e_repr)
        self.assertIn("B", e_repr)
        self.assertIn("C", e_repr)


if __name__ == "__main__":

    unittest.main()
