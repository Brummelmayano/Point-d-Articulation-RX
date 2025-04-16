import sys
import matplotlib.pyplot as plt 
import networkx as nx
from graph import Graph
from dfs import find_articulation_points
from matplotlib.patches import Patch


def read_graph_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    first_line = lines[0].strip().split()
    n, m = int(first_line[0]), int(first_line[1])
    edges = [tuple(map(int, line.strip().split())) for line in lines[1:]]
    return n, edges

def draw_graph(filepath):
    # Lecture et création du graphe personnalisé
    n, edges = read_graph_from_file(filepath)
    custom_graph = Graph()
    for i in range(n):
        custom_graph.add_vertex(i)
    for u, v in edges:
        custom_graph.add_edge(u, v)

    # Détection des points d'articulation avec notre propre fonction
    articulation_points = find_articulation_points(custom_graph)

    # Création d'un graphe NetworkX pour la visualisation
    G_nx = nx.Graph()
    G_nx.add_nodes_from(range(n))
    G_nx.add_edges_from(edges)

    # Positionnement automatique des nœuds
    pos = nx.spring_layout(G_nx, seed=42)

    # Définition des couleurs : rouge pour les points d'articulation, bleu clair pour le reste
    node_colors = ['red' if node in articulation_points else 'lightblue' for node in G_nx.nodes()]

    # Dessin du graphe
    nx.draw(G_nx, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=700, font_size=10)
    
    # Ajout de la légende
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='Point d\'articulation'),
        Patch(facecolor='lightblue', edgecolor='black', label='Autre sommet')
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.title("Graphe avec points d'articulation en rouge")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/visualize.py <graph_file>")
        sys.exit(1)
    graph_file = sys.argv[1]
    draw_graph(graph_file)
