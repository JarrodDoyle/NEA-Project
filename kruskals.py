import random, cells
from bearlibterminal import terminal

class Kruskals_Algorithm:
    """
    Class used to perform Kruskals Algorithm on an arr using randomly assigned
    edge weights
    """
    def __init__(self, arr):
        """
        Initialize empty lists for nodes, edges and connections

        arr -- the array of cells to perform Kruskals on
        """
        self.arr = arr
        self.nodes = []
        self.edges = []
        self.connections = []

    def set_nodes(self):
        """
        Create evenly spaced nodes from the 2d dungeon arr
        """
        # Each node has a region ID, used later for checking region connectivity
        region_id = 1
        # For loops use every other x/y
        for y in range(1, len(self.arr), 2):
            for x in range(1, len(self.arr[y]), 2):
                # If x/y cell is not empty (NoneType)
                if self.arr[y][x] == 0:
                    # Add the node to the nodes list and increment region ID
                    node = Node(region_id, x, y)
                    self.arr[y][x] = node
                    self.nodes.append(node)
                    region_id += 1

    def set_edges(self):
        """
        Create edges between nodes
        """
        # Only node points to the right and below are checked as starting from
        # the top left of the arr, all potential edge points will be considered
        for y in range(1, len(self.arr), 2):
            for x in range(1, len(self.arr[y]), 2):
                # If point is a node and potential node point to the right is
                # also a node, add an edge
                if self.is_node(x, y) and self.is_node(x + 2, y):
                    edge = Edge(x + 1, y, "h")
                    self.edges.append(edge)
                # If point is a node and potential node point below is also a
                # node, add an edge
                if self.is_node(x, y) and self.is_node(x, y + 2):
                    edge = Edge(x, y + 1, "v")
                    self.edges.append(edge)

    def is_node(self, x, y):
        """
        Return boolean for whether a point is a node

        x -- x coordinate of point to be checked
        y -- y coordinate of point to be checked
        """
        # If x and y coordinates are valid
        if x in range(len(self.arr[0])) and y in range(len(self.arr)):
            if self.arr[y][x] != None and self.arr[y][x] != 0 and self.arr[y][x].type == "node":
                return True
        return False

    def is_edge(self, x, y):
        """
        Return boolean for whether a point is an edge

        x -- x coordinate of point to be checked
        y -- y coordinate of point to be checked
        """
        # If x and y coordinates are valid
        if x in range(len(self.arr[0])) and y in range(len(self.arr)):
            if self.arr[y][x] != None and self.arr[y][x] != 0 and self.arr[y][x].type == "edge":
                return True
        return False

    def update_region(self, old_id, new_id):
        """
        Update nodes and edges with a new region ID

        old_id -- Region ID to be replaced
        new_id -- ID to be replaced with
        """
        for node in self.nodes:
            # If node in region being updated, update it
            if node.id == old_id:
                x, y = node.x, node.y
                self.arr[y][x].id = new_id

        for connection in self.connections:
            # If edge in region being updated, update it
            if connection.id == old_id:
                x, y = connection.x, connection.y
                self.arr[y][x].id = new_id

    def add_connecting_edge(self, edge):
        """
        Add a potential edge point as a connection in arr

        edge -- the edge to be added as a connection
        """
        x, y = edge.x, edge.y
        self.arr[y][x] = edge
        self.connections.append(edge)

    def step(self):
        """
        Run a step of the algorithm
        """
        # Pick a random edge (has the effect of using randomly assigned edge weights)
        edge = random.choice(self.edges)
        self.edges.remove(edge)
        x, y = edge.x, edge.y
        # If edge is vertical
        if edge.dir == "v":
            node1 = self.arr[y-1][x]
            node2 = self.arr[y+1][x]
        # If edge is horizontal
        elif edge.dir == "h":
            node1 = self.arr[y][x-1]
            node2 = self.arr[y][x+1]
        # If nodes are not already connected (if they have different region ids)
        if node1.id != node2.id:
            # Add the edge as a connection and update the region IDs so that they match
            edge.id = node1.id
            self.add_connecting_edge(edge)
            self.update_region(node2.id, node1.id)

    def set_regions(self):
        """
        Convert from node/edge based arr to ID based array
        """
        # For each point in the 2d arr
        for y in range(len(self.arr)):
            for x in range(len(self.arr[y])):
                # If its not None and not 0 then it must be an edge or node
                if self.arr[y][x] is not None and self.arr[y][x] != 0:
                    # Therefore set it to the node/edge region ID
                    self.arr[y][x] = self.arr[y][x].id

    def gen_maze(self):
        """
        Generate perfect mazes using Kruskals
        """
        self.set_nodes()
        self.set_edges()
        # Loop until all potential edges have been considered
        while len(self.edges) > 0:
            self.step()
        self.set_regions()

class Node:
    """
    Class used to represent a node on a graph
    """
    def __init__(self, region_id, x, y):
        """
        Initialize node object

        region_id -- the ID of the region the node belongs to
        x -- the x coordinate of the node within a 2d array
        y -- the y coordinate of the node within a 2d array
        """
        self.type = "node"
        self.id = region_id
        self.x = x
        self.y = y

class Edge:
    """
    Class used to represent an edge between two nodes
    """
    def __init__(self, x, y, direction):
        """
        Initialize edge object

        x -- the x coordinate of the edge within a 2d array
        y -- the y coordinate of the edge within a 2d array
        direction -- string ("v" or "h") representing the direction of the connection
        """
        self.type = "edge"
        self.x = x
        self.y = y
        self.id = None
        self.dir = direction
