import os
import csv

def exportar_reporte_csv(lista_proteinas, ruta_salida):
    """
    Toma la lista de objetos Proteina y exporta sus anotaciones 
    a un archivo CSV estructurado.
    """
    print(f"--> Exportando resultados analíticos a: {ruta_salida}")
    
    # Asegurar que la carpeta results/ exista
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    try:
        with open(ruta_salida, mode="w", newline="", encoding="utf-8") as archivo_csv:
            # Definimos las columnas del reporte
            columnas = ["UniProt_ID", "Familia_Pfam", "E_value"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            
            # Escribir la fila de títulos (cabecera)
            escritor.writeheader()
            
            # Recorrer los objetos de la clase Proteina
            for proteina in lista_proteinas:
                if not proteina.familias_encontradas:
                    escritor.writerow({
                        "UniProt_ID": proteina.uniprot_id,
                        "Familia_Pfam": "Ninguna detectada",
                        "E_value": "N/A"
                    })
                else:
                    for fam in proteina.familias_encontradas:
                        escritor.writerow({
                            "UniProt_ID": proteina.uniprot_id,
                            "Familia_Pfam": fam["familia"],
                            "E_value": fam["e_value"]
                        })
                        
        print("--> ¡Archivo CSV exportado con éxito!")
        return True
    except Exception as e:
        print(f"Error al escribir el archivo CSV: {e}")
        return False

