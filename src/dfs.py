
# src/dfs.py

def find_articulation_points(graph):
    """
    Détecte les points d'articulation dans le graphe donné en utilisant un parcours DFS.
    
    :param graph: Instance de Graph (défini dans src/graph.py) avec les méthodes vertices() et neighbors(v)
    :return: Ensemble des points d'articulation (nœuds critiques)
    """
    visited = {}
    disc = {}
    low = {}
    parent = {}
    ap = set()  # Ensemble des points d'articulation
    time = [0]  # Compteur de temps sous forme de liste mutable

    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        children = 0

        for v in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                # Condition pour la racine
                if parent[u] is None and children > 1:
                    ap.add(u)
                # Condition pour un nœud non-racine
                if parent[u] is not None and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent.get(u, None):
                low[u] = min(low[u], disc[v])

    for u in graph.vertices():
        if u not in visited:
            parent[u] = None
            dfs(u)
    
    return ap
