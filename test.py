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

    @unittest.skip('Skip for the implementation of reverse_path')
    def test_three_state(self):
        """Test the deletion of the middle state."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'c'}},
                'c': {},
        }
        final = {
                'a': {'01': {'c'}},
                'c': {},
        }
        delete_state(automaton, 'b')
        self.assertDictEqual(automaton, final)


class ReversePathTest(unittest.TestCase):
    def test_looping_state(self):
        """The reverse of looping state is the looping state itself."""
        automaton = {'a': {'0': {'a'}}}
        self.assertDictEqual(reverse_path(automaton), automaton)

    def test_three_state(self):
        """Test an automaton that has three states."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'c'}},
                'c': {},
        }
        final = {
                'c': {'1': {'b'}},
                'b': {'0': {'a'}},
                'a': {},
        }
        self.assertDictEqual(reverse_path(automaton), final)


if __name__ == '__main__':
    unittest.main()
