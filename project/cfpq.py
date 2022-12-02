from typing import Tuple, Callable
from project.hellings import hellings
from project.matrix_based import matrix_based
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
import cfpq_data
from project.cfgLib import read_cfg_from_file
from project.tensor import tensor


def _cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
    algorithm: Callable = hellings,
) -> set[Tuple[int, int]]:

    if not start_nodes:
        start_nodes = graph.nodes
    if not final_nodes:
        final_nodes = graph.nodes

    result = set()
    for u, var, v in algorithm(cfg, graph):
        if var == start_var and u in start_nodes and v in final_nodes:
            result.add((u, v))
    return result


def cfpq_hellings(
    graph,
    cfg,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[Tuple[int, int]]:

    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)

    if isinstance(graph, str):
        graph_path = cfpq_data.download(graph)
        graph = cfpq_data.graph_from_csv(graph_path)

    return _cfpq(graph, cfg, start_nodes, final_nodes, start_var, hellings)


def cfpq_matrix(
    graph,
    cfg,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[Tuple[int, int]]:

    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)

    if isinstance(graph, str):
        graph_path = cfpq_data.download(graph)
        graph = cfpq_data.graph_from_csv(graph_path)

    return _cfpq(graph, cfg, start_nodes, final_nodes, start_var, matrix_based)


def cfpq_tensor(
    graph,
    cfg,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[Tuple[int, int]]:

    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)

    if isinstance(graph, str):
        graph_path = cfpq_data.download(graph)
        graph = cfpq_data.graph_from_csv(graph_path)

    return _cfpq(graph, cfg, start_nodes, final_nodes, start_var, tensor)
