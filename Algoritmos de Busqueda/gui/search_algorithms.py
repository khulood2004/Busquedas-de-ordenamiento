import tkinter as tk
from tkinter import ttk, messagebox
import time

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from algoritmos.data_manager import DataManager
from algoritmos import searches


# ==========================================================
# POPUP: Selección Iterativo / Recursivo (solo para modo ordenado)
# ==========================================================
class MethodChoiceDialog(tk.Toplevel):
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
            text="Iterativo",
            command=lambda: self._choose("iterative")
        ).pack(side="left", padx=10)

        ttk.Button(
            btn_frame,
            text="Recursivo",
            command=lambda: self._choose("recursive")
        ).pack(side="left", padx=10)

    def _choose(self, mode):
        self.destroy()
        self.on_choose(mode)


# ==========================================================
# PANTALLA PRINCIPAL
# ==========================================================
class SearchAlgorithmScreen(tk.Toplevel):
    def __init__(self, master, data_manager: DataManager, on_back_callback=None):
        super().__init__(master)

        self.dm = data_manager
        self.on_back = on_back_callback

        # tiempos para modo ordenado (lineal vs binaria)
        self.linear_time = None
        self.binary_time = None

        # tiempos para modo desordenado (lineal iterativa vs recursiva)
        self.linear_iter_time = None
        self.linear_rec_time = None

        self.title("Comparación de Algoritmos de Búsqueda")
        self.geometry("900x600")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self._center()

        self.main_container = tk.Frame(self, bg="#f6f1e7")
        self.main_container.pack(fill="both", expand=True)

        # MODO: ordenado => comparar lineal vs binaria
        # desordenado => comparar lineal iterativa vs recursiva
        self.is_ordered = (self.dm.order_mode == "ordered")

        self._build_ui()
        self._refresh_data_view()

    def _center(self):
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"900x600+{x}+{y}")

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------
    def _build_ui(self):
        title = (
            "COMPARACIÓN: BÚSQUEDA LINEAL vs BINARIA"
            if self.is_ordered
            else "COMPARACIÓN: BÚSQUEDA LINEAL (ITERATIVA vs RECURSIVA)"
        )

        tk.Label(
            self.main_container,
            text=title,
            font=("Helvetica", 16, "bold"),
            bg="#f6f1e7"
        ).pack(pady=10)

        # ---------- DATOS ----------
        data_frame = tk.LabelFrame(
            self.main_container,
            text="Datos cargados / generados",
            bg="#e4efd9",
            fg="#2e3d2f",
            font=("Helvetica", 9, "bold")
        )
        data_frame.pack(fill="x", padx=15, pady=5)

        self.data_text = tk.Text(data_frame, height=2, wrap="none")
        self.data_text.pack(fill="x", padx=5)

        h_scroll = tk.Scrollbar(
            data_frame,
            orient="horizontal",
            command=self.data_text.xview
        )
        h_scroll.pack(fill="x")

        self.data_text.configure(xscrollcommand=h_scroll.set, state="disabled")

        # ---------- ENTRADA ----------
        input_frame = tk.Frame(self.main_container, bg="#f6f1e7")
        input_frame.pack(pady=8)

        tk.Label(
            input_frame,
            text="Número a buscar:",
            bg="#f6f1e7",
            font=("Helvetica", 10, "bold")
        ).pack(side="left", padx=5)

        self.target_entry = tk.Entry(input_frame, width=20)
        self.target_entry.pack(side="left", padx=5)

        # ---------- COMPARACIÓN ----------
        compare_frame = tk.LabelFrame(
            self.main_container,
            text="Comparación",
            bg="#e4efd9",
            fg="#2e3d2f",
            font=("Helvetica", 10, "bold")
        )
        compare_frame.pack(fill="x", padx=15, pady=8)

        if self.is_ordered:
            ttk.Button(
                compare_frame,
                text="Ejecutar comparación (Lineal vs Binaria)",
                command=self._run_comparison_ordered
            ).pack(pady=8)

            self.result_label_1 = tk.Label(
                compare_frame,
                text="Tiempo Lineal: -- ms",
                bg="#e4efd9",
                font=("Helvetica", 10)
            )
            self.result_label_1.pack()

            self.result_label_2 = tk.Label(
                compare_frame,
                text="Tiempo Binaria: -- ms",
                bg="#e4efd9",
                font=("Helvetica", 10)
            )
            self.result_label_2.pack()

        else:
            ttk.Button(
                compare_frame,
                text="Ejecutar comparación (Lineal Iterativa vs Recursiva)",
                command=self._run_comparison_unordered
            ).pack(pady=8)

            self.result_label_1 = tk.Label(
                compare_frame,
                text="Tiempo Lineal Iterativa: -- ms",
                bg="#e4efd9",
                font=("Helvetica", 10)
            )
            self.result_label_1.pack()

            self.result_label_2 = tk.Label(
                compare_frame,
                text="Tiempo Lineal Recursiva: -- ms",
                bg="#e4efd9",
                font=("Helvetica", 10)
            )
            self.result_label_2.pack()

        # ---------- BOTONES (GRÁFICO + VOLVER) ----------
        action_frame = tk.Frame(self.main_container, bg="#f6f1e7")
        action_frame.pack(pady=6)

        self.graph_btn = ttk.Button(
            action_frame,
            text="📊 Generar gráfico comparativo",
            command=self._generate_graph,
            state="disabled"
        )
        self.graph_btn.pack(side="left", padx=8)

        ttk.Button(
            action_frame,
            text="⬅ Volver",
            command=self._go_back
        ).pack(side="left", padx=8)

        # ---------- ÁREA GRÁFICO ----------
        self.graph_placeholder = tk.Frame(
            self.main_container,
            bg="#ffffff",
            relief="solid",
            bd=1
        )
        self.graph_placeholder.pack(fill="both", expand=True, padx=15, pady=6)

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------
    def _refresh_data_view(self):
        data = self.dm.get_data_copy()
        txt = ", ".join(map(str, data)) if data else "(Sin datos)"
        self.data_text.config(state="normal")
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, txt)
        self.data_text.config(state="disabled")

    def _get_target(self):
        try:
            return int(self.target_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero a buscar.")
            return None

    # ------------------------------------------------------
    # EJECUCIÓN - MODO ORDENADO (lineal vs binaria + popup)
    # ------------------------------------------------------
    def _run_comparison_ordered(self):
        target = self._get_target()
        if target is None:
            return

        # ordenado => binaria válida
        MethodChoiceDialog(
            self,
            on_choose=lambda mode: self._execute_ordered_both(mode, target)
        )

    def _execute_ordered_both(self, mode, target):
        data = self.dm.get_data_copy()

        # ---- LINEAL ----
        start = time.perf_counter()
        if mode == "iterative":
            searches.linear_search_iterative(data, target)
        else:
            searches.linear_search_recursive(data, target)
        end = time.perf_counter()
        self.linear_time = (end - start) * 1000
        self.result_label_1.config(text=f"Tiempo Lineal: {self.linear_time:.4f} ms")

        # ---- BINARIA ----
        start = time.perf_counter()
        if mode == "iterative":
            searches.binary_search_iterative(data, target)
        else:
            searches.binary_search_recursive(data, target)
        end = time.perf_counter()
        self.binary_time = (end - start) * 1000
        self.result_label_2.config(text=f"Tiempo Binaria: {self.binary_time:.4f} ms")

        self.graph_btn.config(state="normal")

    # ------------------------------------------------------
    # EJECUCIÓN - MODO DESORDENADO (lineal iterativa vs recursiva)
    # ------------------------------------------------------
    def _run_comparison_unordered(self):
        target = self._get_target()
        if target is None:
            return

        data = self.dm.get_data_copy()

        # ---- LINEAL ITERATIVA ----
        start = time.perf_counter()
        searches.linear_search_iterative(data, target)
        end = time.perf_counter()
        self.linear_iter_time = (end - start) * 1000
        self.result_label_1.config(
            text=f"Tiempo Lineal Iterativa: {self.linear_iter_time:.4f} ms"
        )

        # ---- LINEAL RECURSIVA ----
        start = time.perf_counter()
        searches.linear_search_recursive(data, target)
        end = time.perf_counter()
        self.linear_rec_time = (end - start) * 1000
        self.result_label_2.config(
            text=f"Tiempo Lineal Recursiva: {self.linear_rec_time:.4f} ms"
        )

        self.graph_btn.config(state="normal")

    # ------------------------------------------------------
    # GRÁFICO
    # ------------------------------------------------------
    def _generate_graph(self):
        for widget in self.graph_placeholder.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        if self.is_ordered:
            if self.linear_time is None or self.binary_time is None:
                messagebox.showwarning("Falta ejecutar", "Ejecute la comparación antes de graficar.")
                return

            labels = ["Búsqueda Lineal", "Búsqueda Binaria"]
            values = [self.linear_time, self.binary_time]
            title = "Comparación: Lineal vs Binaria"

        else:
            if self.linear_iter_time is None or self.linear_rec_time is None:
                messagebox.showwarning("Falta ejecutar", "Ejecute la comparación antes de graficar.")
                return

            labels = ["Lineal Iterativa", "Lineal Recursiva"]
            values = [self.linear_iter_time, self.linear_rec_time]
            title = "Comparación: Lineal Iterativa vs Recursiva"

        ax.bar(labels, values)
        ax.set_ylabel("Tiempo de ejecución (ms)")
        ax.set_title(title)
        ax.grid(axis="y")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_placeholder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.graph_placeholder)
        toolbar.update()
        toolbar.pan()

    # ------------------------------------------------------
    def _go_back(self):
        self.destroy()
        if self.on_back:
            self.on_back()
