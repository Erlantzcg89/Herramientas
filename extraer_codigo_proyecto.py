"""
Script: extraer_codigo_proyecto.py
Descripción:
  Recorre recursivamente una carpeta de proyecto (Java Spring o Angular)
  y genera un archivo de texto con todo el código fuente relevante concatenado.
  Ignora automáticamente los archivos de prueba (*.spec.ts) y archivos específicos como mvnw.
  Permite seleccionar automáticamente entre dos rutas comentadas.

Autor: (E. Caballero)
Versión: 2.3
"""

import os
import subprocess
import sys

# ==== CONFIGURACIÓN ====

BASE_PATH = r"C:\Users\peric\Documents\portfolio"

# Rutas disponibles según tu comentario
RUTAS = {
    "1": r"angular-workspace\redsocial2026client",
    "2": r"spring-workspace\redsocial2026"
}

# Archivo de salida
ARCHIVO_SALIDA = "codigo_extraido.txt"

# Extensiones de archivos relevantes
EXTENSIONES_PERMITIDAS = {
    ".java", ".properties", # Spring Boot ".xml", ".yml", ".yaml", ".properties",
    ".html", ".ts", ".css" # Angular
}

# Carpetas a excluir
CARPETAS_EXCLUIDAS = {
    "dist", "build", "target", ".git", ".idea", "__pycache__",
    ".mvn", "test", "repository", "model",  # excluidas spring
    ".angular", ".vscode", "node_modules", "public", "banner", "footer",
    "home", "menu-principal", "mi-perfil", "register", "guards" # excluidas angular
}

# Archivos a excluir explícitamente
ARCHIVOS_EXCLUIDOS = {
    "pom.properties", "Redsocial2026Application.java"
}

# ==== LÓGICA ====

def extraer_codigo(base_dir: str, salida: str):
    with open(salida, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(base_dir):
            # Filtrar carpetas excluidas
            dirs[:] = [d for d in dirs if d not in CARPETAS_EXCLUIDAS]
            
            for file in files:
                # Ignorar archivos explícitamente excluidos
                if file in ARCHIVOS_EXCLUIDOS:
                    continue
                # Ignorar archivos spec.ts
                if file.endswith(".spec.ts"):
                    continue

                _, ext = os.path.splitext(file)
                if ext.lower() in EXTENSIONES_PERMITIDAS:
                    ruta_completa = os.path.join(root, file)
                    try:
                        with open(ruta_completa, "r", encoding="utf-8") as f:
                            contenido = f.read()
                        out.write(f"\n\n# ===== Archivo: {ruta_completa} =====\n\n")
                        out.write(contenido)
                    except Exception as e:
                        print(f"[⚠️] No se pudo leer {ruta_completa}: {e}")

    print(f"\n✅ Código extraído correctamente en: {os.path.abspath(salida)}")

def abrir_archivo(ruta_archivo: str):
    """Abre el archivo de salida con el programa predeterminado del sistema."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(ruta_archivo)
        elif sys.platform == "darwin":
            subprocess.run(["open", ruta_archivo])
        else:
            subprocess.run(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"[⚠️] No se pudo abrir el archivo automáticamente: {e}")

# ==== MENÚ AUTOMÁTICO ====

def seleccionar_proyecto():
    print("Selecciona el proyecto a extraer automáticamente:")
    print("1: redsocial2026client (Angular)")
    print("2: redsocial2026 (Spring)")
    eleccion = ""
    while eleccion not in RUTAS:
        eleccion = input("Ingresa 1 o 2: ").strip()
    ruta_completa = os.path.join(BASE_PATH, RUTAS[eleccion])
    print(f"\n📂 Proyecto seleccionado: {ruta_completa}\n")
    return ruta_completa

# ==== EJECUCIÓN ====

if __name__ == "__main__":
    ruta_proyecto = seleccionar_proyecto()
    if not os.path.exists(ruta_proyecto):
        print(f"❌ La ruta especificada no existe: {ruta_proyecto}")
    else:
        extraer_codigo(ruta_proyecto, ARCHIVO_SALIDA)
        abrir_archivo(ARCHIVO_SALIDA)
