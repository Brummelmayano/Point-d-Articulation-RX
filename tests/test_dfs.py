# tests/test_dfs.py

import pytest
from src.graph import Graph
from src.dfs import find_articulation_points

def build_star_graph():
    """
    Construit un graphe en étoile (center 0 relié à 1, 2, 3, 4).
    Le centre (0) est un point d'articulation.
    """
    g = Graph()
    # Ajoute des arêtes reliant le centre (0) aux feuilles 1, 2, 3 et 4.
    for i in range(1, 5):
        g.add_edge(0, i)
    return g

def build_cycle_graph():
    """
    Construit un graphe cyclique (0-1-2-3-0).
    Aucun sommet n'est un point d'articulation.
    """
    g = Graph()
    edges = [(0,1), (1,2), (2,3), (3,0)]
    for u, v in edges:
        g.add_edge(u, v)
    return g

def build_custom_graph():
    """
    Construit un graphe personnalisé :
         1
        / \
       0   2
           |
           3
          / \
         4   5
         
    Ici, 1, 2 et 3 sont des points d'articulation.
    """
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    return g

def test_find_articulation_points_star():
    g = build_star_graph()
    articulation_points = find_articulation_points(g)
    # Dans un graphe en étoile, le centre (0) est le seul point d'articulation.
    assert articulation_points == {0}

def test_find_articulation_points_cycle():
    g = build_cycle_graph()
    articulation_points = find_articulation_points(g)
    # Dans un graphe cyclique, aucun point d'articulation.
    assert articulation_points == set()

def test_find_articulation_points_custom():
    g = build_custom_graph()
    articulation_points = find_articulation_points(g)
    # Pour le graphe personnalisé, les points d'articulation attendus sont 2 et 3.
    assert articulation_points == {1, 2, 3}
