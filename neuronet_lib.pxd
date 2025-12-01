# neuronet_lib.pxd
# Definiciones Cython para interfaz con C++

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.pair cimport pair

# Declaración de la clase abstracta base
cdef extern from "graph_core.hpp":
    cdef cppclass GrafoBase:
        void cargarDatos(const string& archivo) except +
        vector[int] BFS(int nodoInicio, int profundidad) except +
        int obtenerGrado(int nodo) except +
        vector[int] getVecinos(int nodo) except +
        int getNodos() except +
        int getAristas() except +
        int getNodoMayorGrado() except +
        vector[pair[int, int]] getAristasBFS(int nodoInicio, int profundidad) except +

# Declaración de la clase concreta
cdef extern from "graph_core.hpp":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(const string& archivo) except +
        vector[int] BFS(int nodoInicio, int profundidad) except +
        int obtenerGrado(int nodo) except +
        vector[int] getVecinos(int nodo) except +
        int getNodos() except +
        int getAristas() except +
        int getNodoMayorGrado() except +
        vector[pair[int, int]] getAristasBFS(int nodoInicio, int profundidad) except +
        void imprimirEstadisticas() except +