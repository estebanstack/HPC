import itertools
import requests

ciudades = [
    {"id": "A", "x": 0, "y": 0},
    {"id": "B", "x": 3, "y": 4},
    {"id": "C", "x": 6, "y": 0},
    {"id": "D", "x": 2, "y": 1},
]

url = "http://localhost:5001/calculate_distance"

mejor_distancia = float("inf")
mejor_ruta = None

for perm in itertools.permutations(ciudades):
    data = {"cities": list(perm)}
    response = requests.post(url, json=data)
    response_data = response.json()

    distancia = response_data["total_distance"]

    if distancia < mejor_distancia:
        mejor_distancia = distancia
        mejor_ruta = perm

print("\nMejor ruta encontrada:")
print([c["id"] for c in mejor_ruta])
print(f"Distancia total: {mejor_distancia}")
