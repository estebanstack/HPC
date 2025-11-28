# Procesamiento Paralelo y el Problema del Viajero
---

## 1. Objetivos

**Objetivo General:**  
  - Implementar y comparar la eficiencia de un algoritmo secuencial y uno paralelo (utilizando múltiples procesos) para resolver el Problema del Viajante mediante el método de fuerza bruta, analizando el *speedup* obtenido al aplicar paralelismo.

**Objetivos Específicos**
  - Implementar y ejecutar dos versiones del algoritmo de fuerza bruta para el Problema del Viajante (TSP): una secuencial y otra paralela, midiendo y comparando el tiempo de ejecución de ambas
  - Analizar el impacto del procesamiento paralelo en la eficiencia computacional, evaluando el speedup obtenido al utilizar múltiples núcleos del procesador frente a la ejecución secuencial.
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
Se utilizó un conjunto de **ocho ciudades**, representadas mediante coordenadas en el plano (x, y):

| Ciudad | Coordenada (x, y) |
|:-------:|:----------------:|
| 1 | (0, 0) |
| 2 | (2, 3) |
| 3 | (5, 4) |
| 4 | (1, 6) |
| 5 | (4, 7) |
| 6 | (2, 1) |
| 7 | (4, 6) |
| 8 | (5, 5) |


En Python:
```python
ciudades = [(0, 0), (2, 3), (5, 4), (1, 6), (4, 7), (2, 1), (4, 6), (5, 5)]
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

En esta sección se explican detalladamente los dos algoritmos implementados en Python: tsp_secuencial.py y tsp_paralelo.py
Ambos resuelven el Problema del Viajero mediante fuerza bruta probando todas las rutas posibles
La diferencia entre ambos es cómo se ejecutan las permutaciones: uno las ejecuta en un solo proceso y el otro divide el trabajo en varios procesos paralelos

#### a. Algoritmo Secuencial
Este algoritmo recorre todas las posibles rutas (permutaciones) que se pueden generar con las ciudades

##### Funcionamiento:

  - Se genera una lista de índices de ciudades: indices = [0,1,2,...]

  - Con itertools.permutations(indices) se generan todas las rutas posibles.

  - Para cada ruta se calcula su distancia total, utilizando la fórmula de distancia euclidiana.

  - El algoritmo va guardando la ruta con la distancia más corta encontrada.

  - Se usa time.time() para medir cuánto demora el proceso completo.

**Idea del algoritmo**
```python
for ruta in todas_las_permutaciones:
    distancia = distancia_total(ruta)
    si distancia es menor que mejor_distancia:
        mejor_ruta = ruta
```

##### Conclusión secuencial:
Todo el trabajo lo hace un solo proceso, por eso es simple pero mientras más ciudades haya, la cantidad de rutas crece factorialmente → aumenta mucho el tiempo.

#### b. Algoritmo Paralelo
Este código hace lo mismo que el secuencial, pero divide el espacio de rutas en varias partes y cada parte es calculada por un proceso distinto usando multiprocessing

##### Funcionamiento:

  - Igual que el secuencial, genera TODAS las permutaciones posibles.

  - Usa dividir_rutas() para dividir esa lista en N subconjuntos (donde N es la cantidad de procesos).

  - Cada subconjunto se asigna a un proceso del Pool() para que calcule la mejor ruta dentro de ese subconjunto.

  - Luego se comparan los resultados de todos los procesos y se selecciona el mejor total.

  - También se mide el tiempo completo con time.time().

**Idea del algoritmo:**
```python
conjunto_rutas = todas_las_permutaciones
subconjuntos = dividir(conjunto_rutas, numero_procesos)

with Pool as pool:
    resultados_locales = pool.map(mejor_en_subconjunto, subconjuntos)

mejor_global = min(resultados_locales)
```
##### Conclusión paralela:
El tiempo se reduce redistribuyendo el cálculo entre varios núcleos del procesador.
Sin embargo, cuando hay pocas ciudades, el paralelo puede tardar más debido al overhead de crear procesos, lo cual se observa en la práctica.

---

## 4. Resultados

### 4.1 Ejecución Secuencial
<img width="518" height="112" alt="image" src="https://github.com/user-attachments/assets/4bcc4fe6-82a7-4196-a639-e4675c71c07d" />


### 4.2 Ejecución Paralela
<img width="511" height="110" alt="image" src="https://github.com/user-attachments/assets/84c8fe67-c62b-4007-93d1-31723d07f342" />

---

## 5. Análisis de Rendimiento

El algoritmo paralelo obtiene el mismo resultado que el secuencial, pero en menor tiempo.  
El *speedup* medido fue:

$$ S = \frac{T_{secuencial}}{T_{paralelo}} = \frac{0.072405}{0.049458} \approx 1.46x $$


Esto significa que el procesamiento paralelo permitió ejecutar el algoritmo **1.46 veces más rápido** al aprovechar 4 núcleos.

**Interpretación:**
- El tiempo mejora significativamente al distribuir las rutas entre procesos.
- El speedup no es lineal (no alcanza 4x con 4 núcleos) debido al **tiempo de creación y sincronización de procesos**, y a la **comunicación entre ellos**.
- Sin embargo, el rendimiento general demuestra una clara ganancia de eficiencia.

---

## 6. Conclusiones

1. El Problema del Viajante es un **caso ideal para estudiar el paralelismo**, ya que su complejidad factorial permite observar mejoras notables al distribuir las tareas.
2. La **versión paralela** logró reducir el tiempo de ejecución en casi un 65%, manteniendo la exactitud del resultado.
3. El **speedup obtenido (≈1.46x)** demuestra que el uso de múltiples núcleos es efectivo incluso para implementaciones simples de fuerza bruta.
6. Este laboratorio evidencia que, en problemas de búsqueda exhaustiva, **el paralelismo no solo mejora el rendimiento**, sino que también fomenta el diseño de algoritmos más eficientes para aprovechar los recursos del hardware moderno.
