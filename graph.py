class Graph:
    """
    Grafo no dirigido con costos en aristas y atributo de visa en nodos.
    """
    def __init__(self):
        # Se crea el diccionario 
        self.nodes = {}
        # Se crea la lista de adyacencias 
        self.adj = {}

    def add_node(self, codigo, requiere_visa=False):
        if codigo not in self.nodes:
            self.nodes[codigo] = {'requiere_visa': requiere_visa}
            self.adj[codigo] = []

    def add_edge(self, origen, destino, costo):
        # Se verifican que ambos nodos existan
        if origen not in self.nodes or destino not in self.nodes:
            raise KeyError(f"Nodo {origen} o {destino} no existe en el grafo.")
        # Se agrega una arista bidireccional
        self.adj[origen].append((destino, costo))
        self.adj[destino].append((origen, costo))

    def load_from_data(self, destinos_dict, tarifas_list):
        
        # Carga nodos y aristas a partir del diccionario
        # Se agregan todos los nodos
        for codigo, info in destinos_dict.items():
            self.add_node(codigo, info['requiere_visa'])
        # Se agregan todas las aristas
        for origen, destino, costo in tarifas_list:
            # Solo crea la arista si ambos códigos están en destinos
            if origen in destinos_dict and destino in destinos_dict:
                self.add_edge(origen, destino, costo)

    def neighbors(self, codigo):
        # Retorna lista de (vecino, costo) para un nodo dado.
        return self.adj.get(codigo, [])

    def requires_visa(self, codigo):
        """Retorna True si el nodo requiere visa."""
        return self.nodes.get(codigo, {}).get('requiere_visa', False)

if __name__ == "__main__":
    # Prueba
    from data_manager import read_destinos, read_tarifas
    destinos = read_destinos('data/destinos.txt')
    tarifas = read_tarifas('data/tarifas.txt')
    g = Graph()
    g.load_from_data(destinos, tarifas)
    print("Nodos cargados:", g.nodes)
    print("Adjacencias:", g.adj)
