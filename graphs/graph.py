class Graph:
    def __init__(self, graph = {}, num_nodes = 0):
        self.num_nodes = num_nodes
        self.graph = graph

    def add_node(node):
        self.graph[node] = []
        self.num_nodes += 1

    def add_edge(self, node1, node2, weight = None):
        if weight is not None:
            self.graph[node1].append([node2, weight])
            self.graph[node2].append([node1, weight])
        else:
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)

    def remove_edge(self, node1, node2, weight = None):
        if weight is not None:
            if [node2, weight] in self.graph[node1] and [node1, weight] in self.graph[node2]:
                self.graph[node1].remove([node2, weight])
                self.graph[node2].remove([node1, weight])
        elif node2 in self.graph[node1] and node1 in self.graph[node2]:
            self.graph[node1].remove(node2)
            self.graph[node2].remove(node1)
