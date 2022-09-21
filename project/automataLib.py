from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph


def create_dfa_from_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def create_nfa_from_graph(
    graph: MultiDiGraph, start_nodes: set = None, final_nodes: set = None
) -> NondeterministicFiniteAutomaton:

    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    for node in start_nodes:
        nfa.add_start_state(node)

    for node in final_nodes:
        nfa.add_final_state(node)

    return nfa
