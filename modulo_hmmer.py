import os
import subprocess

# --- AQUÍ ESTÁ LA CLASE (POO) REQUERIDA ---
class ProteinaResult:

    def __init__(self,
                 query_id,
                 descripcion="No disponible",
                 longitud=0):

        self.query_id = query_id
        self.descripcion = descripcion
        self.longitud = longitud
        self.familias_encontradas = []

    def agregar_familia(self, familia_nombre, e_value):

        self.familias_encontradas.append({
            "familia": familia_nombre,
            "e_value": float(e_value)
        }) # Lista de diccionarios con familias y E-values



# --- ETAPA DE EJECUCIÓN DE HMMER ---
def ejecutar_hmmscan(archivo_hmm_bd, archivo_fasta, archivo_reporte="resultado_hmmer.tblout"):
    print("--> Ejecutando hmmscan contra las familias del Anexo 1...")
    
    # Comando equivalente a la terminal de Ubuntu
    comando = ["hmmscan", "--tblout", archivo_reporte, archivo_hmm_bd, archivo_fasta]
    
    try:
        # Se ejecuta el comando en el sistema mediante Python
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL)
        print(f"--> hmmscan finalizado con éxito. Resultado en: {archivo_reporte}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar hmmscan: {e}")
        return None
    
    return archivo_reporte


# --- ETAPA DE PARSEO Y CARGA EN LA CLASE ---
def analizar_resultados_hmmer(archivo_reporte, familias_anexo1):
    print("--> Parseando resultados y cargando objetos de la clase...")
    proteinas_dict = {} # Para almacenar objetos {id_proteina: ObjetoProteina}

    if not os.path.exists(archivo_reporte):
        print("No se encontró el archivo de resultados.")
        return proteinas_dict

    with open(archivo_reporte, "r") as f:
        for linea in f:
            # Ignorar líneas de comentarios de HMMER
            if linea.startswith("#"):
                continue
            
            partes = linea.split()
            if len(partes) < 5:
                continue
                
            # hmmscan organiza las columnas así:
            target_name = partes[0]  # Familia Pfam encontrada
            query_name = partes[2]   # ID de nuestra proteína de UniProt
            e_value = partes[4]      # Valor de expectativa (E-value)
            
            # Limpiar el ID de la proteína por si viene con formato "sp|P00519|..."
            if "|" in query_name:
                query_id = query_name.split("|")[1]
            else:
                query_id = query_name

            # Filtrar: Solo nos interesan las familias del Anexo 1
            if target_name in familias_anexo1:
                # Si es la primera vez que vemos la proteína, creamos el Objeto
                if query_id not in proteinas_dict:
                    proteinas_dict[query_id] = ProteinaResult(query_id)
                
                # Agregamos la familia detectada al objeto usando su método
                proteinas_dict[query_id].agregar_familia(target_name, e_value)
                
    return proteinas_dict