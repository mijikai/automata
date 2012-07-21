def auto2regex(automaton, start_state, final_states):
    """Converts an automaton into a regular expression compatible with Perl
    regular expression. Automaton is a dictionary whose keys are the names of
    the states and whose values are dictionary. That dictionary has keys
    representing the label of the path to the next states and has values
    which are sets containing the name of the next states."""


    states = automaton[start_state]
    result = []
    for label, next_states in states.items():
        for s in next_states:
            if s == start_state:
                result.append('{}*'.format(label))
    return ''.join(result)


def delete_state(automaton, state):
    """Delete a state from the automaton. All states connected to it will be
    redirected so that all possible combinations of previous states and next
    states from this state will have a direct path which has a regex label."""
    del automaton[state]


def reverse_path(automaton):
    """Reverse the directed path of the states, that is, the previous state
    will be the next state and the next state will be the previous state."""
    reverse_automaton = {}
    for name in automaton:
        reverse_automaton[name] = {}

    for name, label_states in automaton.items():
        for label, next_states in label_states.items():
            for state in next_states:
                s = reverse_automaton[state].setdefault(label, set())
                s.add(name)
    return reverse_automaton
