import string
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    return regex.to_epsilon_nfa().to_deterministic().minimize()
