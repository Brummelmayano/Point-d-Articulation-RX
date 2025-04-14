
# src/state_manager.py

import json
from graph import Graph

def save_graph_state(graph, disc, low, parent, filename):
    """
    Sauvegarde l'état du graphe et de la structure DFS dans un fichier JSON.
    
    :param graph: Instance de Graph.
    :param disc: Dictionnaire des temps de découverte.
    :param low: Dictionnaire des valeurs low.
    :param parent: Dictionnaire des parents dans l'arbre DFS.
    :param filename: Nom complet du fichier de sauvegarde (par exemple "data/example_graph.json").
    """
    state = {
        "graph": {
            "vertices": graph.vertices(),
            "edges": sorted([tuple(sorted(edge)) for edge in [(u, v) for u in graph.vertices() 
                                                                for v in graph.neighbors(u) if u < v]])
        },
        "dfs_state": {
            "disc": {str(k): v for k, v in disc.items()},
            "low": {str(k): v for k, v in low.items()},
            "parent": {str(k): (parent[k] if parent[k] is None else parent[k]) for k in parent}
        }
    }
    with open(filename, "w") as f:
        json.dump(state, f, indent=2)

def load_graph_state(filename):
    """
    Charge l'état du graphe sauvegardé depuis un fichier JSON.
    
    :param filename: Nom complet du fichier de sauvegarde (par exemple "data/example_graph.json").
    :return: L'état sauvegardé ou None si le fichier n'existe pas.
    """
    try:
        with open(filename, "r") as f:
            state = json.load(f)
        return state
    except FileNotFoundError:
        return None

def compare_graph_states(current_state, saved_state):
    """
    Compare la structure du graphe actuel et celle sauvegardée sur la base de la liste d'arêtes.
    Retourne True s'il y a modification, False sinon.
    """
    current_edges = set([tuple(sorted(edge)) for edge in current_state["graph"]["edges"]])
    saved_edges = set([tuple(sorted(edge)) for edge in saved_state["graph"]["edges"]])
    return current_edges != saved_edges

def get_current_graph_state(graph):
    """
    Construit et retourne un dictionnaire représentant l'état actuel du graphe.
    """
    state = {
        "graph": {
            "vertices": graph.vertices(),
            "edges": sorted([tuple(sorted(edge)) for edge in [(u, v) for u in graph.vertices() 
                                                                for v in graph.neighbors(u) if u < v]])
        }
    }
    return state
