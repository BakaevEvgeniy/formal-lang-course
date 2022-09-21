from enum import auto
import filecmp
import os
import cfpq_data
import project.graphLib
from project.automataLib import create_dfa_from_regex, create_nfa_from_graph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)


def test_create_dfa_from_empty_regex():
    regex = Regex("")

    dfa = create_dfa_from_regex(regex)

    assert dfa.is_empty()


def test_create_dfa_from_regex():
    regex = Regex("(0 1|1)*")

    expected_automata = DeterministicFiniteAutomaton()

    state_0 = State(0)
    state_1 = State(1)

    symbol_0 = Symbol("0")
    symbol_1 = Symbol("1")

    expected_automata.add_start_state(state_0)
    expected_automata.add_final_state(state_0)

    expected_automata.add_transition(state_0, symbol_1, state_0)
    expected_automata.add_transition(state_0, symbol_0, state_1)
    expected_automata.add_transition(state_1, symbol_1, state_0)

    dfa = create_dfa_from_regex(regex)

    assert expected_automata.is_equivalent_to(dfa)


def test_create_nfa_from_graph():
    graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=["a", "b"])

    automaton = create_nfa_from_graph(graph, start_nodes=[0], final_nodes=[1, 3, 5])
    automaton.write_as_dot("./tests/task2/actual_cycles_graph.dot")

    assert filecmp.cmp(
        "./tests/task2/actual_cycles_graph.dot",
        "./tests/task2/expected_cycles_graph.dot",
    )
    os.remove("./tests/task2/actual_cycles_graph.dot")


def test_create_nfa_from_graph_without_start_and_final_nodes():
    graph = cfpq_data.labeled_two_cycles_graph(4, 4, labels=["a", "b"])

    automaton = create_nfa_from_graph(graph)
    automaton.write_as_dot(
        "./tests/task2/actual_cycles_graph_without_start_and_final_nodes.dot"
    )

    assert filecmp.cmp(
        "./tests/task2/actual_cycles_graph_without_start_and_final_nodes.dot",
        "./tests/task2/expected_cycles_graph_without_start_and_final_nodes.dot",
    )
    os.remove("./tests/task2/actual_cycles_graph_without_start_and_final_nodes.dot")


def test_create_nfa_from_graph_dataset():
    graph_path = cfpq_data.download("generations")
    graph = cfpq_data.graph_from_csv(graph_path)

    automaton = create_nfa_from_graph(graph)

    assert len(automaton.final_states) == len(graph.nodes)
    assert len(automaton.start_states) == len(graph.nodes)
