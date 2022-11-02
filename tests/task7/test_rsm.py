from project.automataLib import create_dfa_from_regex
from project.ecfg import ECFG
from project.rsm import RSM, rsm_minimize


def test_rsm_from_ecfg_minimize():
    ecfg = ECFG.ecfg_from_text("S -> (S|A)* 1* A*  0\n A -> 1*")
    rsm = RSM.rsm_from_ecfg(ecfg)

    assert all(
        rsm.boxes.get(k).is_equivalent_to(create_dfa_from_regex(ecfg.productions[k]))
        for k in ecfg.productions.keys()
    )

    rsm = rsm_minimize(rsm)

    assert all(
        rsm.boxes[k] == create_dfa_from_regex(ecfg.productions[k])
        for k in ecfg.productions.keys()
    )
