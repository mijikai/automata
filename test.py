#!/usr/bin/env python3
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

    def test_three_state_one_loop(self):
        """Test the deletion of a middle state that is looping to itself."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'b'}, '2': {'c'}},
                'c': {},
        }
        final = {
                'a': {'01*2': {'c'}},
                'c': {},
        }
        delete_state(automaton, 'b')
        self.assertDictEqual(automaton, final)

    def test_delete_end(self):
        """Test the deletion of a state that has no successor."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {},
        }
        final = {'a': {}}
        delete_state(automaton, 'b')
        self.assertDictEqual(automaton, final)

    def test_two_state_loop_each(self):
        """Test the deletion of the second stat which goes back to the first
        one."""
        automaton = {
                'a': {'0': {'a'}, '1': {'b'}},
                'b': {'2': {'b'}, '3': {'a'}},
        }
        final = {'a': {'0': {'a'}, '12*3': {'a'}}}
        delete_state(automaton, 'b')
        self.assertDictEqual(automaton, final)

    def test_branch(self):
        """Test the deletion of state that has a label going to
        multiple states."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'c', 'd'}},
                'c': {},
                'd': {},
        }
        final = {'a': {'01': {'c', 'd'}},
                'c': {},
                'd': {},
        }
        delete_state(automaton, 'b')
        self.assertDictEqual(automaton, final)

    def test_branching_loop(self):
        """Test the deletion of state that has alternatives to itself."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'b'}, '2': {'b'}, '3': {'c'}},
                'c': {},
        }
        final = {'a': {'0(1|2)*3': {'c'}}, 'c': {}}
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

    def test_branching(self):
        """Test for branches."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'c'}, '2': {'d'}},
                'c': {},
                'd': {},
        }
        final = {
                'd': {'2': {'b'}},
                'c': {'1': {'b'}},
                'b': {'0': {'a'}},
                'a': {},
        }
        self.assertDictEqual(reverse_path(automaton), final)


    def test_dangling_state(self):
        """Test for invalid graph which has a set of next state that is not in
        the graph."""
        automaton = {
                'a': {'0': {'b'}},
                'b': {'1': {'c'}},
                'c': {'2': {'d'}},
        }
        self.assertRaises(KeyError, reverse_path, automaton)


if __name__ == '__main__':
    unittest.main()
