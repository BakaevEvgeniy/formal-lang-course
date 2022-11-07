from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA
from project.ecfg import ECFG


class RSM:
    def __init__(self, start_symbol: Variable, boxes: dict[Variable, EpsilonNFA]):
        self.start_symbol = start_symbol
        self.boxes = boxes

    def rsm_from_ecfg(ecfg: ECFG):
        return RSM(
            ecfg.start_symbol,
            {head: body.to_epsilon_nfa() for head, body in ecfg.productions.items()},
        )


def rsm_minimize(rsm: RSM):
    boxes = dict()
    for k in rsm.boxes.keys():
        boxes[k] = rsm.boxes[k].minimize()

    return RSM(rsm.start_symbol, boxes)
