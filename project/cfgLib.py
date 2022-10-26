from pyformlang.cfg import CFG


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:

    temp = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    simple_productions = temp._get_productions_with_only_single_terminals()
    simple_productions = temp._decompose_productions(simple_productions)

    return CFG(start_symbol=temp._start_symbol, productions=set(simple_productions))


def read_cfg_from_file(path: str) -> CFG:
    with open(path, "r") as f:
        data = f.read()

    return CFG.from_text(data)
