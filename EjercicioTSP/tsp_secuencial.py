import itertools
import math
import time

# Calcula la distancia euclidiana entre dos puntos (x, y)
def calcular_distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Calcula la distancia total de una ruta (incluyendo regreso al origen)
def distancia_total(ruta, ciudades):
    distancia = 0
    for i in range(len(ruta) - 1):
        distancia += calcular_distancia(ciudades[ruta[i]], ciudades[ruta[i + 1]])
    distancia += calcular_distancia(ciudades[ruta[-1]], ciudades[ruta[0]])
    return distancia

# Encuentra la ruta mas corta recorriendo todas las permutaciones posibles
def tsp_secuencial(ciudades): 
    indices = list(range(len(ciudades)))
    mejor_ruta = None
    mejor_distancia = float("inf")

    inicio = time.time()

    for ruta in itertools.permutations(indices):
        distancia = distancia_total(ruta, ciudades)
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_ruta = ruta

    fin = time.time()
    duracion = fin - inicio

    return mejor_ruta, mejor_distancia, duracion

if __name__ == "__main__":
    ciudades = [(0, 0), (2, 3), (5, 4), (1, 6), (4, 7), (2, 1), (4, 6), (5, 5)]

    print("Algoritmo Secuencial: ")
    mejor_ruta, mejor_distancia, tiempo = tsp_secuencial(ciudades)

    print(f"Mejor ruta: {mejor_ruta}")
    print(f"Distancia mínima: {mejor_distancia:.4f}")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")
