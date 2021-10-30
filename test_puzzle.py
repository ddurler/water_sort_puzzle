#: coding:utf-8

import unittest

from eprouvette import Eprouvette
from puzzle import Puzzle


class TestPuzzle(unittest.TestCase):
    def test_puzzle(self):
        p = Puzzle([Eprouvette(["R", "R"]), Eprouvette(["R"])])
        p.add_eprouvette(Eprouvette(["R"]))

    def test_puzzle_len(self):
        p = Puzzle()
        self.assertEqual(len(p), 0)
        p.add_eprouvette(Eprouvette(["R"]))
        self.assertEqual(len(p), 1)

    def test_puzzle_items(self):
        e_0 = Eprouvette(["A"])
        e_1 = Eprouvette(["B"])
        e_2 = Eprouvette(["C"])
        p = Puzzle([e_0, e_1, e_2])
        self.assertEqual(p[0], e_0)
        self.assertEqual(p[1], e_1)
        self.assertEqual(p[2], e_2)

    def test_puzzle_repr(self):
        p = Puzzle([Eprouvette(["A", "B"]), Eprouvette(["C"])])
        puzzle_repr = f"{p}"
        self.assertIn("A", puzzle_repr)
        self.assertIn("B", puzzle_repr)
        self.assertIn("C", puzzle_repr)

    def test_puzzle_is_same_as(self):
        tests = [
            {"p0": [""], "p1": [""], "same": True},
            {"p0": [""], "p1": ["A"], "same": False},
            {"p0": ["A"], "p1": [""], "same": False},
            {"p0": ["A"], "p1": ["A"], "same": True},
            {"p0": ["A"], "p1": ["B"], "same": False},
            {"p0": ["A"], "p1": ["AB", "C"], "same": False},
            {"p0": ["AB"], "p1": ["B"], "same": False},
            {"p0": ["AB", "B"], "p1": ["AB", "B"], "same": True},
            {"p0": ["AB", "B"], "p1": ["B", "AB"], "same": True},
            {"p0": ["", "AB", "B"], "p1": ["B", "", "AB"], "same": True},
        ]

        self.assertFalse(Puzzle().is_same_as("Objet_qui_n_est_pas_un_puzzle"))

        for test in tests:
            p0 = Puzzle()
            for list_liquide in test["p0"]:
                e = Eprouvette(list_liquide)
                p0.add_eprouvette(e)

            p1 = Puzzle()
            for list_liquide in test["p1"]:
                e = Eprouvette(list_liquide)
                p1.add_eprouvette(e)

            if test["same"]:
                self.assertTrue(p0.is_same_as(p1))
                self.assertTrue(p1.is_same_as(p0))
            else:
                self.assertFalse(p0.is_same_as(p1))
                self.assertFalse(p1.is_same_as(p0))

    def test_puzzle_clone(self):
        p = Puzzle([Eprouvette(["A", "A"]), Eprouvette(["B"])])
        p2 = p.clone()
        self.assertTrue(p.is_same_as(p2))

    def test_puzzle_permutations(self):
        e_a = Eprouvette(["A"])
        e_b = Eprouvette(["B"])
        e_c = Eprouvette(["C"])
        p = Puzzle([e_a, e_b, e_c])
        permutations = [perm for perm in p.iter_permutations()]
        self.assertEqual(len(permutations), 6)
        self.assertIn((e_a, e_b), permutations)
        self.assertIn((e_a, e_c), permutations)
        self.assertIn((e_b, e_a), permutations)
        self.assertIn((e_b, e_c), permutations)
        self.assertIn((e_c, e_a), permutations)
        self.assertIn((e_c, e_b), permutations)

    def test_puzzle_is_consistant_nb_doses_liquide(self):
        p = Puzzle()
        for nb_doses in range(Eprouvette.MAX_DOSES):
            p.add_eprouvette(Eprouvette(["A"]))
            if nb_doses == Eprouvette.MAX_DOSES - 1:
                self.assertTrue(p.is_consistant)
            else:
                self.assertFalse(p.is_consistant)

    def test_puzzle_is_consistant_nb_doses_vides(self):
        list_liquides = ["A" for _ in range(Eprouvette.MAX_DOSES)]
        e = Eprouvette(list_liquides)
        p = Puzzle([e])
        self.assertFalse(p.is_consistant)

    def test_puzzle_is_done(self):
        tests = [
            [[""], True],
            [["A"], False],
            [["AA"], False],
            [["AAA"], False],
            [["AAAA"], True],
            [["AABB"], False],
            [["AAAA", ""], True],
            [["AAAA", "AABB"], False],
            [["AAAA", "AABB"], False],
            [["AAAA", "BBBB", ""], True],
        ]

        # Ce test est prévu pour des éprouvettes de 4 doses
        self.assertEqual(Eprouvette.MAX_DOSES, 4)

        for test in tests:
            p = Puzzle()
            for list_strings in test[0]:
                e = Eprouvette(list_strings)
                p.add_eprouvette(e)

            self.assertEqual(p.is_done, test[1])


if __name__ == "__main__":

    unittest.main()
