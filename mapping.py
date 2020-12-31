import json

mapper = {
    "swan ton pacific ranch": "Swanton Pacific Ranch",
    "Swanton Pacific Ranch": "Swanton Pacific Ranch",
    "Swanton Pacifico": "Swanton Pacific Ranch",
    "green house" : "Green House",
    "cheese house" : "Cheese House",
    "cause uh very day": "Casa Verde",
    "cause very day" : "Casa Verde",
    "as a very dead" : "Casa Verde",
    "as a very gay" : "Casa Verde",
    "Casa Verde": "Casa Verde",
    "romona roderigo" : "Ramon Rodriguez"
}

def map(substring):

    with open("test_json.json", "w") as in_json:
        json.dump(mapper, in_json)

    return mapper[substring]