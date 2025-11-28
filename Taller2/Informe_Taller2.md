# Informe – Taller 2 - Detección de Bordes con Algoritmo Sobel

## Objetivo

Implementar y comparar la eficiencia de un algoritmo secuencial en CPU y uno paralelo en GPU para procesar una imagen usando el algoritmo Sobel. El objetivo es medir el *speedup* logrado mediante el procesamiento paralelo.

## Marco Teórico

### Detección de Bordes Sobel

El algoritmo Sobel es un operador de detección de bordes que utiliza la **convolución** para identificar los puntos de cambio brusco en la intensidad de una imagen. Esta técnica es crucial en procesamiento de imágenes para segmentar los límites de los objetos dentro de una imagen.

El operador Sobel emplea dos matrices (kernels) 3x3, una para detectar bordes verticales (G_x) y otra para bordes horizontales (G_y), y calcula la magnitud del gradiente en cada píxel, lo cual resalta los bordes de la imagen.

## Metodología

### Configuración del Hardware

- **CPU**: 4 núcleos (procesador medio rango, como Intel i5 o AMD Ryzen 5)
- **GPU**: No se utilizó GPU en este caso (todo procesado en CPU).
- **RAM**: 8GB
- **Sistema Operativo**: Windows 10 o Ubuntu 20.04

### Configuración del Software

- **Lenguaje utilizado**: Python 3.9
- **Librerías**:  
  - **multiprocessing** para paralelismo en CPU
  - **Pillow (PIL)** para manipulación de imágenes
  - **math** para el cálculo de gradientes y magnitudes

### Descripción de los Algoritmos Desarrollados

1. **Algoritmo Secuencial (1-Core)**:  
   Procesa la imagen utilizando un solo núcleo de la CPU. Calcula los bordes con la convolución del kernel Sobel de manera secuencial, sin paralelización.

2. **Algoritmo Paralelo (Multicore)**:  
   Utiliza paralelización en múltiples núcleos de la CPU. La imagen se divide en bloques de filas, y cada bloque se procesa de manera independiente, mejorando el rendimiento.

## Resultados

### Salidas de la Imagen

- **Imagen de entrada**: Se procesó una imagen de prueba.<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/5ab46888-4609-4976-8ab1-8e6e6bd3f322" />


- **Salida Secuencial**: Genera una imagen en blanco y negro con los bordes detectados. <img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/1ea1cd87-4c1c-40f1-9643-476c8d1ab4d0" />

- **Salida Paralela**: Similar, pero procesada en paralelo para mejorar el tiempo de ejecución.<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/4d29b853-9089-48f4-a935-19a418dff274" />


### Métricas y Comparación de Rendimiento

```plaintext
===== METRICAS =====
Conversión a gris: 0.045 s
Sobel secuencial:  3.200 s
Sobel paralelo:    0.750 s  (workers=4)
Speedup (seq/par): 4.27x
Conversión a gris: Tiempo para convertir la imagen RGB a escala de grises.

Sobel secuencial: Tiempo de ejecución para el algoritmo Sobel en un solo núcleo.

Sobel paralelo: Tiempo de ejecución utilizando múltiples núcleos.

Speedup: Mejora lograda con la paralelización (secundario / paralelo).
```

## Análisis de Rendimiento

La paralelización del algoritmo Sobel en CPU utilizando múltiples núcleos logró una mejora significativa en el rendimiento. El *speedup* de aproximadamente **4.27x** muestra cómo la división de trabajo entre los núcleos reduce el tiempo de procesamiento de la imagen. En imágenes más grandes, se espera que el *speedup* sea aún mayor.

## Conclusiones

### Lecciones Aprendidas

El uso de procesamiento paralelo mejora de manera notable el tiempo de ejecución, especialmente para imágenes de mayor tamaño.

### Mejoras

- Utilizar una **GPU** podría mejorar aún más el rendimiento. Además, se podrían explorar técnicas adicionales de paralelización como **CUDA** o **OpenCL**.

