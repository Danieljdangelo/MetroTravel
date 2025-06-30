import os
import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import read_destinos, read_tarifas
from graph import Graph
from algorithms import shortest_path_cost, shortest_path_stops
import networkx as nx
import matplotlib.pyplot as plt


def start_gui():
    """
    Inicia una interfaz gráfica con Tkinter que permite al usuario calcular 
    la mejor ruta entre dos destinos del Caribe, según dos criterios:
    - Costo total (usando Dijkstra)
    - Número de escalas (usando BFS)

    También permite visualizar el grafo de rutas usando NetworkX y Matplotlib.
    """

    # Configurar rutas de los archivos de datos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    destinos_file = os.path.join(data_dir, 'destinos.txt')
    tarifas_file = os.path.join(data_dir, 'tarifas.txt')

    # Verificar existencia de los archivos requeridos
    if not os.path.exists(destinos_file) or not os.path.exists(tarifas_file):
        messagebox.showerror("Error", "No se encontraron los archivos de datos.\nVerifica que 'destinos.txt' y 'tarifas.txt' existan en la carpeta 'data'.")
        return

    # Leer datos y construir el grafo
    destinos = read_destinos(destinos_file)
    tarifas = read_tarifas(tarifas_file)
    g = Graph()
    g.load_from_data(destinos, tarifas)
    codigos = list(destinos.keys())

    # Crear grafo de NetworkX para visualización
    graph_nx = nx.Graph()
    for node in g.nodes:
        graph_nx.add_node(node)
    for u, neighbors in g.adj.items():
        for v, cost in neighbors:
            if not graph_nx.has_edge(u, v):
                graph_nx.add_edge(u, v, weight=cost)

    # Posicionamiento fijo del grafo para visualización
    pos = nx.spring_layout(graph_nx, seed=42)

    # Variable para guardar la última ruta calculada
    last_path = {'nodes': None}

    # Crear ventana principal con Tkinter
    root = tk.Tk()
    root.title('Metro Travel - Optimizador de Rutas')

    # Widgets de selección de origen y destino
    tk.Label(root, text='Origen:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
    origin_cb = ttk.Combobox(root, values=codigos, state='readonly')
    origin_cb.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text='Destino:').grid(row=1, column=0, sticky='w', padx=5, pady=5)
    dest_cb = ttk.Combobox(root, values=codigos, state='readonly')
    dest_cb.grid(row=1, column=1, padx=5, pady=5)

    # Checkbox para indicar si se tiene visa
    visa_var = tk.BooleanVar()
    ttk.Checkbutton(root, text='Tiene visa?', variable=visa_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Opciones de optimización: costo o escalas
    opt_var = tk.StringVar(value='cost')
    ttk.Radiobutton(root, text='Costo mínimo', variable=opt_var, value='cost').grid(row=3, column=0, padx=5, pady=5)
    ttk.Radiobutton(root, text='Menor escalas', variable=opt_var, value='stops').grid(row=3, column=1, padx=5, pady=5)

    # Área de salida de resultados
    output = tk.Text(root, width=60, height=10, state='disabled')
    output.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def calculate():
        """
        Calcula la ruta óptima entre los destinos seleccionados y
        muestra el resultado en el área de salida.
        """
        origen = origin_cb.get()
        destino = dest_cb.get()
        has_visa = visa_var.get()

        # Validaciones iniciales
        if not origen or not destino:
            messagebox.showwarning('Error', 'Seleccione origen y destino.')
            return
        if origen == destino:
            messagebox.showwarning('Error', 'El origen y destino deben ser distintos.')
            return
        if not g.neighbors(origen):
            messagebox.showwarning("Advertencia", f"El aeropuerto '{origen}' no tiene rutas disponibles desde este origen.")
            return

        # Ejecutar el algoritmo correspondiente
        if opt_var.get() == 'cost':
            path, metric = shortest_path_cost(g, origen, destino, has_visa)
            metric_name = 'Costo total'
        else:
            path, metric = shortest_path_stops(g, origen, destino, has_visa)
            metric_name = 'Número de escalas'

        # Mostrar resultado
        if path is None:
            msg = 'No existe ruta disponible con las condiciones dadas.'
            if not has_visa:
                msg += '\nVerifique si necesita visa para acceder a alguno de los destinos.'
            last_path['nodes'] = None
        else:
            ruta_nombres = [f"{p} ({destinos[p]['nombre']})" for p in path]
            msg = 'Ruta óptima:\n' + ' -> '.join(ruta_nombres) + f"\n{metric_name}: {metric}"
            last_path['nodes'] = path

        # Actualizar área de texto
        output.config(state='normal')
        output.delete('1.0', tk.END)
        output.insert(tk.END, msg)
        output.config(state='disabled')

    def show_graph():
        """
        Muestra el grafo completo con los destinos y resalta la ruta calculada,
        si existe, usando matplotlib y networkx.
        """
        plt.figure(figsize=(8, 6))

        # Dibujar el grafo base
        nx.draw_networkx_edges(graph_nx, pos, alpha=0.4)
        nx.draw_networkx_nodes(graph_nx, pos, node_size=300, node_color='lightblue')
        nx.draw_networkx_labels(graph_nx, pos)

        # Dibujar ruta calculada si existe
        if last_path['nodes']:
            path_nodes = last_path['nodes']
            path_edges = list(zip(path_nodes, path_nodes[1:]))
            nx.draw_networkx_nodes(graph_nx, pos, nodelist=path_nodes, node_color='orange', node_size=400)
            nx.draw_networkx_edges(graph_nx, pos, edgelist=path_edges, edge_color='red', width=2)

        plt.title('Grafo de vuelos Metro Travel')
        plt.axis('off')
        plt.show()

    # Botones principales de acción
    ttk.Button(root, text='Calcular', command=calculate).grid(row=4, column=0, padx=5, pady=5)
    ttk.Button(root, text='Mostrar Grafo', command=show_graph).grid(row=4, column=1, padx=5, pady=5)
    ttk.Button(root, text='Salir', command=root.destroy).grid(row=4, column=2, padx=5, pady=5)

    # Iniciar bucle principal de la interfaz
    root.mainloop()


if __name__ == '__main__':
    start_gui()
