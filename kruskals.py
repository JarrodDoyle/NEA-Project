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
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                if y % 2 == 0:
                    break
                elif x % 2 != 0 and self.arr[y][x] != None:
                    node = Node(region_id, x, y)
                    self.arr[y][x] = node
                    self.nodes.append(node)
                    region_id += 1

    def set_edges(self):
        '''Creates edges between two nodes'''
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                if self.is_node(x, y) and self.is_node(x + 2, y):
                    edge = Edge(x + 1, y, "h")
                    self.arr[y][x + 1] = edge
                    self.edges.append(edge)
                if self.is_node(x, y) and self.is_node(x, y + 2):
                    edge = Edge(x, y + 1, "v")
                    self.arr[y + 1][x] = edge
                    self.edges.append(edge)

    def display_arr(self):
        for y in range(len(self.arr)):
            for x in range(len(self.arr[0])):
                obj = self.arr[y][x]
                if obj.char == "#":
                    terminal.puts(x, y, "[bkcolor={}] [/bkcolor]".format(obj.bk_color))

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

    def step(self):
        edge = random.choice(self.edges)
        self.edges.remove(edge)
        if edge.dir == "v":
            x, y = edge.x, edge.y
            for node in self.nodes:
                if node.x == x and node.y == y - 1:
                    node1 = node
                if node.x == x and node.y == y + 1:
                    node2 = node
            if node1.id != node2.id:
                edge.id = node1.id
                self.connections.append(edge)
                node_id = node2.id
                for node in self.nodes:
                    if node.id == node_id:
                        node.id = node1.id
                for connection in self.connections:
                    if connection.id == node_id:
                        connection.id = node1.id
        elif edge.dir == "h":
            x, y = edge.x, edge.y
            for node in self.nodes:
                if node.x == x - 1 and node.y == y:
                    node1 = node
                if node.x == x + 1 and node.y == y:
                    node2 = node
            if node1.id != node2.id:
                edge.id = node1.id
                self.connections.append(edge)
                node_id = node2.id
                for node in self.nodes:
                    if node.id == node_id:
                        node.id = node1.id
                for connection in self.connections:
                    if connection.id == node_id:
                        connection.id = node1.id

    def set_regions(self):
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                in_maze = False
                for node in self.nodes:
                    if node.x == x and node.y == y:
                        in_maze = True
                        break
                else:
                    for edge in self.connections:
                        if edge.x == x and edge.y == y:
                            in_maze = True
                            break
                if in_maze:
                    self.arr[y][x] = self.arr[y][x].id
                else:
                    self.arr[y][x] = None

    def set_tiles(self):
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                in_maze = False
                for node in self.nodes:
                    if node.x == x and node.y == y:
                        in_maze = True
                        break
                else:
                    for edge in self.connections:
                        if edge.x == x and edge.y == y:
                            in_maze = True
                            break
                if in_maze:
                    self.arr[y][x] = cells.Floor()
                else:
                    self.arr[y][x] = None

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

if __name__ == "__main__":
    terminal.open()
    terminal.set("window.size = 95x63; font: 'fonts/font_12x12.png', size = 12x12, codepage=437")
    while True:
        terminal.clear()
        arr =  [[0 for x in range(95)] for y in range(63)]
        maze = Kruskals_Algorithm(arr)
        maze.gen_maze()
        maze.display_arr()
        terminal.refresh()
        input()
