from graphs.graph import Graph

class Kruskals_MST:
    def __init__(self, graph, num_nodes):
        self.graph = graph
        self.num_nodes = num_nodes

    # Find set of element using path compression
    def find_set(self, parent, e):
        if parent[e] == e:
            return e
        else:
            return self.find(parent, parent[e])

    def kruskals_mst(self):
        mst = []

        index = 0
        edge_count = 0

        graph = sorted(self.graph, key = lambda node: node[2])

        parent = []
        rank = []

        for node in range(self.num_nodes):
            parent.append(node)
            rank.append(0)

        while edge_count < self.num_nodes - 1:
            node1, node2, weight = self.graph[index]
            set1 = self.find(parent, node1)
            set2 = self.find(parent, node2)
            index += 1

            if set1 != set2:
                edge_count += 1
                mst.append([node1, node2, weight])
