#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import math
import time
from multiprocessing import Pool, cpu_count
from PIL import Image

# Kernels Sobel 3x3
KX = [[-1, 0, 1],
      [-2, 0, 2],
      [-1, 0, 1]]

KY = [[-1, -2, -1],
      [ 0,  0,  0],
      [ 1,  2,  1]]

def to_grayscale(img_rgb):
    """Convierte una imagen PIL RGB a matriz 2D."""
    w, h = img_rgb.size
    px = img_rgb.load()
    gray = [[0]*w for _ in range(h)]
    # Luma aproximada (BT.601): 0.299 R + 0.587 G + 0.114 B
    for i in range(h):
        for j in range(w):
            r, g, b = px[j, i]
            y = int(0.299*r + 0.587*g + 0.114*b + 0.5)
            gray[i][j] = y if y < 256 else 255
    return gray

def sobel_pixel(gray, i, j):
    """Calcula la magnitud del gradiente en (i,j) usando KX y KY manualmente."""
    gx = (gray[i-1][j-1]*KX[0][0] + gray[i-1][j]*KX[0][1] + gray[i-1][j+1]*KX[0][2] +
          gray[i][j-1]*KX[1][0]   + gray[i][j]*KX[1][1]   + gray[i][j+1]*KX[1][2] +
          gray[i+1][j-1]*KX[2][0] + gray[i+1][j]*KX[2][1] + gray[i+1][j+1]*KX[2][2])

    gy = (gray[i-1][j-1]*KY[0][0] + gray[i-1][j]*KY[0][1] + gray[i-1][j+1]*KY[0][2] +
          gray[i][j-1]*KY[1][0]   + gray[i][j]*KY[1][1]   + gray[i][j+1]*KY[1][2] +
          gray[i+1][j-1]*KY[2][0] + gray[i+1][j]*KY[2][1] + gray[i+1][j+1]*KY[2][2])

    mag = int(min(255, math.sqrt(gx*gx + gy*gy)))
    return mag

def sobel_secuencial(gray):
    """Implementación secuencial 1-core. Devuelve imagen de bordes (matriz 2D de ints)."""
    h = len(gray)
    w = len(gray[0]) if h else 0
    out = [[0]*w for _ in range(h)]
    # Procesar solo 1..h-2 y 1..w-2 para no salirnos
    for i in range(1, h-1):
        for j in range(1, w-1):
            out[i][j] = sobel_pixel(gray, i, j)
    return out

def _worker_chunk(args):
    """Worker para procesar un rango de filas [i0, i1) (sin tocar bordes)."""
    gray, i0, i1, w = args
    # Cada worker devuelve una lista de filas (matrices parciales)
    partial = []
    for i in range(i0, i1):
        row = [0]*w
        for j in range(1, w-1):
            row[j] = sobel_pixel(gray, i, j)
        partial.append((i, row))
    return partial

def sobel_paralelo(gray, workers=None):
    """Implementación paralela multicore con Pool. Devuelve imagen de bordes (matriz 2D)."""
    h = len(gray)
    w = len(gray[0]) if h else 0
    out = [[0]*w for _ in range(h)]

    if h < 3 or w < 3:
        return out  # imagen demasiado pequeña

    if workers is None or workers < 1:
        workers = max(1, cpu_count() - 1)

    # Repartir filas internas [1..h-2] en bloques casi iguales
    filas_validas = list(range(1, h-1))
    n = len(filas_validas)
    if n < workers:
        workers = n

    # Particiono por bloques contiguos
    bloques = []
    base = n // workers
    resto = n % workers
    idx = 0
    for k in range(workers):
        tam = base + (1 if k < resto else 0)
        if tam == 0: 
            continue
        i0_rel = idx
        i1_rel = idx + tam
        i0 = filas_validas[i0_rel]
        i1 = filas_validas[i1_rel-1] + 1
        bloques.append((gray, i0, i1, w))
        idx += tam

    with Pool(processes=workers) as pool:
        results = pool.map(_worker_chunk, bloques)

    # Ensamblar
    for partial in results:
        for i, row in partial:
            out[i] = row
    return out

def save_as_png(gray_or_edges, path):
    """Guarda una matriz 2D (0..255) como PNG en escala de grises."""
    h = len(gray_or_edges)
    w = len(gray_or_edges[0]) if h else 0
    img = Image.new("L", (w, h))
    # Volcar datos
    pix = img.load()
    for i in range(h):
        for j in range(w):
            pix[j, i] = int(gray_or_edges[i][j])
    img.save(path)

def main():
    ap = argparse.ArgumentParser(description="Sobel secuencial vs. paralelo (multicore)")
    ap.add_argument("--in", dest="in_path", required=True, help="Ruta imagen de entrada (RGB)")
    ap.add_argument("--out_s", dest="out_seq", default="edges_seq.png", help="Salida sobel secuencial")
    ap.add_argument("--out_p", dest="out_par", default="edges_par.png", help="Salida sobel paralelo")
    ap.add_argument("--workers", type=int, default=None, help="Núcleos a usar en paralelo (por defecto, CPU disponibles-1)")
    args = ap.parse_args()

    # Cargar y a gris
    img = Image.open(args.in_path).convert("RGB")
    t0 = time.perf_counter()
    gray = to_grayscale(img)
    t1 = time.perf_counter()

    # Secuencial
    t2 = time.perf_counter()
    edges_seq = sobel_secuencial(gray)
    t3 = time.perf_counter()
    save_as_png(edges_seq, args.out_seq)

    # Paralelo
    t4 = time.perf_counter()
    edges_par = sobel_paralelo(gray, workers=args.workers)
    t5 = time.perf_counter()
    save_as_png(edges_par, args.out_par)

    # Metricas
    t_gray = t1 - t0
    t_seq  = t3 - t2
    t_par  = t5 - t4
    speedup = (t_seq / t_par) if t_par > 0 else float("inf")

    print("\n===== METRICAS =====")
    print(f"Conversión a gris: {t_gray:.4f} s")
    print(f"Sobel secuencial:  {t_seq:.4f} s")
    print(f"Sobel paralelo:    {t_par:.4f} s  (workers={args.workers or 'auto'})")
    print(f"Speedup (seq/par): {speedup:.2f}x")
    print(f"Salidas: {args.out_seq}  |  {args.out_par}")

if __name__ == "__main__":
    main()
