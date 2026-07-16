import json

def load_formulas():
    with open("formulas.json", "r", encoding="utf-8") as f:
        return json.load(f)