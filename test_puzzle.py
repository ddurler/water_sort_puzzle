#: coding:utf-8

from tkinter import E
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
        e_0 = Eprouvette(['A'])
        e_1 = Eprouvette(['B'])
        e_2 = Eprouvette(['C'])
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

    def test_puzzle_eq(self):
        tests = [
            [[""],          [""],           True],
            [[""],          ["A"],          False],
            [["A"],         [""],           False],
            [["A"],         ["A"],          True],
            [["A"],         ["B"],          False],
            [["A"],         ["AB", "C"],    False],
            [["AB"],        ["B"],          False],
            [["AB", "B"],   ["AB", "B"],    True],
        ]

        self.assertFalse(Puzzle() == "Objet_qui_n_est_pas_un_puzzle")

        for test in tests:
            p0 = Puzzle()
            for list_liquide in test[0]:
                e = Eprouvette(list_liquide)
                p0.add_eprouvette(e)

            p1 = Puzzle()
            for list_liquide in test[1]:
                e = Eprouvette(list_liquide)
                p1.add_eprouvette(e)
            
            if test[2]:
                self.assertTrue(p0 == p1)
                self.assertFalse(p0 != p1)
            else:
                self.assertFalse(p0 == p1)
                self.assertTrue(p0 != p1)

    def test_puzzle_clone(self):
        p = Puzzle([Eprouvette(['A', 'A']), Eprouvette(['B'])])
        p2 = p.clone()
        self.assertTrue(p == p2)
        self.assertFalse(p != p2)

    def test_puzzle_permutations(self):
        e_a = Eprouvette(['A'])
        e_b = Eprouvette(['B'])
        e_c = Eprouvette(['C'])
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
        for nb_doses in range(Eprouvette.MAX_DOSES):  # 0..MAX_DOSES-1
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
            [[""],                      True],
            [["A"],                     False],
            [["AA"],                    False],
            [["AAA"],                   False],
            [["AAAA"],                  True],
            [["AABB"],                  False],
            [["AAAA", ""],              True],
            [["AAAA", "AABB"],          False],
            [["AAAA", "AABB"],          False],
            [["AAAA", "BBBB", ""],      True],
        ]

        # Ce test ne fonctionne que pour des éprouvettes de 4 doses
        self.assertEqual(Eprouvette.MAX_DOSES, 4)

        for test in tests:
            p = Puzzle()
            for list_strings in test[0]:
                e = Eprouvette(list_strings)
                p.add_eprouvette(e)

            self.assertEqual(p.is_done, test[1])


if __name__ == "__main__":

    unittest.main()
