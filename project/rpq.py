from networkx import MultiDiGraph
from project.automataLib import create_nfa_from_graph, create_dfa_from_regex
from project.boolDecomposition import BoolDecomposition
from pyformlang.regular_expression import Regex


def rpq(
    query: Regex, graph: MultiDiGraph, start_nodes: set = None, final_nodes: set = None
):
    bool_decomp_graph = BoolDecomposition(
        create_nfa_from_graph(graph, start_nodes, final_nodes)
    )
    bool_decomp_query = BoolDecomposition(create_dfa_from_regex(query))

    intersection = bool_decomp_graph.intersection(bool_decomp_query)
    tc = intersection.transitive_closure()
    res = set()
    for state_from, state_to in zip(*tc.nonzero()):
        if (
            state_from in intersection.start_states
            and state_to in intersection.final_states
        ):
            res.add(
                (
                    state_from // bool_decomp_query.num_states,
                    state_to // bool_decomp_query.num_states,
                ),
            )

    return res
