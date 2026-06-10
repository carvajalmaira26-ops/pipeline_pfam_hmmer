import os
from src.modulo_descarga import descargar_secuencias_uniprot
from src.modulo_hmmer import ejecutar_hmmscan, parsear_resultados_hmmer
from src.modulo_reporte import exportar_reporte_csv

def main():
    print("=" * 60)
    print("      INICIANDO PIPELINE BIOINFORMÁTICO OPTIMIZADO      ")
    print("=" * 60)

    # Definición de rutas con la base de datos reducida (Anexo 1)
    RUTA_PROTEINAS_TXT = os.path.join("data", "proteinas_anexo2.txt")
    RUTA_FAMILIAS_TXT = os.path.join("data", "familias_anexo1.txt")
    
    FASTA_SALIDA = os.path.join("data", "uniprot", "secuencias_totales.fasta")
    HMM_DATABASE = os.path.join("data", "database", "pfam_anexo1.hmm")  # Base de datos optimizada
    HMMER_OUTPUT = os.path.join("results", "resultado_hmmer.tblout")
    CSV_OUTPUT = os.path.join("results", "reporte_final.csv")  # Reporte final Excel/CSV

    # 1. Descarga de secuencias
    if not descargar_secuencias_uniprot(RUTA_PROTEINAS_TXT, FASTA_SALIDA):
        print("Error en el paso de descarga. Pipeline interrumpido.")
        return

    print("-" * 50)

    # 2. Análisis HMMER ultrarrápido
    if not os.path.exists(HMM_DATABASE):
        print(f"Error: No se encuentra la base de datos optimizada en: {HMM_DATABASE}")
        print("Por favor ejecuta primero: python scripts/optimizar_pfam.py")
        return

    if not ejecutar_hmmscan(HMM_DATABASE, FASTA_SALIDA, HMMER_OUTPUT):
        print("Error en la ejecución de hmmscan. Pipeline interrumpido.")
        return

    print("-" * 50)

    # 3. Parseo Orientado a Objetos
    print("--> Parseando resultados y construyendo objetos de la clase Proteina...")
    lista_proteinas = parsear_resultados_hmmer(HMMER_OUTPUT, RUTA_FAMILIAS_TXT)
    print("-" * 50)

    # 4. Exportación de Resultados a CSV
    if exportar_reporte_csv(lista_proteinas, CSV_OUTPUT):
        print("--> Proceso de guardado finalizado de forma correcta.")
    else:
        print("Advertencia: No se pudo generar el reporte CSV.")

    print("=" * 60)
    print("            ¡PIPELINE FINALIZADO CON ÉXITO!             ")
    print("=" * 60)

if __name__ == "__main__":
    main()
