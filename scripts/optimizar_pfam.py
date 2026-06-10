import os
import subprocess

def optimizar_base_datos():
    print("=" * 60)
    print("   OPTIMIZACIÓN DE PFAM: CREANDO HMM REDUCIDO (ANEXO 1)   ")
    print("=" * 60)

    # Definición de rutas del proyecto
    RUTA_FAMILIAS = os.path.join("data", "familias_anexo1.txt")
    HMM_COMPLETO = os.path.join("data", "database", "Pfam-A.hmm")
    HMM_REDUCIDO = os.path.join("data", "database", "pfam_anexo1.hmm")

    if not os.path.exists(HMM_COMPLETO):
        print(f"Error crítico: No se encuentra Pfam-A.hmm en: {HMM_COMPLETO}")
        return

    # 1. Indexar el HMM grande (Error 2: Requisito indispensable para hmmfetch)
    if not os.path.exists(f"{HMM_COMPLETO}.ssi"):
        print("--> Indexando la base de datos completa de Pfam (esto solo se hace una vez)...")
        try:
            subprocess.run(["hmmfetch", "--index", HMM_COMPLETO], check=True)
            print("--> ¡Indexación completada con éxito (.ssi creado)!")
        except subprocess.CalledProcessError as e:
            print(f"Error al indexar con hmmfetch: {e}")
            return

    # 2. Extraer el set filtrado de familias del Anexo 1
    print(f"--> Extrayendo las 10 familias del Anexo 1 hacia: {HMM_REDUCIDO}")
    comando_fetch = ["hmmfetch", "-f", HMM_COMPLETO, RUTA_FAMILIAS]
    
    try:
        with open(HMM_REDUCIDO, "w") as archivo_salida:
            subprocess.run(comando_fetch, stdout=archivo_salida, check=True)
        print("--> ¡Archivo HMM reducido generado correctamente!")
    except subprocess.CalledProcessError as e:
        print(f"Error al extraer perfiles HMM: {e}")
        return

    # 3. Automatizar hmmpress sobre el archivo reducido (Error 3)
    print("--> Ejecutando hmmpress sobre el nuevo HMM reducido...")
    try:
        subprocess.run(["hmmpress", "-f", HMM_REDUCIDO], check=True, stdout=subprocess.DEVNULL)
        print("--> ¡hmmpress completado! Los 4 archivos binarios (.h3m, .h3i, .h3f, .h3p) han sido generados.")
        print("\n[ÉXITO] Tu base de datos optimizada está lista para usarse.")
    except subprocess.CalledProcessError as e:
        print(f"Error al presionar el HMM con hmmpress: {e}")

if __name__ == "__main__":
    optimizar_base_datos()
