## Язык запросов к графам

### Описание абстрактного синтаксиса языка

```
prog = list<stmt>
stmt =
    bind of var * expr
  | print of expr
val =
    string of string
  | int of int
  | bool of bool
  | path of path
  | list of string
  | list of int
  | list of bool
expr =
    var of var                   // переменные
  | val of val                   // константы
  | set_start of set<val> * expr // задать множество стартовых состояний
  | set_final of set<val> * expr // задать множество финальных состояний
  | Add_start of set<val> * expr // добавить состояния в множество стартовых
  | Add_final of set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
lambda =
    lambda of list<var> * expr
```

### Описание конкретного синтаксиса языка
```
prog -> stmt ; prog | eps
stmt -> var = expr | print(expr)
lowercase -> [a-z]
uppercase -> [A-Z]
digit -> [0-9]
int -> 0 | [1-9] digit*
string -> (_ | . | lowercase | uppercase) (_ | . | lowercase | uppercase | digit)*
bool -> true | false
path -> " (/ | _ | . | lowercase | uppercase | digit)+ "
var -> string
val ->
    int
    | " string "
    | bool
    | path
    | list<int>
    | list<" string ">
    | list<bool>
set ->
    set<int>
    | set<" string ">
    | range ( int , int )
expr -> var
expr -> val
expr -> graph
graph -> " string "
graph -> set_start(set, graph)
graph -> set_final(set, graph)
graph -> add_start(set, graph)
graph -> add_final(set, graph)
expr -> vertex | vertices
vertex -> int
vertices -> set<vertex> | range ( int , int )
vertices -> get_start(graph)
vertices -> get_final(set, graph)
expr -> pair
pair -> set<(int, int)>
pair -> get_reachable(graph)
vertices -> get_vertices(graph)
expr -> edge | edges
edge -> (int, " string ", int) | (int, int, int)
edges -> set<edge>
edges -> get_edges(graph)
expr -> labels
labels -> set<int> | set<" string ">
labels -> get_labels(graph)
expr -> map(lambda, expr)
expr -> filter(lambda, expr)
graph -> load(" path ")
graph -> intersect(graph, graph)
graph -> concat(graph, graph)
graph -> union(graph, graph)
graph -> star(graph, graph)
lambda -> (list<var> -> [bool_expr | expr])
bool_expr ->
    bool_expr or bool_expr
    | bool_expr and bool_expr
    | not bool_expr
    | bool
    | has_label(edge, " string ")
    | is_start(vertex)
    | is_final(vertex)
    | x in set<x>
list<x> -> list(x [, x]*) | list()
set<x> -> set(x [, x]*) | set()
```

### Пример программы
```
g = load("wine")
h = set_start(set_final(get_vertices(g), g)), range(1, 10))
l = union("l1", "l2")
q = concat("sub_class_of", l)
res = intersect(g, q1)
print(res)
s = get_start(g)
vertices = filter((list(v) -> v in s), get_edges(res))
print(vertices)
```