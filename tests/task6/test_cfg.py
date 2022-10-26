from itertools import count
from pyformlang.cfg import CFG, Variable, Terminal, Production, Epsilon
from project.cfgLib import cfg_to_weak_normal_form, read_cfg_from_file


def test_epsilon_gram():
    cfg = CFG.from_text("S -> epsilon")
    wncf = cfg_to_weak_normal_form(cfg)
    assert len(wncf.productions) == 1
    assert len(wncf.remove_epsilon().productions) == 0


def test_simple_gram():
    cfg = CFG.from_text("S -> a | b")
    expected = CFG(
        [Variable("S")],
        [Terminal("a"), Terminal("b")],
        Variable("S"),
        {
            Production(Variable("S"), [Terminal("a")]),
            Production(Variable("S"), [Terminal("b")]),
        },
    )
    wncf = cfg_to_weak_normal_form(cfg)
    assert (expected.productions) == expected.productions


def test_chained_gram():
    cfg = CFG.from_text("S -> A\n A -> B\n B -> C\n C -> 0")
    expected = CFG(
        [Variable("S")],
        [Terminal("0")],
        Variable("S"),
        {
            Production(Variable("S"), [Terminal("0")]),
        },
    )
    wncf = cfg_to_weak_normal_form(cfg)
    assert wncf.productions == expected.productions


def test_gram_with_cycle():
    cfg = CFG.from_text("S -> C\n A -> B\n B -> A\n C -> 0 | A | S")
    expected = CFG(
        [Variable("S")],
        [Terminal("0")],
        Variable("S"),
        {
            Production(Variable("S"), [Terminal("0")]),
        },
    )
    wncf = cfg_to_weak_normal_form(cfg)
    assert wncf.productions == expected.productions


def test_read_from_file():
    cfg = read_cfg_from_file("./tests/task6/test.txt")
    expected = CFG(
        [Variable("S"), Variable("C#CNF#1"), Variable("0#CNF#"), Variable("B")],
        [Terminal("0"), Terminal("1")],
        Variable("S"),
        [
            Production(Variable("S"), [Variable("B"), Variable("C#CNF#1")]),
            Production(Variable("S"), []),
            Production(Variable("B"), [Terminal("0")]),
            Production(Variable("B"), [Terminal("1")]),
            Production(Variable("C#CNF#1"), [Variable("B"), Variable("0#CNF#")]),
            Production(Variable("0#CNF#"), [Terminal("0")]),
        ],
    )
    wncf = cfg_to_weak_normal_form(cfg)
    for p in wncf.productions:
        assert p in expected.productions
    assert len(wncf.productions) == len(expected.productions)
