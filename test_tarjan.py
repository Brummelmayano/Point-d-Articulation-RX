import networkx as nx
import time
from statistics import mean
import os

def load_graph_from_file(filepath):
    G = nx.Graph()
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        # Lire la première ligne pour obtenir le nombre de sommets
        n_nodes, n_edges = map(int, lines[0].split())
        G.add_nodes_from(range(n_nodes))  # Ajout explicite des sommets

        # Lire les arêtes
        for line in lines[1:]:
            u, v = map(int, line.split())
            G.add_edge(u, v)

    return G

def run_tarjan_ap(G, runs=10):
    durations = []
    for _ in range(runs):
        start = time.perf_counter()
        ap = list(nx.articulation_points(G))
        end = time.perf_counter()
        durations.append((end - start) * 1000)  # en millisecondes
    return ap, mean(durations)

def precision_recall(predicted, ground_truth):
    predicted_set = set(predicted)
    ground_set = set(ground_truth)
    true_positive = len(predicted_set & ground_set)
    precision = true_positive / len(predicted_set) if predicted_set else 0
    recall = true_positive / len(ground_set) if ground_set else 0
    return precision, recall

def main():
    folder = "data"
    ground_truths = {
        "example_graph.txt": [1, 3],
        "example_graph2.txt": [1, 3]
    }

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            G = load_graph_from_file(path)
            ap, avg_time = run_tarjan_ap(G)

            print(f"\n Graphe: {filename}")
            print(f"Sommet: {G.number_of_nodes()}, Arêtes: {G.number_of_edges()}")
            print(f"Points d'articulation détectés : {sorted(ap)}")
            print(f"Temps moyen d'exécution : {avg_time:.3f} ms")

            if filename in ground_truths:
                precision, recall = precision_recall(ap, ground_truths[filename])
                print(f" Précision : {precision:.2f}, Rappel : {recall:.2f}")

if __name__ == "__main__":
    main()
