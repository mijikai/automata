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
    rev = reverse_path(automaton)
    looping_alter = []
    for prev_label, prev_set in rev[state].items():
        if state in prev_set:
            looping_alter.append('{}'.format(prev_label))
            prev_set.remove(state)

    if looping_alter:
        if len(looping_alter) > 1:
            template = '({})*'
        else:
            template = '{}*'
    else:
        template = '{}'

    looping = template.format('|'.join(looping_alter))

    for next_set in automaton[state].values():
        if state in next_set:
            next_set.remove(state)

    for prev_label, prev_set in rev[state].items():
        for prev_state in prev_set:
            automaton[prev_state][prev_label].remove(state)
            # Delete labels that points to nothing.
            if not automaton[prev_state][prev_label]:
                del automaton[prev_state][prev_label]


        # Build all possible paths from the states going to this state to the
        # states after this state. The label will be regex that simulate the
        # paths as if that state is there.
        for next_label, next_set in tuple(automaton[state].items()):
            new_label = '{}{}{}'.format(prev_label, looping, next_label)

            for next_state in next_set:
                for prev_state in prev_set:
                    prev_paths = automaton[prev_state]
                    new_set = prev_paths.setdefault(new_label, set())
                    new_set.add(next_state)
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
