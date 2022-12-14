import string
import cfpq_data
import networkx


def get_graph_info(graph_name: string):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    nodes_num = graph.number_of_nodes()
    edges_num = graph.number_of_edges()
    labels = []
    for edge in graph.edges(data=True):
        if edge[2]["label"] not in labels:
            labels.append(edge[2]["label"])
    return graph, nodes_num, edges_num, labels


def create_and_write_two_cycles_graph(n, m, labels, path):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(graph, path)
