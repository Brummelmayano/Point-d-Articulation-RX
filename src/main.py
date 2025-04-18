# src/main.py

import sys
import os
import time
from graph import Graph
from dfs import find_articulation_points
from updater import advanced_incremental_update_edge_addition
from state_manager import load_graph_state, save_graph_state, compare_graph_states, get_current_graph_state
from visualize import draw_graph

def compute_dfs_state(graph):
    """
    Effectue un DFS complet sur le graphe pour construire et retourner les dictionnaires:
      - disc  : temps de découverte pour chaque nœud,
      - low   : valeur minimale atteignable pour chaque nœud,
      - parent: parent de chaque nœud dans l'arbre DFS.
    
    Args:
        graph (Graph): Instance du graphe.
    
    Returns:
        tuple: (disc, low, parent)
    """
    visited = {}
    disc = {}
    low = {}
    parent = {}
    time = [0]

    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        for v in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
            elif v != parent.get(u, None):
                low[u] = min(low[u], disc[v])

    for u in graph.vertices():
        if u not in visited:
            parent[u] = None
            dfs(u)
    return disc, low, parent

def read_graph_from_file(file_path):
    """
    Lit un graphe depuis un fichier texte.

    Le format attendu est le suivant :
      - La première ligne contient deux entiers : le nombre de nœuds N et le nombre d'arêtes M.
      - Chaque ligne suivante contient deux entiers (u v) séparés par un espace.

    Args:
        file_path (str): Chemin vers le fichier.

    Returns:
        Graph: Une instance de Graph construite à partir du fichier.
    """
    g = Graph()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines:
            return g
        first_line = lines[0].strip()
        if not first_line:
            return g
        parts = first_line.split()
        if len(parts) < 2:
            raise ValueError("La première ligne doit contenir deux entiers : num_vertices et num_edges")
        num_vertices, num_edges = map(int, parts)
        for i in range(num_vertices):
            g.add_vertex(i)
        for line in lines[1:]:
            line = line.strip()
            if line:
                u, v = map(int, line.split())
                g.add_edge(u, v)
    return g

def main():
    """
    Point d'entrée principal du programme.

    Le programme lit un graphe depuis un fichier et génère dynamiquement un fichier d'état
    (en remplaçant l'extension .txt par .json). L'état sauvegardé est comparé à la structure
    du graphe actuel pour détecter une modification (ajout ou suppression d'arêtes).

    En cas de modification, et si une arête ajoutée est détectée, l'actualisation incrémentale
    est lancée pour recalculer uniquement le sous-arbre impacté à partir du LCA des nœuds de l'arête ajoutée.
    Le nouvel état DFS est ensuite sauvegardé.

    Usage:
         python src/main.py <graph_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <graph_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    print(f"Lecture du graphe depuis le fichier : {file_path}")
    graph = read_graph_from_file(file_path)
    
    print("Graphe chargé :")
    print(graph)

    # Affichage du nombre de sommets et d'arêtes
    print(f"Nombre de sommets : {len(graph.vertices())}")
    print(f"Nombre d’arêtes   : {sum(len(graph.neighbors(v)) for v in graph.vertices()) // 2}")
    
    # Génération dynamique du nom du fichier d'état (ex: data/example_graph.txt -> data/example_graph.json)
    base, ext = os.path.splitext(file_path)
    state_file = base + ".json"

    start_time = time.time()  # Début du chronométrage

    saved_state = load_graph_state(state_file)
    current_state = get_current_graph_state(graph)
    
    if saved_state is None:
        print("\nAucun état persistant trouvé. Exécution d'un DFS complet pour initialiser l'état...")
        disc, low, parent = compute_dfs_state(graph)
        save_graph_state(graph, disc, low, parent, state_file)
    else:
        saved_edges = set(tuple(edge) for edge in saved_state["graph"]["edges"])
        current_edges = set(tuple(edge) for edge in current_state["graph"]["edges"])
        
        if saved_edges != current_edges:
            added_edges = current_edges - saved_edges
            removed_edges = saved_edges - current_edges
            print("\nModifications détectées dans la structure du graphe :")
            if added_edges:
                print("Arêtes ajoutées :", added_edges)
            if removed_edges:
                print("Arêtes supprimées :", removed_edges)
            
            if added_edges:
                mod_edge = next(iter(added_edges))
                print(f"\nActualisation incrémentale pour l'ajout de l'arête {mod_edge}...")
                dfs_saved = saved_state["dfs_state"]
                disc = {int(k): v for k, v in dfs_saved["disc"].items()}
                low = {int(k): v for k, v in dfs_saved["low"].items()}
                parent = {int(k): (None if dfs_saved["parent"][k] is None else int(dfs_saved["parent"][k]))
                          for k in dfs_saved["parent"]}
                updated_ap, updated_nodes_sorted = advanced_incremental_update_edge_addition(graph, mod_edge[0], mod_edge[1], disc, low, parent)
                # Mise à jour visuelle avec coloration
                draw_graph(file_path, articulation_points=updated_ap, highlighted_nodes=updated_nodes_sorted)
                print("\nPoints d'articulation après actualisation incrémentale :")
                print(sorted(updated_ap))
            else:
                print("\nModification(s) détectée(s) (suppression ou modifications diverses), recalcul complet du DFS...")
                disc, low, parent = compute_dfs_state(graph)
            save_graph_state(graph, disc, low, parent, state_file)
        else:
            print("\nAucune modification détectée par rapport à l'état sauvegardé.")
            dfs_saved = saved_state["dfs_state"]
            disc = {int(k): v for k, v in dfs_saved["disc"].items()}
            low = {int(k): v for k, v in dfs_saved["low"].items()}
            parent = {int(k): (None if dfs_saved["parent"][k] is None else int(dfs_saved["parent"][k]))
                      for k in dfs_saved["parent"]}

    ap = find_articulation_points(graph)
    print("\nPoints d'articulation détectés :")
    print(sorted(ap))

    end_time = time.time()
    print(f"\nTemps moyen d'exécution : {end_time - start_time:.4f} secondes")

if __name__ == '__main__':
    main()
