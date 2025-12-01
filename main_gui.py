"""
main_gui.py - Interfaz Gráfica de Usuario para NeuroNet
Utiliza Tkinter para la GUI y NetworkX/Matplotlib solo para visualización
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import neuronet
import time
import threading

class NeuroNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet: Análisis de Grafos Masivos")
        self.root.geometry("1200x800")
        
        # Instancia del grafo C++
        self.grafo = neuronet.PyGrafoDisperso()
        self.archivo_cargado = None
        
        # Configurar interfaz
        self.setup_ui()
        
    def setup_ui(self):
        """Configura todos los componentes de la interfaz"""
        
        # Frame superior: Controles
        frame_controles = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        # Botón para cargar archivo
        btn_cargar = tk.Button(
            frame_controles,
            text="📁 Cargar Dataset",
            command=self.cargar_archivo,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        # Botón para análisis
        btn_analisis = tk.Button(
            frame_controles,
            text="📊 Nodo Mayor Grado",
            command=self.analizar_mayor_grado,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_analisis.pack(side=tk.LEFT, padx=5)
        
        # Frame para BFS
        frame_bfs = tk.Frame(frame_controles, bg="#2c3e50")
        frame_bfs.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            frame_bfs,
            text="Nodo Inicio:",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_nodo = tk.Entry(frame_bfs, width=10, font=("Arial", 10))
        self.entry_nodo.pack(side=tk.LEFT, padx=5)
        self.entry_nodo.insert(0, "0")
        
        tk.Label(
            frame_bfs,
            text="Profundidad:",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_profundidad = tk.Entry(frame_bfs, width=5, font=("Arial", 10))
        self.entry_profundidad.pack(side=tk.LEFT, padx=5)
        self.entry_profundidad.insert(0, "2")
        
        btn_bfs = tk.Button(
            frame_bfs,
            text="🔍 Ejecutar BFS",
            command=self.ejecutar_bfs,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        btn_bfs.pack(side=tk.LEFT, padx=5)
        
        # Frame central: Información y visualización
        frame_central = tk.Frame(self.root)
        frame_central.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo: Métricas
        frame_metricas = tk.LabelFrame(
            frame_central,
            text="📈 Métricas del Grafo",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_metricas.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.text_metricas = tk.Text(
            frame_metricas,
            width=35,
            height=20,
            font=("Consolas", 10),
            bg="#34495e",
            fg="#ecf0f1",
            wrap=tk.WORD
        )
        self.text_metricas.pack(fill=tk.BOTH, expand=True)
        
        # Panel derecho: Visualización
        frame_visualizacion = tk.LabelFrame(
            frame_central,
            text="🎨 Visualización de Subgrafo",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame_visualizacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas para matplotlib
        self.figura = plt.Figure(figsize=(8, 6), dpi=100, facecolor='#ecf0f1')
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_visualizacion)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial
        self.actualizar_metricas("Esperando datos...\n\n💡 Carga un dataset para comenzar.")
        
    def actualizar_metricas(self, texto):
        """Actualiza el panel de métricas"""
        self.text_metricas.delete(1.0, tk.END)
        self.text_metricas.insert(tk.END, texto)
        
    def cargar_archivo(self):
        """Carga un archivo de dataset"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        self.actualizar_metricas("⏳ Cargando archivo...\nEsto puede tomar unos momentos.\n")
        self.root.update()
        
        # Cargar en un hilo separado para no bloquear la GUI
        def cargar_thread():
            try:
                inicio = time.time()
                self.grafo.cargar_datos(archivo)
                fin = time.time()
                
                self.archivo_cargado = archivo
                
                # Obtener métricas
                num_nodos = self.grafo.get_nodos()
                num_aristas = self.grafo.get_aristas()
                tiempo_carga = fin - inicio
                
                # Actualizar interfaz
                metricas = f"""
✅ DATASET CARGADO EXITOSAMENTE

📁 Archivo: {archivo.split('/')[-1]}

📊 ESTADÍSTICAS:
  • Nodos: {num_nodos:,}
  • Aristas: {num_aristas:,}
  • Tiempo de carga: {tiempo_carga:.2f}s

💾 El dataset ha sido cargado en 
   estructura CSR (Compressed Sparse Row)
   optimizada para memoria.

🎯 Usa los botones superiores para:
   - Encontrar el nodo más crítico
   - Ejecutar búsquedas BFS
   - Visualizar subgrafos
                """
                
                self.root.after(0, self.actualizar_metricas, metricas)
                self.root.after(0, messagebox.showinfo, "Éxito", 
                               f"Dataset cargado:\n{num_nodos:,} nodos\n{num_aristas:,} aristas")
                
            except Exception as e:
                error_msg = f"❌ ERROR al cargar archivo:\n\n{str(e)}"
                self.root.after(0, self.actualizar_metricas, error_msg)
                self.root.after(0, messagebox.showerror, "Error", str(e))
        
        thread = threading.Thread(target=cargar_thread)
        thread.start()
        
    def analizar_mayor_grado(self):
        """Encuentra el nodo con mayor grado"""
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
        
        try:
            self.actualizar_metricas("⏳ Analizando grados de nodos...")
            self.root.update()
            
            inicio = time.time()
            nodo_max = self.grafo.get_nodo_mayor_grado()
            grado_max = self.grafo.obtener_grado(nodo_max)
            fin = time.time()
            
            resultado = f"""
🎯 ANÁLISIS DE CENTRALIDAD

🏆 NODO MÁS CRÍTICO:
  • ID del Nodo: {nodo_max}
  • Grado (conexiones): {grado_max}
  • Tiempo de análisis: {(fin-inicio)*1000:.2f}ms

📊 Este nodo tiene el mayor número de
   conexiones en toda la red, lo que lo
   convierte en un punto crítico.

💡 Un fallo en este nodo podría afectar
   significativamente la conectividad
   de la red.
            """
            
            self.actualizar_metricas(resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis:\n{str(e)}")
            
    def ejecutar_bfs(self):
        """Ejecuta BFS y visualiza el resultado"""
        if not self.archivo_cargado:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
        
        try:
            nodo_inicio = int(self.entry_nodo.get())
            profundidad = int(self.entry_profundidad.get())
            
            if profundidad < 1 or profundidad > 5:
                messagebox.showwarning("Advertencia", "La profundidad debe estar entre 1 y 5")
                return
            
            self.actualizar_metricas(f"⏳ Ejecutando BFS desde nodo {nodo_inicio}...")
            self.root.update()
            
            inicio = time.time()
            nodos_visitados = self.grafo.bfs(nodo_inicio, profundidad)
            aristas = self.grafo.get_aristas_bfs(nodo_inicio, profundidad)
            fin = time.time()
            
            # Actualizar métricas
            metricas = f"""
🔍 BÚSQUEDA BFS COMPLETADA

📍 PARÁMETROS:
  • Nodo inicio: {nodo_inicio}
  • Profundidad: {profundidad}

📊 RESULTADOS:
  • Nodos encontrados: {len(nodos_visitados)}
  • Aristas en subgrafo: {len(aristas)}
  • Tiempo de ejecución: {(fin-inicio)*1000:.2f}ms

🎨 El subgrafo resultante se muestra
   en el panel de visualización.

💡 Los nodos están organizados según
   su distancia desde el nodo inicial.
            """
            
            self.actualizar_metricas(metricas)
            
            # Visualizar
            self.visualizar_subgrafo(nodos_visitados, aristas, nodo_inicio)
            
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error en BFS:\n{str(e)}")
            
    def visualizar_subgrafo(self, nodos, aristas, nodo_inicio):
        """Visualiza el subgrafo usando NetworkX (solo para dibujo)"""
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        
        # Crear grafo de NetworkX SOLO para visualización
        G = nx.DiGraph()
        G.add_edges_from(aristas)
        
        # Limitar visualización si hay demasiados nodos
        if len(nodos) > 100:
            mensaje = f"Subgrafo con {len(nodos)} nodos\n(Mostrando estructura simplificada)"
            ax.text(0.5, 0.5, mensaje, ha='center', va='center', 
                   fontsize=14, transform=ax.transAxes)
            ax.set_xlim([0, 1])
            ax.set_ylim([0, 1])
            ax.axis('off')
        else:
            # Layout radial centrado en el nodo inicial
            pos = nx.spring_layout(G, k=1.5, iterations=50)
            
            # Colorear nodos
            colores = ['#e74c3c' if n == nodo_inicio else '#3498db' for n in G.nodes()]
            tamaños = [800 if n == nodo_inicio else 300 for n in G.nodes()]
            
            # Dibujar
            nx.draw_networkx_nodes(G, pos, node_color=colores, 
                                  node_size=tamaños, alpha=0.8, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='#95a5a6', 
                                  arrows=True, alpha=0.5, ax=ax,
                                  arrowsize=10, width=1.5)
            nx.draw_networkx_labels(G, pos, font_size=8, 
                                   font_color='white', ax=ax)
            
            ax.set_title(f"Subgrafo BFS desde Nodo {nodo_inicio}", 
                        fontsize=12, fontweight='bold')
            ax.axis('off')
        
        self.canvas.draw()

def main():
    """Función principal"""
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("="*60)
    print("  NeuroNet: Sistema de Análisis de Grafos Masivos")
    print("  Iniciando interfaz gráfica...")
    print("="*60)
    main()