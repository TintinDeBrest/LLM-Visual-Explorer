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

# To debug plot scene issue w category colors
print(df.head())
print(df.columns)
print(df[["PC1", "PC2", "PC3"]])
import plotly.io as pio
print(df["Catégorie"].unique())
print(CATEGORY_COLORS.keys())
