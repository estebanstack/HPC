# Informe de Laboratorio: Procesamiento de Video en Algoritmos Paralelos

Procesamiento de Video en Algoritmos Paralelos: Transformación de un Video a Escala de Grises

## 1. Objetivos:
El objetivo de este laboratorio es implementar y comparar la eficiencia de dos algoritmos: uno secuencial y uno paralelo multihilos. Ambos algoritmos tienen la tarea de transformar un video original a escala de grises, y se medirá la mejora en el rendimiento al usar paralelismo.

## 2. Marco Teórico

El **procesamiento de video** involucra técnicas y algoritmos utilizados para manipular, analizar y mejorar secuencias de imágenes digitales (videos). En este caso, nos centramos en la conversión de un video de color a escala de grises. El procesamiento de video tiene aplicaciones en áreas como compresión, análisis de movimiento y visión por computadora.

### Conceptos Clave:
- **Video Digital**: Secuencia de fotogramas mostrados a una frecuencia determinada (FPS).
- **Compresión de Video**: Reducción de redundancia en los datos del video para mejorar almacenamiento y transmisión.
- **Mejora de Video**: Aplicación de filtros y técnicas para mejorar la calidad del video.
- **Algoritmos Secuenciales y Paralelos**: El procesamiento secuencial se realiza en un solo hilo, mientras que el procesamiento paralelo divide las tareas en múltiples hilos para mejorar la eficiencia.

## 3. Metodología

### Configuración del Hardware:
- CPU: [Especificar modelo]
- Memoria: [Especificar cantidad de RAM]
- [Detalles adicionales de hardware si es necesario]

### Configuración del Software:
- **Lenguaje**: Python 3.x
- **Librerías**:
  - OpenCV 4.x (para procesamiento de imágenes y video)
  - ThreadPoolExecutor (para paralelismo)
- **Entorno de ejecución**: [Colab, Jupyter, etc.]

### Explicación del Algoritmo Desarrollado:
1. **Extracción de Frames**: Se extraen los frames de un video usando OpenCV.
2. **Procesamiento Secuencial**: Cada frame se convierte a escala de grises de forma secuencial.
3. **Procesamiento Paralelo**: Usando multihilos, cada frame se convierte a escala de grises en paralelo.
4. **Reconstitución del Video**: Los frames procesados se reagrupan y se crean dos videos de salida, uno secuencial y otro paralelo.

## 4. Resultados

### Tiempo de Ejecución:
<img width="403" height="104" alt="image" src="https://github.com/user-attachments/assets/a64ae052-42b8-4f08-8481-3271d155152f" />


## 5. Análisis de Rendimiento

En esta sección, comparamos el rendimiento de los dos algoritmos basándonos en los tiempos de ejecución. El paralelismo mejora considerablemente el tiempo de procesamiento, como se observa en el **speedup** obtenido. Esto se debe a la utilización de múltiples núcleos de CPU en el procesamiento paralelo, lo cual reduce significativamente el tiempo de ejecución al dividir las tareas entre varios hilos.

### Observaciones:
- En videos de mayor resolución o longitud, el paralelismo muestra una mayor ventaja.
- El procesamiento secuencial es más sencillo pero mucho más lento para grandes volúmenes de datos.

## 6. Conclusiones

A lo largo de este laboratorio, hemos aprendido cómo la paralelización puede mejorar significativamente el rendimiento en tareas de procesamiento de video. El uso de múltiples hilos permite realizar el mismo trabajo en un menor tiempo, lo que es particularmente útil cuando se trata de grandes cantidades de datos como un video. Esta experiencia también refuerza la importancia de seleccionar el algoritmo adecuado en función de los recursos disponibles.

## 7. Recomendaciones

Para futuras implementaciones, sería útil considerar el uso de más técnicas de paralelismo o incluso GPUs para mejorar el rendimiento en tareas aún más complejas.
