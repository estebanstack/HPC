from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def distancia_euclidiana(c1, c2):
    return math.sqrt((c1["x"] - c2["x"])**2 + (c1["y"] - c2["y"])**2)

@app.route("/calculate_distance", methods=["POST"])
def calcular_distancia():
    data = request.get_json()

    ciudades = data["cities"]  # Lista de ciudades en orden
    total = 0.0

    for i in range(len(ciudades) - 1):
        total += distancia_euclidiana(ciudades[i], ciudades[i+1])

    return jsonify({"total_distance": total})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
