import os
import urllib.request

def cargar_lista_proteinas(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo de configuración {ruta_archivo}")
        return []
    with open(ruta_archivo, "r") as f:
        return [linea.strip() for linea in f if linea.strip()]

def descargar_secuencias_uniprot(ruta_lista, ruta_salida):
    uniprot_ids = cargar_lista_proteinas(ruta_lista)
    if not uniprot_ids:
        print("No hay proteínas para descargar.")
        return False

    print(f"--> Iniciando descarga de {len(uniprot_ids)} secuencias desde UniProt...")
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w") as archivo_final:
        for uni_id in uniprot_ids:
            url = f"https://rest.uniprot.org/uniprotkb/{uni_id}.fasta"
            try:
                with urllib.request.urlopen(url) as respuesta:
                    fasta_contenido = respuesta.read().decode('utf-8')
                    archivo_final.write(fasta_contenido + "\n")
                print(f"Descargado con éxito: {uni_id}")
            except Exception as e:
                print(f"Error al descargar {uni_id}: {e}")
                
    print(f"--> ¡Descarga completada! Guardado en: {ruta_salida}")
    return True
