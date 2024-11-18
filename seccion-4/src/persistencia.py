import json
from pathlib import Path

BASE_DIR = Path(__name__).parent.parent / "turnos.json"


def cargar_turnos():
    try:
        with open(BASE_DIR, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"pediatria": [], "laboratorio": [], "geriatria": [], "fisioterapia": []}


def guardar_turnos(data):
    with open(BASE_DIR, "w") as file:
        json.dump(data, file, indent=4)
