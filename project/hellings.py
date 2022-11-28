from typing import Tuple
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
from project.cfgLib import cfg_to_weak_normal_form


def hellings(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, Variable, int]]:
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
