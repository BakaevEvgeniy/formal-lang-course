from scipy.sparse import kron, dok_matrix
from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)


class BoolDecomposition:
    def __init__(self, fa: FiniteAutomaton = None):
        if fa is None:
            self.num_states = 0
            self.start_states = set()
            self.final_states = set()
            self.state_indxs = {}
            self.bool_mats = {}
        else:
            self.num_states = len(fa.states)
            self.start_states = fa.start_states
            self.final_states = fa.final_states
            self.state_indxs = {state: indx for indx, state in enumerate(fa.states)}
            self.bool_mats = {}
            for state_from, trans in fa.to_dict().items():
                for label, state_to in trans.items():
                    if not isinstance(state_to, set):
                        state_to = {state_to}

                    for s_to in state_to:
                        indx_from = self.state_indxs[state_from]
                        indx_to = self.state_indxs[s_to]
                        if label not in self.bool_mats.keys():
                            self.bool_mats[label] = dok_matrix(
                                (self.num_states, self.num_states), dtype=bool
                            )

                        self.bool_mats[label][indx_from, indx_to] = True

    def intersection(self, other):
        res_of_intersection = BoolDecomposition(None)
        res_of_intersection.num_states = self.num_states * other.num_states
        intersection_labels = {}
        labels = self.bool_mats.keys() & other.bool_mats.keys()
        for label in labels:
            intersection_labels[label] = kron(
                self.bool_mats[label], other.bool_mats[label], format="csr"
            )
        res_of_intersection.bool_mats = intersection_labels

        for self_state, self_indx in self.state_indxs.items():
            for other_state, other_indx in other.state_indxs.items():
                new_state = new_state_indx = self_indx * other.num_states + other_indx
                res_of_intersection.state_indxs[new_state] = new_state_indx

                if (
                    self_state in self.start_states
                    and other_state in other.start_states
                ):
                    res_of_intersection.start_states.add(new_state)

                if (
                    self_state in self.final_states
                    and other_state in other.final_states
                ):
                    res_of_intersection.final_states.add(new_state)
        return res_of_intersection

    def to_automata(self):
        automaton = NondeterministicFiniteAutomaton()
        for label, bool_mat in self.bool_mats.items():
            for s_from, s_to in zip(*bool_mat.nonzero()):
                automaton.add_transition(s_from, label, s_to)

        for state in self.start_states:
            automaton.add_start_state(State(state))

        for state in self.final_states:
            automaton.add_final_state(State(state))

        return automaton
