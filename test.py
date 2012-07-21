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

    @unittest.skip('Skip temporarily for delete_state')
    def test_three_state_branching(self):
        """Test an automaton that accepts either 0 or 1 only."""
        automaton = {
                'a': {'0': {'b'}, '1': {'c'}},
                'b': {},
                'c': {},
        }
        self.assertEqual(auto2regex(automaton, 'a', {'b', 'c'}), '0|1')


class DeleteStateTest(unittest.TestCase):
    def test_lone_state(self):
        """Test for the deletion of one state automaton."""
        automaton = {'a': {}}
        delete_state(automaton, 'a')
        self.assertDictEqual(automaton, {})


if __name__ == '__main__':
    unittest.main()
