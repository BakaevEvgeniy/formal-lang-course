from project.cfpq import cfpq_hellings
from project.pycubool.cfpq import cfpq_tensor, cfpq_matrix
from pyformlang.cfg import CFG
from networkx import MultiDiGraph
from pyformlang.cfg import CFG


def test_simple_grammar():

    cfg = CFG.from_text(
        """
                        S -> A
                        S -> B
                        A -> a
                        B -> b
                        """
    )

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from([(0, 1, {"label": "a"}), (1, 2, {"label": "b"})])

    res = cfpq_hellings(graph, cfg)
    assert res == {(0, 1), (1, 2)}
    res_tensor = cfpq_tensor(graph, cfg)
    assert res == res_tensor
    res_matrix = cfpq_matrix(graph, cfg)
    assert res == res_matrix


def test_chain():

    cfg = CFG.from_text(
        """
                        S -> A B
                        A -> a
                        B -> b
        """
    )

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from([(0, 1, {"label": "a"}), (1, 2, {"label": "b"})])

    res = cfpq_hellings(graph, cfg)
    assert res == {(0, 2)}
    res_tensor = cfpq_tensor(graph, cfg)
    assert res == res_tensor
    res_matrix = cfpq_matrix(graph, cfg)
    assert res == res_matrix

    cfg = CFG.from_text(
        """
                        S -> B A
                        A -> a
                        B -> b
        """
    )

    res = cfpq_hellings(graph, cfg)
    assert res == set()
    res_tensor = cfpq_tensor(graph, cfg)
    assert res == res_tensor
    res_matrix = cfpq_matrix(graph, cfg)
    assert res == res_matrix


def test_special_nodes():

    cfg = CFG.from_text(
        """
                    S -> a S b S | a b
                    S -> epsilon
        """
    )

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3, 4])
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (1, 4, {"label": "b"}),
            (4, 2, {"label": "a"}),
            (2, 3, {"label": "b"}),
        ]
    )

    res = cfpq_hellings(graph, cfg)
    assert res == {
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (0, 4),
        (4, 3),
        (0, 3),
        (0, 2),
    }
    res_tensor = cfpq_tensor(graph, cfg)
    assert res == res_tensor
    res_matrix = cfpq_matrix(graph, cfg)
    assert res == res_matrix

    res = cfpq_hellings(
        graph,
        cfg,
        start_nodes={0, 4},
        final_nodes=[
            0,
            1,
            2,
            3,
        ],
    )
    assert res == {
        (0, 0),
        (4, 3),
        (0, 3),
        (0, 2),
    }
    res_tensor = cfpq_tensor(
        graph,
        cfg,
        start_nodes={0, 4},
        final_nodes=[
            0,
            1,
            2,
            3,
        ],
    )
    assert res == res_tensor
    res_matrix = cfpq_matrix(
        graph,
        cfg,
        start_nodes={0, 4},
        final_nodes=[
            0,
            1,
            2,
            3,
        ],
    )
    assert res == res_matrix
