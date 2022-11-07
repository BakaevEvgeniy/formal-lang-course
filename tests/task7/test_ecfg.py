from pyformlang.cfg import CFG, Variable
from project.ecfg import ECFG
from pyformlang.regular_expression import Regex


def test_read_from_empty_text():
    ecfg = ECFG.ecfg_from_text("")
    assert ecfg.productions == {}


def test_read_unsupported_fromat_text():
    ecfg = ECFG.ecfg_from_text("S -> 1* S \n S -> A* B")
    assert ecfg.productions == {}


def test_read_text():
    ecfg = ECFG.ecfg_from_text("S -> 1* S \n A -> A* 0")
    expected = ECFG(
        {Variable("S"), Variable("A")},
        Variable("S"),
        {
            Variable("A"): Regex("A* 0"),
            Variable("S"): Regex("1* S"),
        },
    )
    assert len(expected.productions) == len(ecfg.productions)
    for p in ecfg.productions:
        assert p in expected.productions


def test_ecfg_from_cfg():
    cfg = CFG.from_text("S -> A S 0\n A -> 1\n A -> C\n C -> C 0")
    ecfg = ECFG.ecfg_from_cfg(cfg)
    expected = ECFG(
        {Variable("S"), Variable("A"), Variable("C")},
        Variable("S"),
        {
            Variable("S"): Regex("A.S.0"),
            Variable("A"): Regex("1|C"),
            Variable("C"): Regex("C.0"),
        },
    )
    assert len(expected.productions) == len(ecfg.productions)
    for p in ecfg.productions:
        assert p in expected.productions


def test_ecfg_from_file():
    ecfg = ECFG.ecfg_from_file("./tests/task7/test.txt")
    expected = ECFG(
        {Variable("S"), Variable("A"), Variable("C")},
        Variable("S"),
        {
            Variable("S"): Regex("A.S.0"),
            Variable("A"): Regex("1*|C*"),
            Variable("C"): Regex("0"),
        },
    )
    assert len(expected.productions) == len(ecfg.productions)
    for p in ecfg.productions:
        assert p in expected.productions
