# tests/test_graph.py

import pytest
from src.graph import Graph

def test_add_vertex():
    g = Graph()
    g.add_vertex(1)
    assert 1 in g.adj
    assert g.adj[1] == set()

def test_add_edge():
    g = Graph()
    g.add_edge(1, 2)
    # Vérifie que les deux sommets existent et sont connectés
    assert 1 in g.adj and 2 in g.adj
    assert 2 in g.adj[1]
    assert 1 in g.adj[2]

def test_remove_edge():
    g = Graph()
    g.add_edge(1, 2)
    g.remove_edge(1, 2)
    assert 2 not in g.adj[1]
    assert 1 not in g.adj[2]

def test_neighbors():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    neighbors = g.neighbors(1)
    # Les voisins doivent contenir 2 et 3
    assert set(neighbors) == {2, 3}

def test_str_representation():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    s = str(g)
    # Vérifie que la représentation en chaîne de caractères contient les informations attendues
    assert "1:" in s and ("2" in s or "3" in s)
