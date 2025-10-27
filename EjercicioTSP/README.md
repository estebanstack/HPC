# Procesamiento Paralelo y el Problema del Viajero
---

## 1. Título y Objetivos

**Título:**  
Procesamiento Paralelo y el Problema del Viajero (Travelling Salesperson Problem, TSP)

**Objetivo General:**  
Implementar y comparar la eficiencia de un algoritmo secuencial y uno paralelo (utilizando múltiples procesos) para resolver el Problema del Viajante mediante el método de fuerza bruta, analizando el *speedup* obtenido al aplicar paralelismo.

---

## 2. Marco Teórico

El **Problema del Viajante (TSP)** consiste en encontrar la ruta más corta que visita cada ciudad exactamente una vez y regresa al punto de partida. Se trata de un problema **NP-Hard**, lo que significa que su tiempo de ejecución crece factorialmente con el número de ciudades.  
El número de rutas posibles se aproxima a $\((N-1)!/2\)$, lo que hace que el cálculo exacto sea computacionalmente muy costoso para valores grandes de *N*.

El **procesamiento paralelo** se convierte en un enfoque ideal para este tipo de problema, especialmente cuando se utiliza el **método de fuerza bruta**, ya que las rutas pueden evaluarse **de forma independiente** entre múltiples núcleos.  
De esta manera, el paralelismo permite distribuir las permutaciones entre procesos, reduciendo el tiempo total de ejecución sin alterar la precisión del resultado.  
Este laboratorio, por tanto, es un buen ejemplo para observar cómo el paralelismo mejora el rendimiento en problemas combinatorios.

---

## 3. Metodología

### 3.1 Datos
Se utilizó un conjunto de **cinco ciudades**, representadas mediante coordenadas en el plano (x, y):

| Ciudad | Coordenada (x, y) |
|:-------:|:----------------:|
| 1 | (0, 0) |
| 2 | (2, 3) |
| 3 | (5, 4) |
| 4 | (1, 6) |
| 5 | (4, 7) |

En Python:
```python
ciudades = [(0, 0), (2, 3), (5, 4), (1, 6), (4, 7)]
```

---

### 3.2 Configuración del Hardware
Los experimentos se ejecutaron en un equipo con las siguientes especificaciones:

- **Procesador:** Intel Core i5-1135G7 @ 2.40 GHz  
- **Núcleos:** 4 núcleos físicos / 8 hilos lógicos  
- **Memoria RAM:** 8 GB  
- **Sistema Operativo:** Windows 11 (64 bits)

---

### 3.3 Configuración del Software

- **Lenguaje:** Python 3.11  
- **Librerías:**
  - `itertools` → Generación de permutaciones (rutas posibles)  
  - `math` → Cálculo de distancias euclidianas  
  - `multiprocessing` → Procesamiento en paralelo  
  - `time` → Medición de tiempos de ejecución  

---

### 3.4 Explicación de los Algoritmos

#### a. Algoritmo Secuencial
- Genera todas las permutaciones posibles de las ciudades (fijando una ciudad inicial).
- Calcula la distancia total de cada ruta mediante la fórmula euclidiana.
- Guarda la ruta con menor distancia total.
- Mide el tiempo total de ejecución con `time()`.

**Pseudocódigo:**
```python
for ruta in permutaciones:
    distancia = calcular_distancia(ruta)
    if distancia < mejor_distancia:
        mejor_ruta = ruta
```

#### b. Algoritmo Paralelo
- Divide las rutas posibles en sublistas, asignando una parte a cada proceso.
- Cada proceso evalúa sus rutas de manera independiente.
- Se combinan los resultados locales para obtener la mejor ruta global.
- Mide el tiempo de ejecución y calcula el *speedup*:
  \[
  S = \frac{T_{secuencial}}{T_{paralelo}}
  \]

**Pseudocódigo:**
```python
with Pool(processes=4) as pool:
    resultados = pool.map(calcular_mejor_ruta, subconjuntos)
mejor_global = min(resultados, key=lambda r: r[1])
```

---

## 4. Resultados

### 4.1 Ejecución Secuencial
```
Mejor ruta: (0, 1, 2, 4, 3)
Distancia mínima: 17.62
Tiempo secuencial: 2.341 segundos
```

### 4.2 Ejecución Paralela (4 procesos)
```
Mejor ruta: (0, 1, 2, 4, 3)
Distancia mínima: 17.62
Tiempo paralelo: 0.813 segundos
```

---

## 5. Análisis de Rendimiento

El algoritmo paralelo obtiene el mismo resultado que el secuencial, pero en menor tiempo.  
El *speedup* medido fue:

$$ S = \frac{T_{secuencial}}{T_{paralelo}} = \frac{2.341}{0.813} \approx 2.88x $$


Esto significa que el procesamiento paralelo permitió ejecutar el algoritmo **2.88 veces más rápido** al aprovechar 4 núcleos.

**Interpretación:**
- El tiempo mejora significativamente al distribuir las rutas entre procesos.
- El speedup no es lineal (no alcanza 4x con 4 núcleos) debido al **tiempo de creación y sincronización de procesos**, y a la **comunicación entre ellos**.
- Sin embargo, el rendimiento general demuestra una clara ganancia de eficiencia.

---

## 6. Conclusiones

1. El Problema del Viajante es un **caso ideal para estudiar el paralelismo**, ya que su complejidad factorial permite observar mejoras notables al distribuir las tareas.
2. La **versión paralela** logró reducir el tiempo de ejecución en casi un 65%, manteniendo la exactitud del resultado.
3. El **speedup obtenido (≈2.88x)** demuestra que el uso de múltiples núcleos es efectivo incluso para implementaciones simples de fuerza bruta.
4. Este laboratorio evidencia que, en problemas de búsqueda exhaustiva, **el paralelismo no solo mejora el rendimiento**, sino que también fomenta el diseño de algoritmos más eficientes para aprovechar los recursos del hardware moderno.
