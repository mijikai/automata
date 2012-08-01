from copy import deepcopy


def auto2regex(automaton, start_state, final_states):
    """Converts an automaton into a regular expression compatible with Perl
    regular expression. Automaton is a dictionary whose keys are the names of
    the states and whose values are dictionary. That dictionary has keys
    representing the label of the path to the next states and has values
    which are sets containing the name of the next states."""


    result = []
    for s in tuple(automaton):
        if s == start_state or s in final_states:
            continue
        delete_state(automaton, s)

    for final in final_states:
        temp = deepcopy(automaton)
        for t_s in tuple(temp):
            if t_s in (start_state, final):
                continue
            delete_state(temp, t_s)
        length = len(temp.keys())
        if length == 1:
            if temp[start_state]:
                if len(temp[start_state]) == 1:
                    template = '{}*'
                else:
                    template = '({})*'
            else:
                template = '{}'
            result.append(template.format('|'.join(sorted(temp[start_state]))))
        elif length == 2:
            # Add a state before the start and after the final so that we can
            # delete the initial and final state and form the final regex.

            pre_start = '{}{}s'.format(start_state, final)
            post_final = '{}{}f'.format(start_state, final)

            temp[pre_start] = {'': {start_state}}
            delete_state(temp, start_state)

            temp[final].setdefault('', set())
            temp[final][''].add(post_final)
            temp[post_final] = {}
            delete_state(temp, final)

            result.append(*temp[pre_start])
        else:
            raise Exception(
                'Maximum length of two is the supposed final state')

    return '|'.join(sorted(result))


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
