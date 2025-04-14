
# src/graph.py

class Graph:
    def __init__(self):
        # Dictionnaire : clé = sommet, valeur = ensemble des voisins
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = set()

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].add(v)
        self.adj[v].add(u)

    def remove_edge(self, u, v):
        if u in self.adj and v in self.adj[u]:
            self.adj[u].remove(v)
        if v in self.adj and u in self.adj[v]:
            self.adj[v].remove(u)

    def vertices(self):
        return list(self.adj.keys())

    def neighbors(self, v):
        return list(self.adj.get(v, []))

    def __str__(self):
        return "\n".join(f"{v}: {neighbors}" for v, neighbors in self.adj.items())
