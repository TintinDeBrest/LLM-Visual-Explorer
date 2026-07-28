# scenarios
SCENARIOS = {

    "analogie_royale": {
        "titre": "Analogie royale",
        "mots": [
            "roi",
            "reine",
            "homme",
            "femme"
        ],
        "categories": [
            "Royal",
            "Royal",
            "Humain",
            "Humain"
        ]
    },

    "fruits": {
        "titre": "Les fruits",
        "mots": [
            "pomme",
            "orange",
            "banane",
            "poire",
            "citron"
        ],
        "categories": [
            "Fruit",
            "Fruit",
            "Fruit",
            "Fruit",
            "Fruit"
        ]
    },

    "animaux": {
        "titre": "Les animaux",
        "mots": [
            "chat",
            "chien",
            "lion",
            "loup",
            "renard"
        ],
        "categories": [
            "Animal",
            "Animal",
            "Animal",
            "Animal",
            "Animal"
        ]
    },

    "mixte": {
        "titre": "Humains et fruits",
        "mots": [
            "roi",
            "reine",
            "homme",
            "femme",
            "pomme",
            "orange"
        ],
        "categories": [
            "Royal",
            "Royal",
            "Humain",
            "Humain",
            "Fruit",
            "Fruit"
        ]
    }

}

def get_scenarios():
    return list(SCENARIOS.keys())


def load_scenario(name):

    return SCENARIOS[name]
