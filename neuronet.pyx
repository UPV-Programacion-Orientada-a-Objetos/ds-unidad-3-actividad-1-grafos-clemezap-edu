# neuronet.pyx
# Wrapper Cython para exponer funcionalidad C++ a Python

from neuronet_lib cimport GrafoDisperso
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.pair cimport pair

cdef class PyGrafoDisperso:
    """
    Wrapper Python para la clase C++ GrafoDisperso.
    Expone toda la funcionalidad del núcleo C++ a Python.
    """
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++
    
    def __cinit__(self):
        """Constructor: Crea una nueva instancia del grafo C++"""
        self.c_grafo = new GrafoDisperso()
    
    def __dealloc__(self):
        """Destructor: Libera la memoria del grafo C++"""
        del self.c_grafo
    
    def cargar_datos(self, str archivo):
        """
        Carga un dataset desde un archivo de texto.
        
        Args:
            archivo (str): Ruta al archivo de datos (formato Edge List)
        """
        cdef string archivo_cpp = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(archivo_cpp)
    
    def bfs(self, int nodo_inicio, int profundidad):
        """
        Ejecuta BFS (Búsqueda en Anchura) desde un nodo dado.
        
        Args:
            nodo_inicio (int): Nodo de inicio
            profundidad (int): Profundidad máxima de búsqueda
            
        Returns:
            list: Lista de nodos visitados
        """
        cdef vector[int] resultado = self.c_grafo.BFS(nodo_inicio, profundidad)
        return list(resultado)
    
    def obtener_grado(self, int nodo):
        """
        Obtiene el grado (número de conexiones) de un nodo.
        
        Args:
            nodo (int): ID del nodo
            
        Returns:
            int: Grado del nodo
        """
        return self.c_grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, int nodo):
        """
        Obtiene la lista de vecinos de un nodo.
        
        Args:
            nodo (int): ID del nodo
            
        Returns:
            list: Lista de IDs de nodos vecinos
        """
        cdef vector[int] vecinos = self.c_grafo.getVecinos(nodo)
        return list(vecinos)
    
    def get_nodos(self):
        """
        Obtiene el número total de nodos en el grafo.
        
        Returns:
            int: Número de nodos
        """
        return self.c_grafo.getNodos()
    
    def get_aristas(self):
        """
        Obtiene el número total de aristas en el grafo.
        
        Returns:
            int: Número de aristas
        """
        return self.c_grafo.getAristas()
    
    def get_nodo_mayor_grado(self):
        """
        Encuentra el nodo con mayor grado (más conexiones).
        
        Returns:
            int: ID del nodo con mayor grado
        """
        return self.c_grafo.getNodoMayorGrado()
    
    def get_aristas_bfs(self, int nodo_inicio, int profundidad):
        """
        Obtiene las aristas del subgrafo resultante de un BFS.
        
        Args:
            nodo_inicio (int): Nodo de inicio
            profundidad (int): Profundidad máxima
            
        Returns:
            list: Lista de tuplas (origen, destino) representando aristas
        """
        cdef vector[pair[int, int]] aristas = self.c_grafo.getAristasBFS(nodo_inicio, profundidad)
        return [(arista.first, arista.second) for arista in aristas]
    
    def imprimir_estadisticas(self):
        """
        Imprime estadísticas del grafo en consola.
        """
        self.c_grafo.imprimirEstadisticas()