import unittest
from automaton_to_regex import *


class Auto2Regex(unittest.TestCase):
    def test_one_state(self):
        """Test for the automaton which the start and final state are equal."""
        automaton = {
                'a': {},
        }
        self.assertEqual(auto2regex(automaton, 'a', {'a'}), '')

    def test_one_state_loop(self):
        """Test for the automaton that accepts only one input of infinite
        length."""
        automaton = {
                'a': {'0': {'a'}},
        }
        self.assertEqual(auto2regex(automaton, 'a', {'a'}), '0*')


if __name__ == '__main__':
    unittest.main()
