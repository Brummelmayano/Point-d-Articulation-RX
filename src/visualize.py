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

def draw_graph(filepath, articulation_points=None, highlighted_nodes=None):
    # Lecture et création du graphe personnalisé
    n, edges = read_graph_from_file(filepath)
    custom_graph = Graph()
    for i in range(n):
        custom_graph.add_vertex(i)
    for u, v in edges:
        custom_graph.add_edge(u, v)

    # Si les points d'articulation ne sont pas fournis, on les calcule
    if articulation_points is None:
        articulation_points = find_articulation_points(custom_graph)

    # Création d'un graphe NetworkX pour la visualisation
    G_nx = nx.Graph()
    G_nx.add_nodes_from(range(n))
    G_nx.add_edges_from(edges)

    # Positionnement automatique des nœuds
    pos = nx.spring_layout(G_nx, seed=42)

    # Définition des couleurs : jaune > rouge > bleu clair
    node_colors = []
    for node in G_nx.nodes():
        if highlighted_nodes and node in highlighted_nodes:
            node_colors.append('yellow')  # Sommets recalculés
        elif node in articulation_points:
            node_colors.append('red')  # Points d'articulation
        else:
            node_colors.append('lightblue')  # Autres sommets

    # Dessin du graphe
    nx.draw(G_nx, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=200, font_size=10)

    # Légende
    legend_elements = [
        Patch(facecolor='yellow', edgecolor='black', label='Sommets recalculés'),
        Patch(facecolor='red', edgecolor='black', label='Point d\'articulation'),
        Patch(facecolor='lightblue', edgecolor='black', label='Autre sommet')
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.title("Graphe mis à jour avec coloration")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/visualize.py <graph_file>")
        sys.exit(1)
    graph_file = sys.argv[1]
    draw_graph(graph_file)
