import itertools
import math
import time
from multiprocessing import Pool, cpu_count

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

# Calcula la mejor ruta dentro de un subconjunto de rutas
def mejor_en_subconjunto(subrutas_ciudades):
    subrutas, ciudades = subrutas_ciudades
    mejor_ruta = None
    mejor_distancia = float("inf")

    for ruta in subrutas:
        distancia = distancia_total(ruta, ciudades)
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_ruta = ruta

    return mejor_ruta, mejor_distancia

# Divide la lista de rutas en subconjuntos equilibrados para cada proceso
def dividir_rutas(rutas, partes):
   
    tamaño = len(rutas)
    base = tamaño // partes
    resto = tamaño % partes
    sublistas = []
    inicio = 0
    for i in range(partes):
        extra = 1 if i < resto else 0
        fin = inicio + base + extra
        sublistas.append(rutas[inicio:fin])
        inicio = fin
    return sublistas

# Resuelve el TSP por fuerza bruta usando procesamiento paralelo
def tsp_paralelo(ciudades, num_procesos=None):
    if num_procesos is None:
        num_procesos = cpu_count()

    indices = list(range(len(ciudades)))
    rutas = list(itertools.permutations(indices))

    sublistas = dividir_rutas(rutas, num_procesos)
    paquetes = [(sublista, ciudades) for sublista in sublistas]

    inicio = time.time()

    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(mejor_en_subconjunto, paquetes)

    mejor_ruta = None
    mejor_distancia = float("inf")

    for ruta, dist in resultados:
        if dist < mejor_distancia:
            mejor_ruta = ruta
            mejor_distancia = dist

    fin = time.time()
    duracion = fin - inicio

    return mejor_ruta, mejor_distancia, duracion

if __name__ == "__main__":
    ciudades = [(0, 0), (2, 3), (5, 4), (1, 6), (4, 7), (2, 1), (4, 6), (5, 5)]

    print("Algoritmo Paralelo")
    mejor_ruta, mejor_distancia, tiempo = tsp_paralelo(ciudades, num_procesos=4)

    print(f"Mejor ruta: {mejor_ruta}")
    print(f"Distancia mínima: {mejor_distancia:.4f}")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")
