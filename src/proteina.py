class Proteina:
    """
    Clase que representa una entidad biológica proteica y almacena 
    sus anotaciones funcionales obtenidas mediante HMMER.
    """
    def __init__(self, uniprot_id, descripcion="No disponible", longitud=0):
        self.uniprot_id = uniprot_id
        self.descripcion = descripcion
        self.longitud = longitud
        self.familias_encontradas = []

    def agregar_familia(self, familia_nombre, e_value):
        self.familias_encontradas.append({
            "familia": familia_nombre,
            "e_value": float(e_value)
        })

    def __str__(self):
        return f"Proteína UniProt: {self.uniprot_id} | Longitud: {self.longitud} aa"
