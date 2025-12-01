#include "graph_core.hpp"

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {
    std::cout << "[C++ Core] Liberando memoria de GrafoDisperso..." << std::endl;
}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "[C++ Core] ERROR: No se pudo abrir el archivo " << archivo << std::endl;
        return;
    }
    
    std::vector<std::pair<int, int>> aristas_temp;
    std::string linea;
    int nodo_origen, nodo_destino;
    
    // Leer archivo línea por línea
    while (std::getline(file, linea)) {
        // Ignorar comentarios
        if (linea.empty() || linea[0] == '#') continue;
        
        std::istringstream iss(linea);
        if (iss >> nodo_origen >> nodo_destino) {
            aristas_temp.push_back({nodo_origen, nodo_destino});
            
            // Construir mapeo de nodos
            if (nodo_a_indice.find(nodo_origen) == nodo_a_indice.end()) {
                int idx = nodo_a_indice.size();
                nodo_a_indice[nodo_origen] = idx;
                indice_a_nodo[idx] = nodo_origen;
            }
            if (nodo_a_indice.find(nodo_destino) == nodo_a_indice.end()) {
                int idx = nodo_a_indice.size();
                nodo_a_indice[nodo_destino] = idx;
                indice_a_nodo[idx] = nodo_destino;
            }
        }
    }
    file.close();
    
    num_nodos = nodo_a_indice.size();
    num_aristas = aristas_temp.size();
    
    // Construir estructura CSR
    construirCSR(aristas_temp);
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::milliseconds>(fin - inicio);
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos 
              << " | Aristas: " << num_aristas << std::endl;
    std::cout << "[C++ Core] Tiempo de carga: " << duracion.count() << "ms" << std::endl;
    
    // Estimar memoria (aproximado)
    size_t memoria_bytes = (values.size() + col_indices.size() + row_ptr.size()) * sizeof(int);
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " 
              << memoria_bytes / (1024 * 1024) << " MB." << std::endl;
}

void GrafoDisperso::construirCSR(std::vector<std::pair<int, int>>& aristas) {
    // Convertir IDs originales a índices
    std::vector<std::pair<int, int>> aristas_indexadas;
    for (const auto& arista : aristas) {
        int src = nodo_a_indice[arista.first];
        int dst = nodo_a_indice[arista.second];
        aristas_indexadas.push_back({src, dst});
    }
    
    // Ordenar aristas por nodo origen
    std::sort(aristas_indexadas.begin(), aristas_indexadas.end());
    
    // Construir vectores CSR
    row_ptr.resize(num_nodos + 1, 0);
    
    for (const auto& arista : aristas_indexadas) {
        values.push_back(arista.second);
        col_indices.push_back(arista.second);
    }
    
    // Construir row_ptr
    int idx_actual = 0;
    for (int i = 0; i < num_nodos; i++) {
        row_ptr[i] = idx_actual;
        while (idx_actual < aristas_indexadas.size() && 
               aristas_indexadas[idx_actual].first == i) {
            idx_actual++;
        }
    }
    row_ptr[num_nodos] = aristas_indexadas.size();
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int profundidad) {
    std::cout << "[Cython] Solicitud recibida: BFS desde Nodo " 
              << nodoInicio << ", Profundidad " << profundidad << "." << std::endl;
    std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::vector<int> nodos_visitados;
    
    // Verificar si el nodo existe
    if (nodo_a_indice.find(nodoInicio) == nodo_a_indice.end()) {
        std::cerr << "[C++ Core] ERROR: Nodo " << nodoInicio << " no existe en el grafo." << std::endl;
        return nodos_visitados;
    }
    
    int idx_inicio = nodo_a_indice[nodoInicio];
    
    std::vector<bool> visitado(num_nodos, false);
    std::vector<int> nivel(num_nodos, -1);
    std::queue<int> cola;
    
    cola.push(idx_inicio);
    visitado[idx_inicio] = true;
    nivel[idx_inicio] = 0;
    nodos_visitados.push_back(indice_a_nodo[idx_inicio]);
    
    while (!cola.empty()) {
        int nodo_actual = cola.front();
        cola.pop();
        
        int nivel_actual = nivel[nodo_actual];
        if (nivel_actual >= profundidad) continue;
        
        // Obtener vecinos usando CSR
        int inicio_vecinos = row_ptr[nodo_actual];
        int fin_vecinos = row_ptr[nodo_actual + 1];
        
        for (int i = inicio_vecinos; i < fin_vecinos; i++) {
            int vecino = col_indices[i];
            if (!visitado[vecino]) {
                visitado[vecino] = true;
                nivel[vecino] = nivel_actual + 1;
                cola.push(vecino);
                nodos_visitados.push_back(indice_a_nodo[vecino]);
            }
        }
    }
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio);
    
    std::cout << "[C++ Core] Nodos encontrados: " << nodos_visitados.size() 
              << ". Tiempo ejecución: " << duracion.count() / 1000.0 << "ms." << std::endl;
    std::cout << "[Cython] Retornando lista de adyacencia local a Python." << std::endl;
    
    return nodos_visitados;
}

std::vector<std::pair<int, int>> GrafoDisperso::getAristasBFS(int nodoInicio, int profundidad) {
    std::vector<std::pair<int, int>> aristas_resultado;
    
    if (nodo_a_indice.find(nodoInicio) == nodo_a_indice.end()) {
        return aristas_resultado;
    }
    
    int idx_inicio = nodo_a_indice[nodoInicio];
    
    std::vector<bool> visitado(num_nodos, false);
    std::vector<int> nivel(num_nodos, -1);
    std::queue<int> cola;
    
    cola.push(idx_inicio);
    visitado[idx_inicio] = true;
    nivel[idx_inicio] = 0;
    
    while (!cola.empty()) {
        int nodo_actual = cola.front();
        cola.pop();
        
        int nivel_actual = nivel[nodo_actual];
        if (nivel_actual >= profundidad) continue;
        
        int inicio_vecinos = row_ptr[nodo_actual];
        int fin_vecinos = row_ptr[nodo_actual + 1];
        
        for (int i = inicio_vecinos; i < fin_vecinos; i++) {
            int vecino = col_indices[i];
            
            // Agregar arista al resultado
            aristas_resultado.push_back({indice_a_nodo[nodo_actual], indice_a_nodo[vecino]});
            
            if (!visitado[vecino]) {
                visitado[vecino] = true;
                nivel[vecino] = nivel_actual + 1;
                cola.push(vecino);
            }
        }
    }
    
    return aristas_resultado;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo_a_indice.find(nodo) == nodo_a_indice.end()) {
        return 0;
    }
    
    int idx = nodo_a_indice[nodo];
    return row_ptr[idx + 1] - row_ptr[idx];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    
    if (nodo_a_indice.find(nodo) == nodo_a_indice.end()) {
        return vecinos;
    }
    
    int idx = nodo_a_indice[nodo];
    int inicio = row_ptr[idx];
    int fin = row_ptr[idx + 1];
    
    for (int i = inicio; i < fin; i++) {
        vecinos.push_back(indice_a_nodo[col_indices[i]]);
    }
    
    return vecinos;
}

int GrafoDisperso::getNodos() const {
    return num_nodos;
}

int GrafoDisperso::getAristas() const {
    return num_aristas;
}

int GrafoDisperso::getNodoMayorGrado() {
    int max_grado = 0;
    int nodo_max = -1;
    
    for (const auto& par : indice_a_nodo) {
        int idx = par.first;
        int nodo = par.second;
        int grado = row_ptr[idx + 1] - row_ptr[idx];
        
        if (grado > max_grado) {
            max_grado = grado;
            nodo_max = nodo;
        }
    }
    
    return nodo_max;
}

void GrafoDisperso::imprimirEstadisticas() const {
    std::cout << "=== Estadísticas del Grafo ===" << std::endl;
    std::cout << "Nodos: " << num_nodos << std::endl;
    std::cout << "Aristas: " << num_aristas << std::endl;
    std::cout << "=============================" << std::endl;
}