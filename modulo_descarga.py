import os
import urllib.request

def descargar_secuencias_uniprot(lista_ids, archivo_salida="secuencias_totales.fasta"):
    print("--> Iniciando descarga de secuencias desde UniProt...")
    
    # Abrimos un único archivo para concatenar todas las secuencias
    with open(archivo_salida, "w") as archivo_final:
        for uniprot_id in lista_ids:
            uniprot_id = uniprot_id.strip() # Limpiar espacios
            if not uniprot_id:
                continue
                
            url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
            try:
                # Descargamos el contenido de la URL
                with urllib.request.urlopen(url) as respuesta:
                    fasta_contenido = respuesta.read().decode('utf-8')
                    archivo_final.write(fasta_contenido + "\n")
                print(f"Descargado: {uniprot_id}")
            except Exception as e:
                print(f"Error al descargar {uniprot_id}: {e}")
                
    print(f"--> ¡Descarga completada! Todas las secuencias guardadas en: {archivo_salida}")