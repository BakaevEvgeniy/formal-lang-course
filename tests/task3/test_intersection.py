import project.boolDecomposition
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


def test_intersection_with_empty():
    symbol_0 = Symbol("0")
    symbol_1 = Symbol("1")

    first = DeterministicFiniteAutomaton()
    state_p = State("p")
    state_q = State("q")

    first.add_start_state(state_p)
    first.add_final_state(state_q)
    first.add_transition(state_p, symbol_1, state_p)
    first.add_transition(state_p, symbol_0, state_q)
    first.add_transition(state_q, symbol_0, state_q)
    first.add_transition(state_q, symbol_1, state_q)

    second = DeterministicFiniteAutomaton()
    bool_dec_first = project.boolDecomposition.BoolDecomposition(first)
    bool_dec_second = project.boolDecomposition.BoolDecomposition(second)

    actual_intersection = bool_dec_first.intersection(bool_dec_second)
    actual_automata = actual_intersection.to_automata()
    assert len(actual_automata.states) == 0


def test_intersection_two_empty():
    first = DeterministicFiniteAutomaton()
    second = DeterministicFiniteAutomaton()

    bool_dec_first = project.boolDecomposition.BoolDecomposition(first)
    bool_dec_second = project.boolDecomposition.BoolDecomposition(second)

    actual_intersection = bool_dec_first.intersection(bool_dec_second)
    actual_automata = actual_intersection.to_automata()
    assert len(actual_automata.states) == 0


def test_intersection():

    symbol_0 = Symbol("0")
    symbol_1 = Symbol("1")

    first = DeterministicFiniteAutomaton()
    state_p = State("p")
    state_q = State("q")

    first.add_start_state(state_p)
    first.add_final_state(state_q)
    first.add_transition(state_p, symbol_1, state_p)
    first.add_transition(state_p, symbol_0, state_q)
    first.add_transition(state_q, symbol_0, state_q)
    first.add_transition(state_q, symbol_1, state_q)

    second = DeterministicFiniteAutomaton()
    state_r = State("r")
    state_s = State("s")
    second.add_start_state(state_r)
    second.add_final_state(state_s)
    second.add_transition(state_r, symbol_0, state_r)
    second.add_transition(state_r, symbol_1, state_s)
    second.add_transition(state_s, symbol_0, state_s)
    second.add_transition(state_s, symbol_1, state_s)

    bool_dec_first = project.boolDecomposition.BoolDecomposition(first)
    bool_dec_second = project.boolDecomposition.BoolDecomposition(second)

    actual_intersection = bool_dec_first.intersection(bool_dec_second)
    actual_automata = actual_intersection.to_automata()

    expected = DeterministicFiniteAutomaton()
    state_0 = State("0")
    state_1 = State("1")
    state_2 = State("2")
    state_3 = State("3")

    expected.add_start_state(state_0)
    expected.add_final_state(state_3)

    expected.add_transition(state_0, symbol_1, state_1)
    expected.add_transition(state_1, symbol_1, state_1)
    expected.add_transition(state_1, symbol_0, state_3)
    expected.add_transition(state_0, symbol_0, state_2)
    expected.add_transition(state_2, symbol_0, state_2)
    expected.add_transition(state_2, symbol_1, state_3)
    expected.add_transition(state_3, symbol_0, state_3)
    expected.add_transition(state_3, symbol_1, state_3)

    assert expected.is_equivalent_to(actual_automata)
