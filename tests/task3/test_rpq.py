from project.rpq import rpq
import project.graphLib
from project.automataLib import create_dfa_from_regex, create_nfa_from_graph
from pyformlang.regular_expression import Regex
import cfpq_data
import networkx
from itertools import product


def test_rpq_to_cycled_graph():
    graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=["a", "b"])

    req = Regex("a* b")
    res = rpq(req, graph)
    assert res == {(3, 4), (0, 3), (2, 3), (4, 5), (5, 0), (1, 3)}

    req = Regex("a* b")
    res = rpq(req, graph, {1}, {3})
    assert res == {(1, 3)}

    req = Regex("(a | b)*")
    res = rpq(req, graph)
    assert res == set(product(range(6), range(6)))


def test_chain_graph():
    graph = networkx.MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "a"}),
            (3, 4, {"label": "b"}),
        ]
    )

    req = Regex("a b")
    res = rpq(req, graph)
    assert res == {(0, 2), (2, 4)}

    res = rpq(req, graph, {0})
    assert res == {(0, 2)}

    req = Regex("a* b")
    res = rpq(req, graph)
    assert res == {(0, 2), (1, 2), (2, 4), (3, 4)}


def test_empty_regex():
    graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=["a", "b"])
    req = Regex("")
    res = rpq(req, graph)
    assert res == set()


def test_empty_graph():
    graph = networkx.MultiDiGraph()
    req = Regex("sad* s a d")
    res = rpq(req, graph)

    assert res == set()
