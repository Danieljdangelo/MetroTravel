import os
import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import read_destinos, read_tarifas
from graph import Graph
from algorithms import shortest_path_cost, shortest_path_stops
import networkx as nx
import matplotlib.pyplot as plt


def start_gui():
    # Configurar rutas de datos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    destinos_file = os.path.join(data_dir, 'destinos.txt')
    tarifas_file = os.path.join(data_dir, 'tarifas.txt')

    # Leer datos y construir grafo
    destinos = read_destinos(destinos_file)
    tarifas = read_tarifas(tarifas_file)
    g = Graph()
    g.load_from_data(destinos, tarifas)
    codigos = list(destinos.keys())

    # Preparar grafo para dibujo y layout fijo
    graph_nx = nx.Graph()
    for node in g.nodes:
        graph_nx.add_node(node)
    for u, neighbors in g.adj.items():
        for v, cost in neighbors:
            if not graph_nx.has_edge(u, v):
                graph_nx.add_edge(u, v, weight=cost)
    # Layout fijo con semilla
    pos = nx.spring_layout(graph_nx, seed=42)

    # Variable para almacenar la última ruta calculada
    last_path = {'nodes': None}

    # Crear ventana principal
    root = tk.Tk()
    root.title('Metro Travel - Optimizador de Rutas')

    # Widgets de selección
    tk.Label(root, text='Origen:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
    origin_cb = ttk.Combobox(root, values=codigos, state='readonly')
    origin_cb.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text='Destino:').grid(row=1, column=0, sticky='w', padx=5, pady=5)
    dest_cb = ttk.Combobox(root, values=codigos, state='readonly')
    dest_cb.grid(row=1, column=1, padx=5, pady=5)

    visa_var = tk.BooleanVar()
    ttk.Checkbutton(root, text='Tiene visa?', variable=visa_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    opt_var = tk.StringVar(value='cost')
    ttk.Radiobutton(root, text='Costo mínimo', variable=opt_var, value='cost').grid(row=3, column=0, padx=5, pady=5)
    ttk.Radiobutton(root, text='Menor escalas', variable=opt_var, value='stops').grid(row=3, column=1, padx=5, pady=5)

    output = tk.Text(root, width=60, height=10, state='disabled')
    output.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def calculate():
        origen = origin_cb.get()
        destino = dest_cb.get()
        has_visa = visa_var.get()

        if not origen or not destino:
            messagebox.showwarning('Error', 'Seleccione origen y destino.')
            return
        if origen == destino:
            messagebox.showwarning('Error', 'El origen y destino deben ser distintos.')
            return

        # Selección de algoritmo
        if opt_var.get() == 'cost':
            path, metric = shortest_path_cost(g, origen, destino, has_visa)
            metric_name = 'Costo total'
        else:
            path, metric = shortest_path_stops(g, origen, destino, has_visa)
            metric_name = 'Número de escalas'

        # Mostrar resultado y guardar ruta
        if path is None:
            msg = 'No existe ruta disponible con las condiciones dadas.'
            last_path['nodes'] = None
        else:
            ruta_nombres = [f"{p} ({destinos[p]['nombre']})" for p in path]
            msg = 'Ruta óptima:\n' + ' -> '.join(ruta_nombres) + f"\n{metric_name}: {metric}"
            last_path['nodes'] = path

        output.config(state='normal')
        output.delete('1.0', tk.END)
        output.insert(tk.END, msg)
        output.config(state='disabled')

    def show_graph():
        plt.figure(figsize=(8, 6))
        # Dibujar grafo base
        nx.draw_networkx_edges(graph_nx, pos, alpha=0.4)
        nx.draw_networkx_nodes(graph_nx, pos, node_size=300, node_color='lightblue')
        nx.draw_networkx_labels(graph_nx, pos)

        # Resaltar ruta si existe
        if last_path['nodes']:
            path_nodes = last_path['nodes']
            path_edges = list(zip(path_nodes, path_nodes[1:]))
            nx.draw_networkx_nodes(graph_nx, pos, nodelist=path_nodes, node_color='orange', node_size=400)
            nx.draw_networkx_edges(graph_nx, pos, edgelist=path_edges, edge_color='red', width=2)

        plt.title('Grafo de vuelos Metro Travel')
        plt.axis('off')
        plt.show()

    # Botones
    ttk.Button(root, text='Calcular', command=calculate).grid(row=4, column=0, padx=5, pady=5)
    ttk.Button(root, text='Mostrar Grafo', command=show_graph).grid(row=4, column=1, padx=5, pady=5)
    ttk.Button(root, text='Salir', command=root.destroy).grid(row=4, column=2, padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    start_gui()
