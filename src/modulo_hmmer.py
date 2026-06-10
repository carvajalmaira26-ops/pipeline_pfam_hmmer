import os
import subprocess
from src.proteina import Proteina

def cargar_familias_anexo1(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo de familias {ruta_archivo}")
        return set()
    with open(ruta_archivo, "r") as f:
        return set(linea.strip() for linea in f if linea.strip())

def ejecutar_hmmscan(archivo_hmm_bd, archivo_fasta, archivo_reporte):
    print("--> Ejecutando hmmscan contra la base de datos...")
    os.makedirs(os.path.dirname(archivo_reporte), exist_ok=True)
    
    comando = ["hmmscan", "--tblout", archivo_reporte, archivo_hmm_bd, archivo_fasta]
    try:
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL)
        print(f"--> hmmscan finalizado con éxito. Resultado en: {archivo_reporte}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error crítico al ejecutar hmmscan: {e}")
        return False

def parsear_resultados_hmmer(archivo_reporte, ruta_familias):
    familias_validas = cargar_familias_anexo1(ruta_familias)
    diccionario_proteinas = {}

    if not os.path.exists(archivo_reporte):
        print("No se encontró el reporte de HMMER para parsear.")
        return []

    with open(archivo_reporte, "r") as f:
        for linea in f:
            if linea.startswith("#"):
                continue
            
            partes = linea.split()
            if len(partes) < 5:
                continue
                
            familia_nombre = partes[0]
            query_id = partes[2]
            e_value = partes[4]

            if familia_nombre in familias_validas:
                if query_id not in diccionario_proteinas:
                    id_limpio = query_id.split("|")[1] if "|" in query_id else query_id
                    diccionario_proteinas[query_id] = Proteina(uniprot_id=id_limpio)
                
                diccionario_proteinas[query_id].agregar_familia(familia_nombre, e_value)

    return list(diccionario_proteinas.values())
