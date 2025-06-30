import PySimpleGUI as sg
from data_manager import read_destinos, read_tarifas
from graph import Graph
from algorithms import shortest_path_cost, shortest_path_stops


def start_gui():
    """
    Inicia una interfaz gráfica para calcular la ruta óptima entre islas del Caribe
    según el criterio seleccionado: costo o número de escalas.
    El usuario puede seleccionar el aeropuerto de origen, destino y si posee visa.
    """

    # Cargar datos desde archivos
    destinos = read_destinos('data/destinos.txt')
    tarifas = read_tarifas('data/tarifas.txt')

    # Construir grafo con los datos cargados
    g = Graph()
    g.load_from_data(destinos, tarifas)

    # Obtener la lista de códigos de aeropuerto
    codigos = list(destinos.keys())

    # Definir el diseño de la ventana
    layout = [
        [sg.Text('Origen:'), sg.Combo(codigos, key='-ORIGEN-', readonly=True)],
        [sg.Text('Destino:'), sg.Combo(codigos, key='-DESTINO-', readonly=True)],
        [sg.Checkbox('Tiene visa?', key='-VISA-')],
        [sg.Text('Optimizar por:'),
         sg.Radio('Costo mínimo', 'RADIO', default=True, key='-OPC_COSTO-'),
         sg.Radio('Menor escalas', 'RADIO', key='-OPC_ESCALAS-')],
        [sg.Button('Calcular'), sg.Button('Salir')],
        [sg.Multiline(size=(60, 10), key='-OUTPUT-', disabled=True)]
    ]

    # Crear ventana principal
    window = sg.Window('Metro Travel - Optimizador de Rutas', layout)

    # Bucle principal de eventos
    while True:
        event, values = window.read()

        # Cerrar la ventana
        if event in (sg.WIN_CLOSED, 'Salir'):
            break

        if event == 'Calcular':
            origen = values['-ORIGEN-']
            destino = values['-DESTINO-']
            has_visa = values['-VISA-']

            # Validaciones básicas de entrada
            if not origen or not destino:
                window['-OUTPUT-'].update('Por favor, seleccione origen y destino.\n')
                continue

            if origen == destino:
                window['-OUTPUT-'].update('El origen y destino deben ser distintos.\n')
                continue

            # Determinar algoritmo según criterio seleccionado
            if values['-OPC_COSTO-']:
                path, metric = shortest_path_cost(g, origen, destino, has_visa)
                metric_name = 'Costo total'
            else:
                path, metric = shortest_path_stops(g, origen, destino, has_visa)
                metric_name = 'Número de escalas'

            # Preparar el resultado a mostrar
            if path is None:
                output = 'No existe ruta disponible con las condiciones dadas.\n'
            else:
                ruta_nombres = [f"{p} ({destinos[p]['nombre']})" for p in path]
                output = 'Ruta óptima:\n' + ' -> '.join(ruta_nombres) + '\n'
                output += f"{metric_name}: {metric}\n"

            # Limpiar y mostrar resultado en el área de texto
            window['-OUTPUT-'].update('')
            window['-OUTPUT-'].update(output)

    # Cerrar ventana al salir del bucle
    window.close()


if __name__ == '__main__':
    start_gui()
