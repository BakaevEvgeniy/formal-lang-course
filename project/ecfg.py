from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: set[Variable] = None,
        start_symbol: Variable = None,
        productions: dict[Variable, Regex] = {},
    ):
        self.variables = variables
        self.start_symbol = start_symbol
        self.productions = productions

    def ecfg_from_cfg(cfg: CFG):
        variables = set(cfg.variables)

        if cfg.start_symbol is not None:
            start_symbol = cfg.start_symbol
        else:
            start_symbol = Variable("S")

        variables.add(start_symbol)
        productions: dict[Variable, Regex] = {}
        for p in cfg.productions:
            if len(p.body) > 0:
                body = Regex(" ".join(obj.value for obj in p.body))
            else:
                body = Regex("$")

            if p.head in productions:
                productions[p.head] = productions[p.head].union(body)
            else:
                productions[p.head] = body

        return ECFG(variables, cfg.start_symbol, productions)

    def ecfg_from_text(text: str, start_symbol: Variable = Variable("S")):
        variables = set()
        productions = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production = line.split("->")
            if len(production) != 2:
                return ECFG()

            v, body = production
            var = Variable(v.strip())

            if var in variables:
                return ECFG()

            variables.add(var)
            body = Regex(body)
            productions[var] = body

        return ECFG(variables, start_symbol, productions)

    def ecfg_from_file(path: str, start_symbol: Variable = Variable("S")):
        with open(path) as f:
            return ECFG.ecfg_from_text(f.read(), start_symbol)
