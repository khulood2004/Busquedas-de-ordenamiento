import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algoritmos.data_manager import DataManager
from algoritmos.stats_manager import StatsManager
import algoritmos.sorts as sorts


# helper para mostrar muestras
def format_array_for_display(arr, head=10, tail=10):
    n = len(arr)
    if n <= head + tail + 2:
        return str(arr)
    head_part = arr[:head]
    tail_part = arr[-tail:]
    return f"{head_part} ... {tail_part}  (total: {n})"


class SortersScreen(tk.Toplevel):
    # Adaptación: Agregamos on_back_callback para que funcione con tu nuevo menú
    def __init__(self, master=None, data_manager: DataManager=None, on_back_callback=None):
        super().__init__(master)
        self.title("Ordenamientos")
        
        self.WIDTH = 900
        self.HEIGHT= 700
        self.configure(bg="#0b0b0b")
        self.resizable(True, True)
        
        self.master_window = master
        self.on_back = on_back_callback  # Guardamos el callback de retorno
        
        self.dm = data_manager if data_manager else DataManager()
        self.stats = StatsManager()

        self.result_queue = queue.Queue()
        
        # Si cerramos la ventana con la X, intentamos usar el flujo de retorno
        self.protocol("WM_DELETE_WINDOW", self._go_back) 
            
        self._create_widgets()
        self._center_window()
        
    def _center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.WIDTH // 2)
        y = (screen_height // 2) - (self.HEIGHT // 2)
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{x}+{y}')

    def _create_widgets(self):
        top_frame = tk.Frame(self, bg="#0b0b0b")
        top_frame.pack(fill="x", padx=12, pady=10)

        left = tk.Frame(top_frame, bg="#0b0b0b")
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(top_frame, bg="#0b0b0b")
        right.pack(side="right", fill="y")

        # Algoritmos disponibles (RESTAURADOS TODOS)
        tk.Label(right, text="Seleccione un Algoritmo", bg="#333333", fg="white").pack(pady=(0,5))
        
        self.alg_var = tk.StringVar(value="quicksort_recursive")
        algs = [
            ("Bubble (mejorado)", "bubble_improved"),
            ("Insertion", "insertion_sort"),
            ("Selection", "selection_sort"),
            ("Shell", "shell_sort"),
            ("Quicksort (rec)", "quicksort_recursive"),
            ("Mergesort (rec)", "mergesort_recursive"),
        ]
        for text, val in algs:
            tk.Radiobutton(right, text=text, variable=self.alg_var, value=val, bg="black", fg="white", selectcolor="black").pack(anchor="w", padx=4, pady=2)

        ttk.Button(right, text="Ejecutar", command=self._on_run).pack(pady=8, fill="x", padx=6)
        # BOTON PARA MOSTRAR GRAFICO MATPLOT (Comentado original)
        # ttk.Button(right, text="Mostrar gráfico", command=self._show_time_graph).pack(pady=4, fill="x", padx=6)
        ttk.Button(right, text="Exportar estadísticas", command=self._export_stats).pack(pady=4, fill="x", padx=6)
        
        # Botón Regresar (Restaurado)
        ttk.Button(right, text="Regresar", command=self._go_back).pack(pady=4, fill="x", padx=6)

        # Muestras de arreglo
        info_frame = tk.Frame(left, bg="#0b0b0b")
        info_frame.pack(fill="both", expand=False, pady=4)

        tk.Label(info_frame, text="Arreglo original (muestra):", bg="#0b0b0b", fg="white").grid(row=0, column=0, sticky="w")
        self.orig_text = tk.Text(info_frame, height=3, width=80, bg="#111", fg="white", wrap="none")
        self.orig_text.grid(row=1, column=0, padx=4, pady=2)

        tk.Label(info_frame, text="Arreglo ordenado (muestra):", bg="#0b0b0b", fg="white").grid(row=2, column=0, sticky="w")
        self.sorted_text = tk.Text(info_frame, height=3, width=80, bg="#111", fg="white", wrap="none")
        self.sorted_text.grid(row=3, column=0, padx=4, pady=2)

        self.time_label = tk.Label(info_frame, text="Tiempo: -- ms", bg="#0b0b0b", fg="white", font=("Helvetica", 12, "bold"))
        self.time_label.grid(row=4, column=0, sticky="w", pady=(6,0))
        
        # Tabla comparativa
        table_frame = tk.Frame(self, bg="#0b0b0b")
        table_frame.pack(fill="both", expand=True, padx=12, pady=6)
        style = ttk.Style()
        style.theme_use("default")

        # Fondo de la tabla
        style.configure("Treeview",
            background="#333232",
            fieldbackground="#0b0b0b",
            foreground="white",
            borderwidth=0)

        # Color de la fila seleccionada
        style.map("Treeview",
          background=[("selected", "#333333")],
          foreground=[("selected", "white")])

        # Encabezados
        style.configure("Treeview.Heading",
                background="#1a1a1a",
                foreground="white",
                font=("Helvetica", 10, "bold"))
        
        self.tree = ttk.Treeview(table_frame, columns=("alg", "n", "ms"), show="headings", height=6)
        self.tree.heading("alg", text="Algoritmo")
        self.tree.heading("n", text="n")
        self.tree.heading("ms", text="ms")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _on_run(self):
        arr = self.dm.get_data_copy()
        if not arr:
            messagebox.showerror("Error", "No hay datos cargados.")
            return

        alg_key = self.alg_var.get()

        # Advertencia para arreglos grandes (Lógica Original)
        n = len(arr)
        if n > 100000 and alg_key in ("quicksort_recursive", "mergesort_recursive", "insertion_sort", "selection_sort", "bubble_improved"):
            msg = (
                f"El algoritmo seleccionado puede ser muy lento o agotar recursión con n = {n}.\n"
                f"¿Deseas continuar?"
            )
            if not messagebox.askyesno("Advertencia", msg):
                return

        thread = threading.Thread(target=self._run_sort_in_thread, args=(alg_key, arr), daemon=True)
        thread.start()

        self.time_label.config(text="Ejecutando...")

        self.after(100, self._check_result_queue)

    def _run_sort_in_thread(self, alg_key, arr):
        try:
            func = getattr(sorts, alg_key)
            sorted_arr, elapsed = func(arr)

            self.result_queue.put({
                'alg': alg_key,
                'n': len(arr),
                'ms': elapsed,
                'sorted': sorted_arr
            })

        except Exception as e:
            self.result_queue.put({'error': str(e)})

    def _check_result_queue(self):
        try:
            item = self.result_queue.get_nowait()
        except queue.Empty:
            self.after(100, self._check_result_queue)
            return

        if 'error' in item:
            messagebox.showerror("Error en ordenamiento", item['error'])
            self.time_label.config(text="Error")
            return

        alg = item['alg']
        n = item['n']
        ms = item['ms']
        sorted_arr = item['sorted']

        self.stats.add(alg, n, ms)

        self.orig_text.delete("1.0", "end")
        self.orig_text.insert("end", format_array_for_display(self.dm.base_data))

        self.sorted_text.delete("1.0", "end")
        self.sorted_text.insert("end", format_array_for_display(sorted_arr))

        self.time_label.config(text=f"Tiempo: {ms:.3f} ms  | Alg: {alg}  |  n: {n}")
        
        self.tree.insert("", "end", values=(alg, n, f"{ms:.3f}"))
        
    def _export_stats(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            self.stats.export_csv(path)
            messagebox.showinfo("Exportado", f"Estadísticas exportadas a {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _go_back(self):
        self.destroy()
        # Adaptación: Si tenemos un callback (del nuevo menú), lo usamos.
        if self.on_back:
            self.on_back()
        # Si no, intentamos el método antiguo (por seguridad)
        elif self.master_window and hasattr(self.master_window, 'deiconify'):
            self.master_window.deiconify()