import subprocess
import os
import sys

# --- 🛠️ CONFIGURACIÓN DE JUEGOS ---
# 
# **IMPORTANTE:** Reemplaza los HASHES y FILENAMES con los datos exactos 
# de los commits en tu repositorio.
# 
JUEGOS = {
    1: {
        "nombre": "Juego de Bryan (Viborita)",
        "hash": "b0ea520b8565adf626bb6cab987aa82ba7103748",
        "archivo": "viborita.py", 
    },
    2: {
        "nombre": "Juego de Alex (Ahorcado)",
        "hash": "f2c6c639bd32244e8ce8a9a36f7c633913e48244",
        "archivo": "proyecto SI.py",
    },
    3: {
        "nombre": "Juego de Gad (Reloj)",
        "hash": "43e6050f56b9dc21add019fab99d2b68327c0428", 
        "archivo": "reloj.py", 
    },
    4: {
        "nombre": "Juego de Erick",
        "hash": "752c424a7b7bd503b175b9e741e0aeb82d7e15ea",
        "archivo": "holamundo.py",
    },
    5: {
        "nombre": "Juego de Rafa (Memorama)",
        "hash": "b89bb2686dbea39ee90285262cb73c0da0247baf", 
        "archivo": "MEMORAMA1.py", 
    },
    6: {
        "nombre": "Juego de Zury",
        "hash": "c88aebbc30f9ecb4721c8b4b314de9a55336fb31", 
        "archivo": "Sudoku.py", 
    },
    7: {
        "nombre": "Juego Siete",
        "hash": "HASH_JUEGO_7", 
        "archivo": "juego_siete.py", 
    },
    8: {
        "nombre": "Juego Ocho",
        "hash": "HASH_JUEGO_8", # REEMPLAZAR
        "archivo": "juego_ocho.py", 
    },
    9: {
        "nombre": "Juego Nueve",
        "hash": "HASH_JUEGO_9", # REEMPLAZAR
        "archivo": "juego_nueve.py", 
    },
} 
def ejecutar_juego_desde_commit(juego_info):
    """
    Extrae un archivo Python de un commit específico usando 'git show', 
    lo guarda temporalmente y lo ejecuta.
    """
    hash_commit = juego_info["hash"]
    nombre_archivo = juego_info["archivo"]
    
    # Directorio temporal para guardar los archivos extraídos
    temp_dir = "temp_juegos_git"
    ruta_temporal = os.path.join(temp_dir, nombre_archivo)
    
    try:
        # Asegurarse de que el directorio temporal exista
        os.makedirs(temp_dir, exist_ok=True)
        
        # 1. Comando GIT para extraer el contenido del archivo
        comando_git = f'git show "{hash_commit}:{nombre_archivo}"'
        
        # Ejecutar el comando git y capturar el contenido
        proceso = subprocess.run(comando_git, shell=True, capture_output=True, text=True,encoding='utf-8',errors='replace', check=True)
        contenido_py = proceso.stdout
        
        if not contenido_py.strip():
            # Si Git no devuelve contenido, el archivo o hash es incorrecto
            raise ValueError("El archivo está vacío o el nombre/ruta/hash es incorrecto.")
        
        # 2. Guardar el contenido en el archivo temporal
        with open(ruta_temporal, "w", encoding="utf-8") as f:
            f.write(contenido_py)
            
        print(f"\n--- Ejecutando: {juego_info['nombre']} ---\n")
        
        # 3. Ejecutar el script temporal con el intérprete de Python
        subprocess.run([sys.executable, ruta_temporal])
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR GIT] El comando Git falló. Verifica el HASH o la ruta del archivo.")
        print(f"Detalles: {e.stderr.strip()}")
        
    except ValueError as e:
         print(f"[ERROR] Archivo no encontrado en el commit: {e}")
         
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")
        
    finally:
        # Limpiar: eliminar el archivo temporal
        if os.path.exists(ruta_temporal):
             os.remove(ruta_temporal)
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
             os.rmdir(temp_dir)


def mostrar_menu():
    """Muestra el menú principal y maneja la selección del usuario."""
    while True:
        print("\n=== MENÚ DE JUEGOS DEL REPOSITORIO ===")
        
        # Mostrar las opciones del menú
        for clave, info in JUEGOS.items():
            print(f"{clave}. {info['nombre']}")
            
        print("0. Salir")
        print("-" * 40)
        
        try:
            seleccion = int(input("Selecciona un juego para ejecutar (0 para salir): "))
            
            if seleccion == 0:
                print("¡Gracias! Saliendo...")
                break
            
            if seleccion in JUEGOS:
                ejecutar_juego_desde_commit(JUEGOS[seleccion])
                input("\nPresiona ENTER para volver al menú...")
            else:
                print("Opción no válida. Intenta de nuevo.")
                
        except ValueError:
            print("Entrada no válida. Por favor, ingresa solo un número.")


if __name__ == "__main__":
    mostrar_menu()