import filecmp
import project.graphLib
import os


def test_get_graph_info():
    nodes, edges, labels = project.graphLib.get_graph_info("generations")

    # from README of generations.tar.gz
    assert nodes == 129
    assert edges == 273
    assert labels == [
        "rest",
        "first",
        "onProperty",
        "type",
        "hasValue",
        "someValuesFrom",
        "equivalentClass",
        "intersectionOf",
        "inverseOf",
        "range",
        "hasSibling",
        "sameAs",
        "hasParent",
        "hasSex",
        "hasChild",
        "versionInfo",
        "oneOf",
    ]


def test_build_two_cycles_graph():
    project.graphLib.create_and_write_two_cycles_graph(
        2, 3, ["a", "b"], "./tests/task1/builded_graph.dot"
    )
    assert filecmp.cmp(
        "./tests/task1/builded_graph.dot", "./tests/task1/expected_graph.dot"
    )
    os.remove("./tests/task1/builded_graph.dot")
