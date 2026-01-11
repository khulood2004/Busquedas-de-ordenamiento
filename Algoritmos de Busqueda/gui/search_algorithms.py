import tkinter as tk
from tkinter import ttk
from algoritmos.data_manager import DataManager

class SearchAlgorithmScreen(tk.Toplevel):
    def __init__(self, master, data_manager: DataManager, on_back_callback=None):
        super().__init__(master)

        self.dm = data_manager
        self.on_back = on_back_callback

        self.title("Ejecución de Algoritmos")
        self.geometry("800x600") # Un poco más alto para el botón volver
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self.selected_algorithm = tk.StringVar()
        self.show_graph = tk.BooleanVar(value=False)

        self._center()
        self.create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"800x600+{x}+{y}")

    def create_widgets(self):
        # -------- TÍTULO --------
        tk.Label(
            self,
            text="ALGORITMOS - BÚSQUEDA / OTROS",
            font=("Helvetica", 16, "bold"),
            bg="#f6f1e7"
        ).pack(pady=15)

        main_frame = tk.Frame(self, bg="#f6f1e7")
        main_frame.pack(fill="both", expand=True, padx=15)

        # -------- PANEL IZQUIERDO --------
        left_frame = tk.LabelFrame(
            main_frame,
            text="Selección de Algoritmo",
            font=("Helvetica", 10, "bold"),
            bg="#e4efd9",
            fg="#2e3d2f",
            bd=2
        )
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Opciones originales restauradas
        algorithms = [
            "Búsqueda Iterativa",
            "Búsqueda Recursiva",
            "Karatsuba",
            "Strassen",
            "PI (10000 cifras)"
        ]

        for alg in algorithms:
            ttk.Radiobutton(
                left_frame,
                text=alg,
                value=alg,
                variable=self.selected_algorithm
            ).pack(anchor="w", padx=15, pady=5)

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
        
        # Botón Volver agregado
        ttk.Button(
            left_frame,
            text="⬅ Volver",
            command=self._go_back
        ).pack(side="bottom", pady=20, fill="x", padx=15)

        # -------- PANEL DERECHO --------
        right_frame = tk.LabelFrame(
            main_frame,
            text="Resultados",
            font=("Helvetica", 10, "bold"),
            bg="#e4efd9",
            fg="#2e3d2f",
            bd=2
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ---- Tiempo ----
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

        # ---- Salida ----
        tk.Label(
            right_frame,
            text="Salida / Resultado:",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w", padx=5, pady=(10, 0))

        self.output_text = tk.Text(
            right_frame,
            height=8,
            state="disabled",
            wrap="word"
        )
        self.output_text.pack(padx=10, pady=5, fill="x")

        # ---- Área de gráfico ----
        tk.Label(
            right_frame,
            text="Gráfico:",
            bg="#e4efd9",
            font=("Helvetica", 9, "bold")
        ).pack(anchor="w", padx=5, pady=(10, 0))

        self.graph_placeholder = tk.Label(
            right_frame,
            text="📊 El gráfico se mostrará aquí",
            bg="#ffffff",
            fg="gray",
            relief="solid",
            height=8
        )
        self.graph_placeholder.pack(fill="both", padx=10, pady=5, expand=True)

    def _execute_algorithm(self):
        alg = self.selected_algorithm.get()

        if not alg:
            self._write_output("⚠️ Seleccione un algoritmo antes de ejecutar.")
            return

        self._set_time("0.00")

        result_text = (
            f"Algoritmo seleccionado:\n{alg}\n\n"
            "Resultados pendientes de implementación.\n"
            "(Nota: Los datos ya fueron ordenados internamente con QuickSort)"
        )

        if self.show_graph.get():
            result_text += "\n\n✔ Opción de gráfico activada."
            self.graph_placeholder.config(
                text="📈 Gráfico generado (placeholder)",
                fg="#2e3d2f"
            )
        else:
            self.graph_placeholder.config(
                text="📊 El gráfico se mostrará aquí",
                fg="gray"
            )

        self._write_output(result_text)

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