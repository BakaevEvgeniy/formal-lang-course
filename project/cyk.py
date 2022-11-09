from pyformlang.cfg import CFG

def CYK(cfg: CFG, word: str):
    n = len(word)
    if n == 0:
        return cfg.generate_epsilon()
    
    cnf = cfg.to_normal_form()
    
    term_productions = [p for p in cnf.productions if len(p.body) == 1]
    var_productions = [p for p in cnf.productions if len(p.body) == 2]
            
    d = []
    
    for i in range(n):
        d.append([])
        for j in range(n):
            d[i].append(set())
            
    for i in range(n):
        for prod in term_productions:
            if word[i] == prod.body[0].value:
                d[i][i].update(prod.head.value)
    
    for step in range(1, n):
        for i in range(n - step):
            j = i + step
            for k in range(i, j):
                for prod in var_productions:
                    if (
                        prod.body[0].value in d[i][k]
                        and prod.body[1].value in d[k + 1][j]
                    ):
                        d[i][j].update(prod.head.value)

    return cnf.start_symbol.value in d[0][n - 1]
                        
    