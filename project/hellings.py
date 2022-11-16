from typing import Tuple
import cfpq_data
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfgLib import cfg_to_weak_normal_form, read_cfg_from_file


def cfpq_with_helling(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[Tuple[int, int]]:
    if not start_nodes:
        start_nodes = graph.nodes
    if not final_nodes:
        final_nodes = graph.nodes

    result = set()
    for u, var, v in hellings(cfg, graph):
        if var == start_var and u in start_nodes and v in final_nodes:
            result.add((u, v))
    return result


def hellings(cfg, graph) -> set[Tuple[int, str, int]]:
    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)

    if isinstance(graph, str):
        graph_path = cfpq_data.download(graph)
        graph = cfpq_data.graph_from_csv(graph_path)

    nodes_num = graph.number_of_nodes()
    if nodes_num == 0:
        return set()

    terminal_productions = set()
    var_productions = set()
    eps_productions = set()

    cfg = cfg_to_weak_normal_form(cfg)

    result = set()
    for p in cfg.productions:
        if len(p.body) == 1:
            terminal_productions.add(p)
        elif len(p.body) == 2:
            var_productions.add(p)
        else:
            eps_productions.add(p.head.value)

    for u, v, ddict in graph.edges(data=True):
        for p in terminal_productions:
            if ddict["label"] == p.body[0].value:
                result.add((u, p.head, v))

    for node in graph.nodes:
        for var in eps_productions:
            result.add((node, var, node))

    q = result.copy()
    while len(q) > 0:
        tmp = set()
        start1, var1, end1 = q.pop()

        for (start2, var2, end2) in result:
            if end2 == start1:
                for p in var_productions:
                    if (
                        p.body[0] == var2
                        and p.body[1] == var1
                        and (start2, p.head, end1) not in result
                    ):
                        q.add((start2, p.head, end1))
                        tmp.add((start2, p.head, end1))
        for (start2, var2, end2) in result:
            if start2 == u:
                for p in var_productions:
                    if (
                        p.body[0] == var1
                        and p.body[1] == var2
                        and (start1, p.head, end2) not in result
                    ):
                        q.add((v, p.head, end2))
                        tmp.add((v, p.head, end2))

        result |= tmp

    return result
