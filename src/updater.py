
# src/updater.py

from dfs import find_articulation_points

def get_path_to_root(node, parent):
    """
    Renvoie la liste des nœuds allant du nœud donné jusqu'à la racine de l'arbre DFS.
    """
    path = []
    while node is not None:
        path.append(node)
        node = parent.get(node)
    return path

def find_lca(x, y, parent, disc):
    """
    Trouve le Lowest Common Ancestor (LCA) de deux nœuds x et y dans l'arbre DFS.
    
    Args:
        x (int): Premier nœud.
        y (int): Deuxième nœud.
        parent (dict): Dictionnaire des parents.
        disc (dict): Dictionnaire des temps de découverte.
    
    Returns:
        int: Le nœud LCA ou None s'il n'en existe pas.
    """
    path_x = get_path_to_root(x, parent)
    path_y = set(get_path_to_root(y, parent))
    common = [node for node in path_x if node in path_y]
    if not common:
        return None
    lca = max(common, key=lambda node: disc[node])
    return lca

def partial_dfs_update(graph, u, new_disc, new_low, new_parent, visited, time, counter, updated_nodes, original_parent):
    """
    Effectue un DFS partiel à partir du nœud 'u', recalculant les valeurs new_disc et new_low
    uniquement pour les nœuds appartenant au sous-arbre défini par l'état DFS initial (original_parent).

    Args:
        graph (Graph): Le graphe.
        u (int): Le nœud de départ pour la mise à jour.
        new_disc (dict): Dictionnaire local pour les temps de découverte recalculés.
        new_low (dict): Dictionnaire local pour les valeurs low recalculées.
        new_parent (dict): Dictionnaire local pour les parents recalculés.
        visited (set): Ensemble des nœuds déjà visités dans le DFS partiel.
        time (list): Liste contenant la valeur du temps courant (mutable).
        counter (list): Liste utilisée comme compteur (le premier élément compte le nombre de nœuds traités).
        updated_nodes (list): Liste des nœuds recalculés (pour affichage).
        original_parent (dict): Dictionnaire des parents issu de l'état DFS initial, pour restreindre le DFS.
    
    Returns:
        None
    """
    if u in visited:
        return
    visited.add(u)
    counter[0] += 1
    updated_nodes.append(u)
    
    new_disc[u] = new_low[u] = time[0]
    time[0] += 1
    print(f"Traitement du nœud {u} : new_disc={new_disc[u]}, new_low={new_low[u]}")
    
    for v in graph.neighbors(u):
        # Ne traiter que les voisins qui appartiennent au sous-arbre de u dans l'état DFS initial.
        if original_parent.get(v) != u:
            continue
        if v not in visited:
            new_parent[v] = u
            partial_dfs_update(graph, v, new_disc, new_low, new_parent, visited, time, counter, updated_nodes, original_parent)
            new_low[u] = min(new_low[u], new_low[v])
        elif v != new_parent.get(u, None):
            new_low[u] = min(new_low[u], new_disc[v])
    
    print(f"Nœud {u} terminé : new_disc={new_disc[u]}, new_low={new_low[u]}")

def advanced_incremental_update_edge_addition(graph, x, y, disc, low, parent):
    """
    Met à jour de manière incrémentale l'état DFS après l'ajout d'une arête (x, y) 
    en recalculant uniquement la sous-arborescence impactée à partir du LCA des deux nœuds,
    limitée au sous-arbre défini par l'état DFS initial.

    Args:
        graph (Graph): Le graphe.
        x (int): Un des nœuds de la nouvelle arête.
        y (int): L'autre nœud.
        disc (dict): Dictionnaire global des temps de découverte.
        low (dict): Dictionnaire global des valeurs low.
        parent (dict): Dictionnaire global des parents dans l'arbre DFS (état initial).

    Returns:
        list: Liste des points d'articulation détectés après actualisation incrémentale.
    """
    lca = find_lca(x, y, parent, disc)
    if lca is None:
        return find_articulation_points(graph)

    print(f"LCA pour les nœuds {x} et {y} est {lca}")

    visited = set()
    counter = [0]
    updated_nodes = []
    new_disc = {}
    new_low = {}
    new_parent = {}
    # Reprise du temps à partir du LCA
    time = [disc[lca]]
    
    partial_dfs_update(graph, lca, new_disc, new_low, new_parent, visited, time, counter, updated_nodes, parent)

    updated_nodes_sorted = sorted(updated_nodes)
    print(f"DFS partiel mis à jour sur {counter[0]} nœuds à partir du LCA {lca}")
    print(f"Nœuds recalculés : {updated_nodes_sorted}")
    print(f"Nombre total de nœuds recalculés : {len(updated_nodes_sorted)}")
    
    # Intégration : mettre à jour uniquement les nœuds recalculés dans l'état global
    for node in new_disc:
        disc[node] = new_disc[node]
        low[node] = new_low[node]
        parent[node] = new_parent[node] if node in new_parent else parent.get(node, None)
    
    return find_articulation_points(graph)
