from typing import Tuple
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix
from project.cfgLib import cfg_to_weak_normal_form


def matrix_based(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, str, int]]:
    nodes_num = graph.number_of_nodes()
    if nodes_num == 0:
        return set()

    terminal_productions = set()
    var_productions = set()
    eps_productions = set()

    cfg = cfg_to_weak_normal_form(cfg)

    for p in cfg.productions:
        if len(p.body) == 1:
            terminal_productions.add(p)
        elif len(p.body) == 2:
            var_productions.add(p)
        else:
            eps_productions.add(p.head.value)

    matrices = {}
    for v in cfg.variables:
        matrices[v.value] = dok_matrix((nodes_num, nodes_num), dtype=bool)

    for u, v, ddict in graph.edges(data=True):
        for p in terminal_productions:
            if ddict["label"] == p.body[0].value:
                matrices[p.head.value][u, v] = True

    for i in range(nodes_num):
        for var in eps_productions:
            matrices[var][i, i] = True

    changed = True
    while changed:
        changed = False
        for p in var_productions:
            old_nnz = matrices[p.head.value].nnz
            matrices[p.head.value] += (
                matrices[p.body[0].value] @ matrices[p.body[1].value]
            )
            new_nnz = matrices[p.head.value].nnz
            changed = old_nnz != new_nnz

    result = set()
    for variable, matrix in matrices.items():
        for u, v in zip(*matrix.nonzero()):
            result.add((u, variable, v))
    return result
