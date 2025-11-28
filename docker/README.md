# Informe de Laboratorio - Taller Práctico 4: Optimización de Rutas del Viajero con Clusters de Servicios

## 1. Objetivos

*Objetivos:*  
- Diseñar y construir una solución distribuida y escalable para el Problema del Viajante (TSP) aplicando arquitecturas modernas de microservicios.  
- Desarrollar una API RESTful con Flask para calcular distancias.  
- Contenerizar la aplicación Flask usando Docker.  
- Desplegar un servicio escalable (Swarm) de la API en Docker.  
- Implementar un programa cliente de fuerza bruta para interactuar con la API y encontrar la ruta óptima.

## 2. Marco Teórico

El *Problema del Viajante de Comercio (TSP)* es un problema clásico de optimización combinatoria en el que se debe encontrar el camino más corto que recorre un conjunto de ciudades, visitando cada una exactamente una vez y regresando a la ciudad inicial. Se trata de un problema NP-hard, lo que significa que es difícil de resolver de manera eficiente para grandes números de ciudades.

*Microservicios:*  
En esta solución, se utiliza una arquitectura de microservicios, en la que cada operación es manejada por un servicio independiente y autónomo. En este caso, se creó una API RESTful utilizando Flask para el cálculo de distancias entre las ciudades.

*Docker y Docker Swarm:*  
Se utiliza Docker para contenerizar la API Flask y desplegarla de manera escalable utilizando *Docker Swarm*. Docker Swarm permite gestionar y orquestar un conjunto de contenedores de manera eficiente, asegurando la disponibilidad y balanceo de carga.

## 3. Metodología

### Configuración del Hardware

- *Sistema operativo*: Ubuntu 20.04 LTS.
- *Memoria RAM*: 4 GB.
- *Disco duro*: 25 GB.
- *Procesador*: Intel Core i5.

### Configuración del Software

- *Python*: Versión 3.10.
- *Flask*: Framework de Python para crear aplicaciones web.
- *Docker*: Plataforma para desarrollar, enviar y ejecutar aplicaciones dentro de contenedores.
- *Docker Swarm*: Orquestador de contenedores para la gestión de clusters de Docker.

### Descripción del Algoritmo y Desarrollo

1. *API Flask:*  
   Se construyó una API RESTful con Flask que recibe un conjunto de ciudades y calcula la distancia total utilizando la fórmula de *distancia euclidiana* entre ciudades consecutivas.

2. *Dockerización:*  
   La aplicación Flask se contenedorizó usando Docker. Para ello, se creó un archivo Dockerfile que define el entorno de ejecución y las dependencias necesarias.

3. *Despliegue con Docker Swarm:*  
   El servicio Flask fue desplegado en un cluster de Docker Swarm para gestionar la escalabilidad. Se crearon réplicas del servicio para manejar múltiples solicitudes simultáneamente.

4. *Cliente de Fuerza Bruta:*  
   El cliente genera todas las permutaciones posibles de las ciudades usando la librería itertools.permutations y envía las solicitudes a la API para calcular la distancia. Luego, mantiene un registro de la ruta con la menor distancia total.

## 4. Resultados

Al ejecutar el cliente de fuerza bruta, el sistema fue capaz de calcular las distancias entre las ciudades y encontrar la mejor ruta para un conjunto de 4 ciudades:

*Resultado de la ejecución:*

<img width="681" height="183" alt="image" src="https://github.com/user-attachments/assets/48ff9972-b006-4859-a969-cb17a258d1db" />


Los resultados fueron consistentes para diferentes combinaciones de ciudades dentro del rango de prueba.

## 5. Análisis de Rendimiento

- *Escalabilidad:*  
  El uso de Docker Swarm permitió distribuir las solicitudes de cálculo entre varias réplicas del servicio. Esto resultó en una *distribución eficiente de la carga*, mejorando el tiempo de respuesta para múltiples solicitudes.

- *Tiempo de ejecución:*  
  Para 4 ciudades, el tiempo de ejecución fue corto, pero el tiempo aumenta significativamente con el número de ciudades, debido a la naturaleza del *algoritmo de fuerza bruta*. Con más ciudades, el número de permutaciones crece rápidamente, lo que hace que el tiempo de cómputo sea más largo.

- *Comparación de rendimiento:*  
  Al comparar con un solo contenedor, el uso de múltiples réplicas con Swarm mejoró el rendimiento, reduciendo el tiempo de respuesta al balancear las cargas entre los contenedores.

## 6. Conclusiones

1. *Microservicios y Docker:*  
   La solución basada en microservicios y contenedores Docker permitió una implementación escalable y eficiente del problema del viajante, con un buen balance entre desarrollo y operación.

2. *Escalabilidad con Swarm:*  
   Docker Swarm permitió gestionar la carga de trabajo de manera eficiente, distribuyendo las solicitudes entre múltiples réplicas del servicio. Esto es crucial para sistemas distribuidos con alta carga.

3. *Fuerza Bruta:*  
   Si bien el algoritmo de fuerza bruta funciona bien para un número pequeño de ciudades, no es adecuado para grandes volúmenes debido a su complejidad exponencial. Sin embargo, es útil para entender el problema y puede ser optimizado con algoritmos heurísticos en el futuro.

## 7. Referencias

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
