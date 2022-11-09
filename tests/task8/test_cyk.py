from project.cyk import CYK
from pyformlang.cfg import CFG


def test_syk():
    cfg = CFG.from_text(
        """
                        S -> B B
                        S -> C D
                        S -> epsilon
                        B -> B B
                        B -> C D
                        C -> (
                        D -> B E
                        D -> )
                        E -> )
                        """
    )

    accepted = ["()", "()()", "((()()))", "()()()()()(())"]
    rejected = ["((", "(()", "(()()()))", ")()()()()(())"]
    for word in accepted:
        assert CYK(cfg, word) == True

    for word in rejected:
        assert CYK(cfg, word) == False
