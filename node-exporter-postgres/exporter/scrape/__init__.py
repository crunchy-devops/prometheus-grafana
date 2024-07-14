import os
import sys

# Obtenir le chemin absolu du répertoire principal
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ajouter le répertoire principal au chemin de recherche de modules
sys.path.insert(0, main_directory)
