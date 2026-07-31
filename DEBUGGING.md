# Méthode debugging pour être sûr de savoir ce que Python execute
#==============================================================

# DEBUG pour afficher le contenu complet du scenario.py utilisé
print(explorer.scenarios.__file__)
from pathlib import Path

with open(explorer.scenarios.__file__, "r", encoding="utf-8") as f:
    print(f.read()[:600])


# Voir les 40 1ères lignes de code de load_scenario dans scenario.py
import inspect
import explorer.scenarios

print(inspect.getsource(explorer.scenarios.load_scenario))
