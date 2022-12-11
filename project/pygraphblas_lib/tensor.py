from pycubool import Matrix

from typing import Tuple
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from project.automataLib import create_nfa_from_graph
from project.pygraphblas_lib.boolDecomposition import BoolDecomposition
from project.rsm import RSM, rsm_minimize
from project.ecfg import ECFG




def tensor(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, str, int]]:
    graph_matrix = BoolDecomposition(create_nfa_from_graph(graph))
    rsm = rsm_minimize(RSM.rsm_from_ecfg((ECFG.ecfg_from_cfg(cfg))))
    rsm_matrix = BoolDecomposition(rsm.rsm_to_single_NFA())
            
    identity_matrix = Matrix.empty(shape=(graph_matrix.num_states, graph_matrix.num_states))
    for i in range(graph_matrix.num_states):
        identity_matrix[i, i] = True
    
    for var in cfg.get_nullable_symbols():
        if var.value in graph_matrix.bool_mats.keys():
            graph_matrix.bool_mats[var.value] += identity_matrix
        else:
            graph_matrix.bool_mats[var.value] = identity_matrix

    last = 0
    while True:
        tc_idxs = list(
            zip(*rsm_matrix.intersection(graph_matrix).transitive_closure().to_lists())
        )
        if len(tc_idxs) == last:
            break
        last = len(tc_idxs)
        for (i, j) in tc_idxs:
            r_i, r_j = i // graph_matrix.num_states, j // graph_matrix.num_states
            g_i, g_j = (
                i % graph_matrix.num_states,
                j % graph_matrix.num_states,
            )

            state_from = rsm_matrix.indx_to_state[r_i]
            state_to = rsm_matrix.indx_to_state[r_j]
            var, _ = state_from.value
            if (
                state_from in rsm_matrix.start_states
                and state_to in rsm_matrix.final_states
            ):
                if var.value in graph_matrix.bool_mats.keys():
                    graph_matrix.bool_mats[var][g_i, g_j] = True
                else:
                    graph_matrix.bool_mats[var] = Matrix.empty(
                        shape=(graph_matrix.num_states, graph_matrix.num_states)
                    )
                    graph_matrix.bool_mats[var][g_i, g_j] = True

    result = set()
    for variable, matrix in graph_matrix.bool_mats.items():
        for u, v in zip(*matrix.to_lists()):
            result.add(
                (graph_matrix.indx_to_state[u], variable, graph_matrix.indx_to_state[v])
            )

    return result
