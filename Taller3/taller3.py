#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import cv2
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Funciones auxiliares

def limpiar_y_crear_carpeta(path):
    """Elimina (si existe) y vuelve a crear la carpeta."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def extraer_frames(video_path, folder_frames_original):
    """Extrae frames de un video y los guarda como imagenes JPG."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"No se pudo abrir el video: {video_path}")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = f"frame_{frame_count:05d}.jpg"
        frame_path = os.path.join(folder_frames_original, frame_filename)
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    print(f"[OK] Se extrajeron {frame_count} frames en '{folder_frames_original}'.")

    return frame_count


def procesar_imagen_a_gris(input_path, output_path):
    """
    Lee una imagen en 'input_path', la pasa a escala de grises
    y la guarda en 'output_path' con 3 canales (BGR).
    """
    img = cv2.imread(input_path)
    if img is None:
        print(f"[WARN] No se pudo leer {input_path}")
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(output_path, gray_bgr)
    return True


def procesar_secuencial(folder_frames_original, folder_frames_seq):
    """Procesa los frames de forma secuencial."""
    frame_files = sorted(os.listdir(folder_frames_original))

    print("\n[INFO] Iniciando procesamiento SECUENCIAL...")
    start_time = time.time()

    for filename in frame_files:
        input_path = os.path.join(folder_frames_original, filename)
        output_path = os.path.join(folder_frames_seq, filename)
        procesar_imagen_a_gris(input_path, output_path)

    end_time = time.time()
    dt = end_time - start_time
    print(f"[OK] Procesamiento SECUENCIAL terminado en {dt:.4f} s")

    return dt, frame_files


def procesar_paralelo(folder_frames_original, folder_frames_par, frame_files, num_workers):
    """Procesa los frames de forma paralela usando hilos."""
    print("\n[INFO] Iniciando procesamiento PARALELO "
          f"(multihilos, workers = {num_workers})...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {}
        for filename in frame_files:
            input_path = os.path.join(folder_frames_original, filename)
            output_path = os.path.join(folder_frames_par, filename)
            future = executor.submit(procesar_imagen_a_gris, input_path, output_path)
            futures[future] = filename

        for future in as_completed(futures):
            ok = future.result()
            if not ok:
                print(f"[ERROR] Procesando {futures[future]}")

    end_time = time.time()
    dt = end_time - start_time
    print(f"[OK] Procesamiento PARALELO terminado en {dt:.4f} s")

    return dt


def crear_video_desde_frames(frames_folder, video_name, fps):
    """
    Crea un video .mp4 a partir de las imágenes de una carpeta.
    Todas las imágenes deben tener el mismo tamaño.
    """
    print(f"\n[INFO] Creando video '{video_name}' desde frames en '{frames_folder}'...")
    image_files = sorted(os.listdir(frames_folder))
    if not image_files:
        print(f"[ERROR] No hay imágenes en la carpeta {frames_folder}")
        return

    first_frame_path = os.path.join(frames_folder, image_files[0])
    frame = cv2.imread(first_frame_path)
    if frame is None:
        print("[ERROR] No se pudo leer el primer frame para determinar tamaño.")
        return

    height, width, channels = frame.shape
    frame_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, frame_size)

    for filename in image_files:
        file_path = os.path.join(frames_folder, filename)
        img = cv2.imread(file_path)
        if img is not None:
            video.write(img)
        else:
            print(f"[WARN] No se pudo cargar la imagen {filename}. Se omite.")

    video.release()
    print(f"[OK] ¡Video '{video_name}' creado exitosamente!")


# Funcion principal

def main():
    parser = argparse.ArgumentParser(
        description="Taller: procesamiento de video a escala de grises "
                    "(secuencial vs paralelo)."
    )
    parser.add_argument(
        "video_path",
        help="Ruta al archivo de video de entrada (por ejemplo, input.mp4)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="FPS del video de salida (por defecto 30)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Número de hilos para procesamiento paralelo "
             "(0 = usar número de CPUs detectadas)"
    )

    args = parser.parse_args()

    video_path = args.video_path
    video_result_fps = args.fps

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"No se encontró el video: {video_path}")

    # Si no se especifica número de workers, usar el número de CPUs
    if args.workers <= 0:
        try:
            import os as _os
            num_workers = _os.cpu_count() or 4
        except Exception:
            num_workers = 4
    else:
        num_workers = args.workers

    # Carpetas de trabajo
    folder_frames_original = "frames_video_original"
    folder_frames_seq = "frames_video_gray_seq"
    folder_frames_par = "frames_video_gray_par"

    # Nombres de los videos de salida
    video_name_seq = "video_gray_secuencial.mp4"
    video_name_par = "video_gray_paralelo.mp4"

    print(f"[INFO] Video de entrada: {video_path}")
    print(f"[INFO] FPS de salida: {video_result_fps}")
    print(f"[INFO] Hilos para paralelo: {num_workers}")

    # 1. Preparar carpetas
    limpiar_y_crear_carpeta(folder_frames_original)
    limpiar_y_crear_carpeta(folder_frames_seq)
    limpiar_y_crear_carpeta(folder_frames_par)

    # 2. Extraer frames del video original
    extraer_frames(video_path, folder_frames_original)

    # 3. Procesamiento secuencial
    time_seq, frame_files = procesar_secuencial(
        folder_frames_original, folder_frames_seq
    )

    # 4. Procesamiento paralelo
    time_par = procesar_paralelo(
        folder_frames_original, folder_frames_par, frame_files, num_workers
    )

    # 5. Calcular speedup
    print("\n================ RESULTADOS ================")
    print(f"Tiempo SECUENCIAL: {time_seq:.4f} s")
    print(f"Tiempo PARALELO  : {time_par:.4f} s")

    if time_par > 0:
        speedup = time_seq / time_par
        print(f"Speedup (T_secuencial / T_paralelo) = {speedup:.2f}x")
    else:
        print("No se pudo calcular speedup (tiempo paralelo = 0).")
    print("===========================================\n")

    # 6. Crear videos de salida
    crear_video_desde_frames(folder_frames_seq, video_name_seq, fps=video_result_fps)
    crear_video_desde_frames(folder_frames_par, video_name_par, fps=video_result_fps)

    print("\nListo. Videos generados en el directorio actual:")
    print(f" - {os.path.abspath(video_name_seq)}")
    print(f" - {os.path.abspath(video_name_par)}")


if __name__ == "__main__":
    main()
