Pipeline Bioinformático para la Identificación de Familias Pfam mediante HMMER

Este repositorio contiene el desarrollo de un pipeline bioinformático automatizado diseñado para clasificar funcionalmente e identificar los dominios biológicos asociados a un conjunto de 50 secuencias proteicas obtenidas desde UniProt. El análisis molecular se realiza mediante perfiles probabilísticos basados en Modelos Ocultos de Márkov (HMM) utilizando la suite de herramientas HMMER.

Con el fin de optimizar el tiempo de procesamiento y evitar la saturación de recursos computacionales, el análisis se enfoca exclusivamente en un subconjunto de 38 familias Pfam seleccionadas previamente por su relevancia estructural y catalítica. El pipeline realiza la ingesta automatizada de datos a través de consultas a la API REST de UniProtKB, unifica las secuencias, ejecuta las búsquedas homólogas mediante el motor de alineamiento hmmscan y gestiona las anotaciones estadísticas utilizando el paradigma de Programación Orientada a Objetos (POO).

Objetivo del Análisis

Identificar de manera dirigida y reproducible las familias de proteínas Pfam asociadas a las accesiones de UniProt mediante el uso de perfiles HMM y la herramienta HMMER, consolidando los hallazgos en una matriz analítica de salida.

Datos de Entrada y Control de Familias
El análisis de homología de secuencias y dominios conservados se limitó de forma estricta a las siguientes 38 familias del Anexo 1: Protein_kinase, Pkinase_Tyr, Ras, SH2, SH3_1, zf-C2H2, Homeobox, HTH_1, bZIP_1, Myb_DNA-binding, RRM_1, DEAD, KH_1, dsrm, ABC_tran, MFS_1, Ion_trans, HlyD, Aminotran_1_2, Aldedh, TIM, NAD_binding_1, GST_C_family, WD40, Ank, TPR_1, LRR_1, HSP70, HSP20, DnaJ, Response_reg, HisKA, Peptidase_M16, Sigma70_r2, Immunoglobulin, EGF, Cadherin y Fibronectin.

Las proteínas analizadas corresponden de forma exacta a los 50 identificadores UniProt suministrados en el Anexo 2 de la actividad, abarcando desde la accesión P00519 hasta la Q13485. 

Estructura Final del Repositorio
El proyecto se organiza bajo una arquitectura modular que separa el código ejecutable de los archivos de datos masivos y los outputs analíticos intermedios mediante un archivo de configuración .gitignore:

Plaintext
pfam_hmmer_pipeline/
├── data/                  # Datos de entrada y bases HMM (Ignorado en Git)
│   ├── database/          # Archivo maestro Pfam-A y perfiles optimizados
│   └── uniprot/           # Archivo FASTA consolidado de secuencias
├── results/               # Reportes y outputs del análisis (Ignorado en Git)
│   ├── resultado_hmmer.tblout
│   └── reporte_final.csv  # Matriz final de resultados exportada
├── scripts/               # Scripts de optimización local
│   └── optimizar_pfam.py  # Extracción selectiva de perfiles HMM
├── src/                   # Código fuente modular del pipeline
│   ├── __init__.py
│   ├── proteina.py        # Clase estructural Proteina (POO)
│   ├── modulo_descarga.py # Descarga automatizada desde la API de UniProt
│   ├── modulo_hmmer.py    # Ejecución de hmmscan y parseo tabular
│   └── modulo_reporte.py  # Exportación y formateo a matriz CSV
├── .gitignore             # Filtro de exclusión de datos masivos
├── README.md              # Informe técnico y documentación
└── main.py                # Orquestador y punto de entrada único del pipeline
Requisitos y Configuración del Entorno
El sistema requiere el sistema operativo Ubuntu 22.04 LTS (o superior) o Windows Subsystem for Linux (WSL), Python 3.8 o superior, Git y la suite HMMER instalado desde los repositorios oficiales mediante el comando sudo apt update && sudo apt install hmmer. La instalación se puede validar en consola ejecutando hmmscan -h.

Para la base de datos de perfiles se utiliza Pfam versión 38.2, obtenida mediante la instrucción de red wget https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam38.2/Pfam-A.hmm.gz, descomprimida con gunzip Pfam-A.hmm.gz y reubicada en la ruta de destino interna data/database/.

Metodología y Flujo de Trabajo Ejecutable
El pipeline opera de forma automática e integrada mediante dos fases secuenciales ejecutadas desde la consola de comandos:

La Fase 1 corresponde a la preparación y optimización biológica local. El comando python scripts/optimizar_pfam.py indexa el archivo maestro de Pfam mediante hmmfetch --index y genera una base de datos reducida denominada pfam_anexo1.hmm que contiene únicamente los 38 modelos probabilísticos de interés. Finalmente, ejecuta hmmpress para dar lugar a los cuatro archivos binarios de acceso rápido (.h3f, .h3i, .h3m y .h3p), disminuyendo el tiempo de búsqueda general de minutos a escasos segundos.

La Fase 2 corresponde al procesamiento analítico unificado. Tras activar el entorno virtual con source env/bin/activate, se lanza el orquestador principal mediante el comando python main.py. Este script lee de forma autónoma los identificadores, realiza la descarga asíncrona de las secuencias FASTA desde la API web de UniProt, unifica el archivo multiproteico en data/uniprot/secuencias_totales.fasta y ejecuta hmmscan comparando el set contra los perfiles HMM locales filtrados.

Programación Orientada a Objetos (POO)
El procesamiento y almacenamiento de la información biológica se rige bajo los principios de abstracción y encapsulamiento. El pipeline implementa la clase denominada Proteina en el archivo src/proteina.py, encargada de modelar informáticamente cada secuencia analizada.

Cada objeto instanciado de esta clase retiene dinámicamente el identificador UniProt, la longitud de la secuencia y una lista de diccionarios que almacena de forma estructurada los nombres de las familias Pfam asignadas junto con sus respectivos valores de significancia estadística (E-value). Esto permite transicionar de un análisis de texto plano a un manejo estructurado de entidades moleculares en memoria.

Resumen de Resultados Biológicos Obtenidos

El pipeline logró procesar y anotar exitosamente las 50 proteínas de UniProt de la lista de control, generando una matriz analítica limpia en results/reporte_final.csv que cumple con los requerimientos de interoperabilidad de datos.El análisis reveló un predominio de dominios asociados a la transducción de señales y el control metabólico celular. Entre los hallazgos más destacados se encuentra la correcta identificación de dominios catalíticos de cinasas (Protein_kinase y Pkinase_Tyr) en proteínas como P00519 con valores de expectativa estadística (E-value) sumamente cercanos a cero (ej. $1.7 \times 10^{-24}$), lo que descarta científicamente cualquier emparejamiento aleatorio y confirma una homología estructural absoluta. Asimismo, se detectó una fuerte presencia de proteínas G pequeñas de la familia Ras (ej. en la proteína P01112) y de chaperonas moleculares de choque térmico de la familia HSP70 en accesiones tanto eucariotas como procariotas (como P11142 y P0A6Y8), demostrando la robustez del modelo probabilístico empleado por HMMER para reconocer dominios altamente conservados a lo largo de la evolución.
