import random, cells
from bearlibterminal import terminal

class Kruskals_Algorithm:
    def __init__(self, arr):
        self.arr = arr
        self.nodes = []
        self.edges = []
        self.connections = []

    def set_nodes(self):
        '''Creates evenly spaced nodes'''
        region_id = 1
        for y in range(1, len(self.arr), 2):
            for x in range(1, len(self.arr[y]), 2):
                if self.arr[y][x] == 0:
                    node = Node(region_id, x, y)
                    self.arr[y][x] = node
                    self.nodes.append(node)
                    region_id += 1

    def set_edges(self):
        '''Creates edges between two nodes'''
        for y in range(1, len(self.arr), 2):
            for x in range(1, len(self.arr[y]), 2):
                if self.is_node(x, y) and self.is_node(x + 2, y):
                    edge = Edge(x + 1, y, "h")
                    self.edges.append(edge)
                if self.is_node(x, y) and self.is_node(x, y + 2):
                    edge = Edge(x, y + 1, "v")
                    self.edges.append(edge)

    def is_node(self, x, y):
        if x in range(len(self.arr[0])) and y in range(len(self.arr)):
            if self.arr[y][x] != None and self.arr[y][x] != 0 and self.arr[y][x].type == "node":
                return True
        return False

    def is_edge(self, x, y):
        if x in range(len(self.arr[0])) and y in range(len(self.arr)):
            if self.arr[y][x] != None and self.arr[y][x] != 0 and self.arr[y][x].type == "edge":
                return True
        return False

    def update_region(self, old_id, new_id):
        for node in self.nodes:
            if node.id == old_id:
                x, y = node.x, node.y
                self.arr[y][x].id = new_id

        for connection in self.connections:
            if connection.id == old_id:
                x, y = connection.x, connection.y
                self.arr[y][x].id = new_id

    def add_connecting_edge(self, edge):
        x, y = edge.x, edge.y
        self.arr[y][x] = edge
        self.connections.append(edge)

    def step(self):
        edge = random.choice(self.edges)
        self.edges.remove(edge)
        x, y = edge.x, edge.y
        if edge.dir == "v":
            node1 = self.arr[y-1][x]
            node2 = self.arr[y+1][x]
        elif edge.dir == "h":
            node1 = self.arr[y][x-1]
            node2 = self.arr[y][x+1]
        if node1.id != node2.id:
            edge.id = node1.id
            self.add_connecting_edge(edge)
            self.update_region(node2.id, node1.id)

    def set_regions(self):
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                if self.arr[y][x] is not None and self.arr[y][x] != 0:
                    self.arr[y][x] = self.arr[y][x].id

    def gen_maze(self):
        self.set_nodes()
        self.set_edges()
        while len(self.edges) > 0:
            self.step()
        self.set_regions()

class Node:
    def __init__(self, region_id, x, y):
        self.type = "node"
        self.id = region_id
        self.x = x
        self.y = y

class Edge:
    def __init__(self, x, y, direction):
        self.type = "edge"
        self.x = x
        self.y = y
        self.id = None
        self.dir = direction
