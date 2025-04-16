# Point d'Articulation RX

Point d'Articulation RX est une application Python dédiée à la détection et à la gestion incrémentale des points d'articulation dans des graphes. Ce projet est conçu pour :

- **Parcours DFS complet** : Calculer les temps de découverte (`disc`) et les valeurs "low" pour chaque nœud d'un graphe.
- **Détection des points d'articulation** : Identifier les nœuds critiques dont la suppression fragmente le graphe.
- **Actualisation incrémentale** : Lorsqu'une modification (ajout ou suppression d'une arête) est détectée dans le fichier de données, l'algorithme ne recalculera que la zone impactée (définie par le Lowest Common Ancestor, LCA) afin d'optimiser le temps de traitement.
- **Persistance de l'état** : Sauvegarder et recharger l'état du graphe et de la structure DFS (les dictionnaires `disc`, `low` et `parent`) au format JSON, pour comparer l'état actuel du graphe avec l'état sauvegardé lors de l'exécution précédente.
- **Visualisation graphique** : Afficher le graphe à l'aide de NetworkX et Matplotlib en mettant en évidence les points d'articulation détectés par notre propre algorithme (colorés en rouge), avec une légende explicative.

## Fonctionnalités

- **Initialisation (DFS complet)**
  - Parcours en profondeur du graphe pour calculer les tableaux `disc` et `low`.
  - Identification des points d'articulation selon les conditions classiques.
  
- **Actualisation incrémentale (Phase 2)**
  - Détection des modifications dans la structure du graphe en comparant l'état actuel à celui sauvegardé.
  - Recalcule local, via un DFS partiel lancé à partir du LCA des nœuds affectés, pour mettre à jour uniquement la zone impactée.
  - Affichage des nœuds recalculés et du nombre total de nœuds mis à jour, afin de prouver que l'actualisation est limitée.
  
- **Gestion persistante**
  - Sauvegarde de l'état du graphe (liste des sommets et arêtes) et de la structure DFS dans un fichier JSON (le nom du fichier d'état est généré en remplaçant l'extension `.txt` par `.json`).
  - Rechargement et comparaison de l'état entre plusieurs exécutions pour déclencher des mises à jour incrémentales si des modifications sont détectées.
  
- **Visualisation**
  - Représentation graphique du graphe à l'aide de NetworkX et Matplotlib.
  - Les points d'articulation identifiés par notre algorithme personnalisé sont affichés en rouge, avec une légende indiquant que le rouge correspond aux points d'articulation.

## Installation

### 🔁 Cloner le dépôt :
   ```bash
   git clone https://github.com/Brummelmayano/Point-d-Articulation-RX.git
   cd point_articulation_rx
   ```
### 📦 Installer les dépendances : Assurez-vous d’avoir Python 3.7+ installé, puis lancez :
   ```bash
  pip install -r requirements.txt
   ```

## Utilisation

### ▶️ Exécution du Programme Principal

   ```bash
  python src/main.py data/example_graph.txt
   ```


### 👁️ Visualisation Graphique
   ```bash
    python src/visualize.py data/example_graph.txt
   ```


### 🧪 Lancer les Tests Unitaires
   ```bash
  pytest tests/
   ```
## Création d’un Nouveau Graphe

Pour tester notre algorithme avec un nouveau graphe, il vous suffit de créer un fichier texte (.txt) contenant le graphe au format suivant :

- La première ligne doit comporter deux entiers séparés par un espace : le nombre total de nœuds et le nombre total d’arêtes.
- Chaque ligne suivante doit représenter une arête, indiquée par deux entiers (séparés par un espace) correspondant aux identifiants des nœuds reliés.

Par exemple, voici un fichier simple décrivant un graphe de 5 nœuds et 4 arêtes :
   ```bash
    5 4
    0 1
    0 2
    1 3
    2 4
   ```

Vous pouvez enregistrer ce fichier n’importe où sur votre système, par exemple sous le nom \texttt{mon\_graphe.txt}. 
Pour lancer l'algorithme sur ce nouveau graphe, utilisez la commande suivante: :

```bash
python src/main.py <chemin_complet_vers_le_fichier>/mon_graphe.txt
```
