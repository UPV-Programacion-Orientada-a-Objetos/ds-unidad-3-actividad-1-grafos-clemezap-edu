#ifndef GRAPH_CORE_HPP
#define GRAPH_CORE_HPP

#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>

// Clase Abstracta Base para Grafos
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    
    // Métodos virtuales puros
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual std::vector<int> BFS(int nodoInicio, int profundidad) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual std::vector<int> getVecinos(int nodo) = 0;
    virtual int getNodos() const = 0;
    virtual int getAristas() const = 0;
    virtual int getNodoMayorGrado() = 0;
    virtual std::vector<std::pair<int, int>> getAristasBFS(int nodoInicio, int profundidad) = 0;
};

// Clase Concreta: Grafo Disperso con CSR
class GrafoDisperso : public GrafoBase {
private:
    // Estructura CSR (Compressed Sparse Row)
    std::vector<int> values;        // Valores (nodos destino)
    std::vector<int> col_indices;   // Índices de columnas (mismo que values)
    std::vector<int> row_ptr;       // Punteros de inicio de fila
    
    int num_nodos;
    int num_aristas;
    
    // Mapeo de IDs originales a índices consecutivos
    std::unordered_map<int, int> nodo_a_indice;
    std::unordered_map<int, int> indice_a_nodo;
    
    // Construir estructura CSR desde lista de aristas
    void construirCSR(std::vector<std::pair<int, int>>& aristas);
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    // Implementación de métodos virtuales
    void cargarDatos(const std::string& archivo) override;
    std::vector<int> BFS(int nodoInicio, int profundidad) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    int getNodos() const override;
    int getAristas() const override;
    int getNodoMayorGrado() override;
    std::vector<std::pair<int, int>> getAristasBFS(int nodoInicio, int profundidad) override;
    
    // Métodos auxiliares
    void imprimirEstadisticas() const;
};

#endif // GRAPH_CORE_HPP