import os
from modulo_descarga import descargar_secuencias_uniprot
from modulo_hmmer import ejecutar_hmmscan, analizar_resultados_hmmer

# ANEXO 1: Lista de familias Pfam de interés
FAMILIAS_ANEXO1 = [
    "Protein_kinase", "Pkinase_Tyr", "Ras", "SH2", "SH3_1", "zf-C2H2", 
    "Homeobox", "HTH_1", "bZIP_1", "Myb_DNA-binding", "RRM_1", "DEAD", 
    "KH_1", "dsrm", "ABC_tran", "MFS_1", "Ion_trans", "HlyD", "Aminotran_1_2", 
    "Aldedh", "TIM", "NAD_binding_1", "GST_C_family", "WD40", "Ank", "TPR_1", 
    "LRR_1", "HSP70", "HSP20", "DnaJ", "Response_reg", "HisKA", "Peptidase_M16", 
    "Sigma70_r2", "Immunoglobulin", "EGF", "Cadherin", "Fibronectin"
]

# ANEXO 2: Lista de IDs de UniProt a evaluar
PROTEINAS_ANEXO2 = [
    "P00519", "P42684", "P12931", "P06241", "P07947", "Q06187", "P43403", "P43405",
    "P62993", "P01112", "P01116", "P01111", "P04049", "P31749", "P28482", "P27361",
    "P00533", "P21802", "P16234", "P12956", "P29353", "P42681", "P35222", "P62937",
    "P29317", "P08047", "P15056", "P40763", "P42224", "P15924", "P10242", "P19838",
    "P11473", "P61244", "Q9Y2T1", "P08107", "P0A6Y8", "P0A6W5", "P0A9Q7", "P0A799",
    "P0A7Y4", "P0A8V2", "P39451", "P11142", "P13569", "P22681", "P98160", "P12814",
    "Q92793", "Q13485"
]

def main():
    print("====================================================")
    print("      INICIANDO PIPELINE BIOINFORMÁTICO PFAM       ")
    print("====================================================\n")
    
    # Base de datos completa de Pfam que acabamos de descargar
    bd_pfam = "Pfam-A.hmm" 
    
    if not os.path.exists(bd_pfam):
        print(f"ERROR CRÍTICO: No se encuentra el archivo de base de datos '{bd_pfam}'.")
        print("Por favor, asegúrate de haber ejecutado los comandos wget y gunzip en la terminal.")
        return

    # 1. Ejecutar Descarga Automatizada de UniProt
    archivo_fasta = "secuencias_totales.fasta"
    descargar_secuencias_uniprot(PROTEINAS_ANEXO2, archivo_fasta)
    print("-" * 50)

    # 2. Ejecutar HMMER hmmscan
    archivo_reporte = "resultado_hmmer.tblout"
    ejecutar_hmmscan(bd_pfam, archivo_fasta, archivo_reporte)
    print("-" * 50)

    # 3. Analizar y Cargar en la Clase POO
    resultado_objetos = analizar_resultados_hmmer(archivo_reporte, FAMILIAS_ANEXO1)
    print("-" * 50)

    # 4. Mostrar el reporte final solicitado en clase
    print("\n================ REPORTES DE FAMILIAS DETECTADAS ================")
    if not resultado_objetos:
        print("No se mapearon familias del Anexo 1 en las proteínas provistas.")
    else:
        for id_prot, obj_proteina in resultado_objetos.items():
            print(f"\nProteína UniProt ID: {obj_proteina.query_id}")
            print("  Familias Pfam asignadas:")
            for fam in obj_proteina.familias_encontradas:
                print(f"    - {fam['familia']} (E-value: {fam['e_value']})")
    print("=================================================================\n")

if __name__ == "__main__":
    main()