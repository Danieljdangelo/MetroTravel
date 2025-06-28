import csv


def read_destinos(file_path):
    """
    Lee destinos.txt y retorna un diccionario con:
    {codigo: {'nombre': nombre, 'requiere_visa': bool}}
    """
    destinos = {}
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Ignorar líneas vacías o comentarios
            if not row or row[0].startswith('#'):
                continue
            codigo, nombre, requiere_visa = row
            requiere = requiere_visa.strip().lower() in ('si', 'sí', 'yes', 'y')
            destinos[codigo.strip()] = {
                'nombre': nombre.strip(),
                'requiere_visa': requiere
            }
    return destinos


def read_tarifas(file_path):
    """
    Lee tarifas.txt y retorna una lista de tuplas:
    [(origen, destino, precio_float), ...]
    """
    tarifas = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            origen, destino, precio = row
            try:
                precio_val = float(precio)
            except ValueError:
                continue
            tarifas.append((origen.strip(), destino.strip(), precio_val))
    return tarifas


if __name__ == "__main__":
    # Prueba de lectura
    destinos = read_destinos("data/destinos.txt")
    tarifas = read_tarifas("data/tarifas.txt")
    print("Destinos cargados:", destinos)
    print("Tarifas cargadas:", tarifas)
