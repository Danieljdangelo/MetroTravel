class Graph:
    """
    Representa un grafo no dirigido donde los nodos son aeropuertos,
    las aristas son rutas con un costo, y los nodos pueden requerir visa.
    
    Atributos:
        nodes (dict): información de cada nodo, incluyendo si requiere visa.
        adj (dict): lista de adyacencia con los vecinos y costos por nodo.
    """
    def __init__(self):
        # Diccionario de nodos: {codigo: {'requiere_visa': bool}}
        self.nodes = {}
        # Diccionario de adyacencias: {codigo: [(vecino, costo), ...]}
        self.adj = {}

    def add_node(self, codigo, requiere_visa=False):
        """
        Agrega un nodo al grafo si no existe.
        
        Args:
            codigo (str): Código del aeropuerto.
            requiere_visa (bool): Indica si se requiere visa para ese destino.
        """
        if codigo not in self.nodes:
            self.nodes[codigo] = {'requiere_visa': requiere_visa}
            self.adj[codigo] = []

    def add_edge(self, origen, destino, costo):
        """
        Agrega una arista bidireccional entre dos nodos existentes.

        Args:
            origen (str): Código del nodo de origen.
            destino (str): Código del nodo de destino.
            costo (float): Costo del vuelo entre ambos nodos.

        Raises:
            KeyError: Si uno de los nodos no existe en el grafo.
        """
        if origen not in self.nodes or destino not in self.nodes:
            raise KeyError(f"Nodo {origen} o {destino} no existe en el grafo.")
        self.adj[origen].append((destino, costo))
        self.adj[destino].append((origen, costo))

    def load_from_data(self, destinos_dict, tarifas_list):
        """
        Carga nodos y aristas desde estructuras de datos preprocesadas.

        Args:
            destinos_dict (dict): Diccionario con nodos y si requieren visa.
            tarifas_list (list): Lista de tuplas (origen, destino, costo).
        """
        # Agregar nodos
        for codigo, info in destinos_dict.items():
            self.add_node(codigo, info['requiere_visa'])
        # Agregar aristas
        for origen, destino, costo in tarifas_list:
            if origen in destinos_dict and destino in destinos_dict:
                self.add_edge(origen, destino, costo)

    def neighbors(self, codigo):
        """
        Retorna los vecinos y costos de un nodo.

        Args:
            codigo (str): Código del aeropuerto.

        Returns:
            list: Lista de tuplas (vecino, costo).
        """
        return self.adj.get(codigo, [])

    def requires_visa(self, codigo):
        """
        Retorna si un nodo requiere visa.

        Args:
            codigo (str): Código del aeropuerto.

        Returns:
            bool: True si requiere visa, False si no o si no existe.
        """
        return self.nodes.get(codigo, {}).get('requiere_visa', False)


if __name__ == "__main__":
    # Prueba de carga de grafo desde archivos
    from data_manager import read_destinos, read_tarifas
    destinos = read_destinos('data/destinos.txt')
    tarifas = read_tarifas('data/tarifas.txt')
    g = Graph()
    g.load_from_data(destinos, tarifas)
    print("Nodos cargados:", g.nodes)
    print("Adyacencias:", g.adj)
