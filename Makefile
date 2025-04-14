# Makefile pour point_articulation_rx

.PHONY: run test visualize clean

# Exécute le programme principal en utilisant le fichier de graphe d'exemple.
run:
	@echo "Lancement du programme..."
	python src/main.py data/example_graph.txt

# Exécute les tests unitaires (assurez-vous que pytest est installé).
test:
	@echo "Exécution des tests..."
	pytest tests/

# Lance le module de visualisation pour afficher graphiquement le graphe.
visualize:
	@echo "Visualisation du graphe..."
	python src/visualize.py data/example_graph.txt

# Nettoie les fichiers compilés et les répertoires __pycache__.
clean:
	@echo "Nettoyage des fichiers temporaires..."
	-find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Nettoyage terminé."
