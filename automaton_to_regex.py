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
