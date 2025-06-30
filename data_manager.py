import csv

def read_destinos(file_path):
    """
    Lee el archivo destinos.txt y construye un diccionario con la información de cada aeropuerto.
    Cada línea debe tener: código, nombre, requiere_visa (Sí/No).
    
    Retorna:
        dict: {
            'CCS': {'nombre': 'Caracas', 'requiere_visa': False},
            ...
        }
    """
    destinos = {}
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Ignorar líneas vacías o comentarios con #
            if not row or row[0].startswith('#'):
                continue
            # Extraer columnas y normalizar datos
            codigo, nombre, requiere_visa = row
            codigo = codigo.strip().upper()                     # Código en mayúsculas sin espacios
            nombre = nombre.strip()                             # Nombre limpio
            requiere = requiere_visa.strip().lower() in ('si', 'sí', 'yes', 'y')  # Convertir a booleano
            # Almacenar en el diccionario
            destinos[codigo] = {
                'nombre': nombre,
                'requiere_visa': requiere
            }
    return destinos

def read_tarifas(file_path):
    """
    Lee el archivo tarifas.txt y construye una lista de rutas con sus precios.
    Cada línea debe tener: origen, destino, precio (float).
    
    Retorna:
        list: [
            ('CCS', 'CUR', 35.0),
            ...
        ]
    """
    tarifas = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Ignorar líneas vacías o comentarios
            if not row or row[0].startswith('#'):
                continue
            origen, destino, precio = row
            try:
                precio_val = float(precio)  # Convertir precio a número
            except ValueError:
                continue  # Si falla la conversión, se salta la fila
            origen = origen.strip().upper()
            destino = destino.strip().upper()
            # Almacenar como tupla
            tarifas.append((origen, destino, precio_val))
    return tarifas

if __name__ == "__main__":
    # Prueba local para verificar lectura correcta de archivos
    destinos = read_destinos("data/destinos.txt")
    tarifas = read_tarifas("data/tarifas.txt")
    print("Destinos cargados:", destinos)
    print("Tarifas cargadas:", tarifas)
