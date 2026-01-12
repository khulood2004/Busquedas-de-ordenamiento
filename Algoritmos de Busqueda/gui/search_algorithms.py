import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algoritmos.data_manager import DataManager
from algoritmos import searches
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


class MethodChoiceDialog(tk.Toplevel):
    """Ventana para elegir Iterativa o Recursiva."""
    def __init__(self, master, on_choose):
        super().__init__(master)
        self.on_choose = on_choose

        self.title("Método de búsqueda")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        w, h = 300, 150
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(
            self,
            text="Seleccione el método:",
            font=("Helvetica", 11, "bold"),
            bg="#f6f1e7"
        ).pack(pady=15)

        btn_frame = tk.Frame(self, bg="#f6f1e7")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Iterativa",
            command=lambda: self._choose("iterative")
        ).pack(side="left", padx=10)

        ttk.Button(
            btn_frame,
            text="Recursiva",
            command=lambda: self._choose("recursive")
        ).pack(side="left", padx=10)

    def _choose(self, mode: str):
        self.destroy()
        self.on_choose(mode)


class SearchAlgorithmScreen(tk.Toplevel):
    def __init__(self, master, data_manager: DataManager, on_back_callback=None):
        super().__init__(master)

        self.dm = data_manager
        self.on_back = on_back_callback

        self.selected_algorithm = tk.StringVar()
        self.show_graph = tk.BooleanVar(value=False)

        self.title("Ejecución de Algoritmos de Búsqueda")
        self.geometry("900x620")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self._center()
        self.create_widgets()
        self._refresh_data_view()

    def _center(self):
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 620) // 2
        self.geometry(f"900x620+{x}+{y}")

    def create_widgets(self):
        # ---------- TÍTULO ----------
        tk.Label(
            self,
            text="ALGORITMOS DE BÚSQUEDA",
            font=("Helvetica", 16, "bold"),
            bg="#f6f1e7"
        ).pack(pady=15)

        main_frame = tk.Frame(self, bg="#f6f1e7")
        main_frame.pack(fill="both", expand=True, padx=15)

        # ---------- PANEL IZQUIERDO ----------
        left_frame = tk.LabelFrame(
            main_frame,
            text="Selección de Búsqueda",
            bg="#e4efd9",
            fg="#2e3d2f",
            font=("Helvetica", 10, "bold"),
            bd=2
        )
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Radiobutton(
            left_frame,
            text="Búsqueda Lineal",
            value="LINEAL",
            variable=self.selected_algorithm
        ).pack(anchor="w", padx=15, pady=5)

        if self.dm.order_mode == "ordered":
            ttk.Radiobutton(
                left_frame,
                text="Búsqueda Binaria",
                value="BINARIA",
                variable=self.selected_algorithm
            ).pack(anchor="w", padx=15, pady=5)
        else:
            tk.Label(
                left_frame,
                text="(Binaria solo con datos ordenados)",
                bg="#e4efd9",
                fg="#555",
                font=("Helvetica", 8, "italic")
            ).pack(anchor="w", padx=18, pady=(0, 8))

        ttk.Checkbutton(
            left_frame,
            text="Mostrar gráfico",
            variable=self.show_graph
        ).pack(anchor="w", padx=15, pady=(10, 5))

        ttk.Button(
            left_frame,
            text="Ejecutar",
            command=self._execute_algorithm
        ).pack(pady=15)

        ttk.Button(
            left_frame,
            text="⬅ Volver",
            command=self._go_back
        ).pack(side="bottom", pady=20, fill="x", padx=15)

        # ---------- PANEL DERECHO ----------
        right_frame = tk.LabelFrame(
            main_frame,
            text="Resultados",
            bg="#e4efd9",
            fg="#2e3d2f",
            font=("Helvetica", 10, "bold"),
            bd=2
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Tiempo
        time_frame = tk.Frame(right_frame, bg="#e4efd9")
        time_frame.pack(fill="x", pady=5)

        tk.Label(
            time_frame,
            text="Tiempo de ejecución (ms):",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(side="left", padx=5)

        self.time_entry = tk.Entry(time_frame, width=15, state="readonly")
        self.time_entry.pack(side="left", padx=5)

        # Número a buscar
        target_frame = tk.Frame(right_frame, bg="#e4efd9")
        target_frame.pack(fill="x", pady=5)

        tk.Label(
            target_frame,
            text="Número a buscar:",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(side="left", padx=5)

        self.target_entry = tk.Entry(target_frame, width=20)
        self.target_entry.pack(side="left", padx=5)

        # Datos cargados
        data_frame = tk.LabelFrame(
            right_frame,
            text="Datos cargados / generados",
            bg="#e4efd9",
            fg="#2e3d2f",
            font=("Helvetica", 9, "bold"),
            bd=1
        )
        data_frame.pack(fill="x", padx=10, pady=8)

        self.data_text = tk.Text(
            data_frame,
            height=2,          
            wrap="none"
        )
        self.data_text.pack(fill="x", padx=5)

        h_scroll = tk.Scrollbar(
            data_frame,
            orient="horizontal",
            command=self.data_text.xview
        )
        h_scroll.pack(fill="x")

        self.data_text.configure(xscrollcommand=h_scroll.set)

        # Salida
        tk.Label(
            right_frame,
            text="Salida / Resultado:",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.output_text = tk.Text(right_frame, height=4, state="disabled", wrap="word")
        self.output_text.pack(padx=10, pady=5, fill="x")

        # Gráfico
        tk.Label(
            right_frame,
            text="Gráfico:",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.graph_placeholder = tk.Frame(
            right_frame,
            bg="#ffffff",
            relief="solid",
            bd=1
        )
        self.graph_placeholder.pack(fill="both", padx=10, pady=5, expand=True)

    # ---------- MÉTODOS AUXILIARES ----------
    def _refresh_data_view(self):
        data = self.dm.get_data_copy()
        txt = ", ".join(map(str, data)) if data else "(Sin datos)"
        self.data_text.config(state="normal")
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, txt)
        self.data_text.config(state="disabled")

    def _set_time(self, value: str):
        self.time_entry.config(state="normal")
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, value)
        self.time_entry.config(state="readonly")

    def _write_output(self, text: str):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")

    def _go_back(self):
        self.destroy()
        if self.on_back:
            self.on_back()

    # ---------- EJECUCIÓN ----------
    def _execute_algorithm(self):
        self._refresh_data_view()
        alg = self.selected_algorithm.get()

        if not alg:
            self._write_output("⚠️ Seleccione un algoritmo de búsqueda.")
            return

        raw = self.target_entry.get().strip()
        if not raw:
            messagebox.showwarning("Falta dato", "Ingrese el número a buscar.")
            return

        try:
            target = int(raw)
        except ValueError:
            messagebox.showerror("Dato inválido", "El número a buscar debe ser un entero.")
            return

        MethodChoiceDialog(
            self,
            on_choose=lambda mode: self._run_search(alg, mode, target)
        )

    def _run_search(self, alg: str, mode: str, target: int):
        data = self.dm.get_data_copy()

        start = time.perf_counter()

        if alg == "LINEAL":
            if mode == "iterative":
                idx = searches.linear_search_iterative(data, target)
                name = "Búsqueda Lineal Iterativa"
            else:
                idx = searches.linear_search_recursive(data, target)
                name = "Búsqueda Lineal Recursiva"
        else:
            if mode == "iterative":
                idx = searches.binary_search_iterative(data, target)
                name = "Búsqueda Binaria Iterativa"
            else:
                idx = searches.binary_search_recursive(data, target)
                name = "Búsqueda Binaria Recursiva"

        end = time.perf_counter()
        self._set_time(f"{(end - start) * 1000:.2f}")

        if idx == -1:
            self._write_output(
                f"{name}\n\n"
                f"Resultado: el valor {target} NO se encontró.\n"
                f"Tamaño de datos: {len(data)}"
            )
        else:
            self._write_output(
                f"{name}\n\n"
                f"Resultado: el valor {target} se encontró en el índice {idx}.\n"
                f"Tamaño de datos: {len(data)}"
            )
        
        # ---------- GRÁFICO DE RENDIMIENTO ----------
        if self.show_graph.get():
            sizes = []
            times = []

            full_data = data
            max_n = len(full_data)

            # Definir tamaños de prueba (ajustados al tamaño real)
            test_sizes = [50, 100, 300, 500, 1000]
            test_sizes = [n for n in test_sizes if n <= max_n]

            for n in test_sizes:
                subset = full_data[:n]

                start = time.perf_counter()

                if alg == "LINEAL":
                    if mode == "iterative":
                        searches.linear_search_iterative(subset, target)
                    else:
                        searches.linear_search_recursive(subset, target)
                else:
                    if mode == "iterative":
                        searches.binary_search_iterative(subset, target)
                    else:
                        searches.binary_search_recursive(subset, target)

                end = time.perf_counter()

                sizes.append(n)
                times.append((end - start) * 1000)

            title = f"Tiempo vs Tamaño ({name})"
            self._draw_performance_graph(sizes, times, title)

    def _draw_performance_graph(self, sizes, times, title):
        """
        Dibuja el gráfico comparativo: busqueda lineal vs busqueda binaria
        """

        # Limpiar el placeholder anterior
        for widget in self.graph_placeholder.winfo_children():
            widget.destroy()

        # Crear figura
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.plot(sizes, times, marker="o")
        ax.set_xlabel("Tamaño de datos (n)")
        ax.set_ylabel("Tiempo de ejecución (ms)")
        ax.set_title(title)
        ax.grid(True)

        # Insertar figura en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_placeholder)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        # Barra de herramientas (zoom, pan, mover con mano)
        toolbar = NavigationToolbar2Tk(canvas, self.graph_placeholder)
        toolbar.update()
        toolbar.pan() 
