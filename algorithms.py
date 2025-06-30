import heapq
from collections import deque
from graph import Graph


def shortest_path_cost(graph: Graph, start: str, end: str, has_visa: bool):
    """
    Calcula la ruta de costo mínimo entre dos nodos usando el algoritmo de Dijkstra,
    respetando las restricciones de visa si el usuario no la posee.

    Args:
        graph (Graph): Grafo de destinos y rutas.
        start (str): Nodo de inicio (código de aeropuerto).
        end (str): Nodo destino (código de aeropuerto).
        has_visa (bool): Indica si el usuario tiene visa.

    Returns:
        tuple: Una tupla (ruta, costo_total) si existe una ruta, o (None, inf) si no hay ruta válida.
    """

    # Validación: no puede iniciar o terminar en nodo con visa si no la tiene
    if not has_visa:
        if graph.requires_visa(start) or graph.requires_visa(end):
            return None, float('inf')

    # Inicialización de distancias y heap de prioridad
    dist = {node: float('inf') for node in graph.nodes}
    prev = {}
    dist[start] = 0
    heap = [(0, start)]  # Tupla (costo acumulado, nodo)

    # Búsqueda de camino mínimo (Dijkstra)
    while heap:
        cost_u, u = heapq.heappop(heap)
        if u == end:
            break
        if cost_u > dist[u]:
            continue
        for v, w in graph.neighbors(u):
            # Omitir destinos que requieren visa si no la tiene
            if not has_visa and graph.requires_visa(v):
                continue
            alt = cost_u + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    if dist[end] == float('inf'):
        return None, float('inf')

    # Reconstruir ruta a partir del diccionario prev
    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()

    return path, dist[end]


def shortest_path_stops(graph: Graph, start: str, end: str, has_visa: bool):
    """
    Calcula la ruta con menor número de escalas (menor número de aristas) entre dos nodos
    usando el algoritmo de búsqueda en anchura (BFS), respetando las restricciones de visa.

    Args:
        graph (Graph): Grafo de destinos y rutas.
        start (str): Nodo de inicio (código de aeropuerto).
        end (str): Nodo destino (código de aeropuerto).
        has_visa (bool): Indica si el usuario tiene visa.

    Returns:
        tuple: Una tupla (ruta, escalas) si existe una ruta, o (None, inf) si no hay ruta válida.
    """

    # Validación de restricciones de visa
    if not has_visa:
        if graph.requires_visa(start) or graph.requires_visa(end):
            return None, float('inf')

    visited = {start}
    prev = {}
    queue = deque([start])

    # Búsqueda BFS
    while queue:
        u = queue.popleft()
        if u == end:
            break
        for v, _ in graph.neighbors(u):
            if v not in visited:
                if not has_visa and graph.requires_visa(v):
                    continue
                visited.add(v)
                prev[v] = u
                queue.append(v)

    if end not in visited:
        return None, float('inf')

    # Reconstruir ruta
    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()

    # Número de escalas = número de aristas entre nodos intermedios (sin contar origen y destino)
    escalas = max(len(path) - 2, 0)
    return path, escalas


if __name__ == "__main__":
    # Prueba rápida de los algoritmos con visa = False
    from data_manager import read_destinos, read_tarifas

    destinos = read_destinos('data/destinos.txt')
    tarifas = read_tarifas('data/tarifas.txt')
    g = Graph()
    g.load_from_data(destinos, tarifas)

    ruta_costo, costo = shortest_path_cost(g, 'CCS', 'SXM', has_visa=False)
    print("Ruta mínimo costo (sin visa):", ruta_costo, "Costo:", costo)

    ruta_escalas, escalas = shortest_path_stops(g, 'CCS', 'SXM', has_visa=False)
    print("Ruta mínimo escalas (sin visa):", ruta_escalas, "Escalas:", escalas)
