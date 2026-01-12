import tkinter as tk
from tkinter import ttk, messagebox
from algoritmos.pi_algos import PiAlgorithms

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ===============================
# PANTALLA DE CONFIGURACIÓN
# ===============================
class PiInputScreen(tk.Toplevel):
    def __init__(self, master, on_back_callback):
        super().__init__(master)
        self.on_back = on_back_callback
        self.title("Configuración Pi")
        self.geometry("600x400")
        self.configure(bg="#f6f1e7")
        self._center()
        self._create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"600x400+{x}+{y}")

    def _create_widgets(self):
        tk.Label(self, text="Generación de PI (DV)", font=("Helvetica", 14, "bold"),
                 bg="#f6f1e7").pack(pady=20)

        frame = tk.LabelFrame(self, text="Parámetros", bg="#e4efd9",
                              padx=20, pady=20)
        frame.pack(padx=50, fill="x")

        tk.Label(frame, text="Número de decimales:", bg="#e4efd9").pack(side="left")
        self.entry_digits = tk.Entry(frame, width=15)
        self.entry_digits.insert(0, "10000")
        self.entry_digits.pack(side="left", padx=10)

        btn_box = tk.Frame(self, bg="#f6f1e7")
        btn_box.pack(pady=30)

        tk.Button(btn_box, text="Cargar y Continuar",
                  bg="#333", fg="white",
                  command=self._on_continue).pack(side="left", padx=10)

        tk.Button(btn_box, text="Volver",
                  bg="#d9534f", fg="white",
                  command=self._go_back).pack(side="left", padx=10)

    def _on_continue(self):
        try:
            d = int(self.entry_digits.get())
            if d <= 0:
                raise ValueError
            PiExecutionScreen(self.master, d, self.deiconify)
            self.withdraw()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")

    def _go_back(self):
        self.destroy()
        self.on_back()


# ===============================
# PANTALLA DE EJECUCIÓN
# ===============================
class PiExecutionScreen(tk.Toplevel):
    def __init__(self, master, digits, on_back_callback):
        super().__init__(master)
        self.digits = digits
        self.on_back = on_back_callback

        self.time_iter = 0.0
        self.time_rec = 0.0

        self.title("Ejecución PI")
        self.geometry("800x600")
        self.configure(bg="#f6f1e7")
        self._center()
        self._create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"800x600+{x}+{y}")

    def _create_widgets(self):
        # ===== CONSOLA =====
        self.output_text = tk.Text(
            self,
            height=4,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Consolas", 10)
        )
        self.output_text.pack(fill="x", padx=20, pady=10)

        # Líneas fijas
        self.output_text.insert(tk.END, "Iterativo: pendiente...\n")
        self.output_text.insert(tk.END, "Recursivo: pendiente...\n")
        self.output_text.config(state="disabled")

        # ===== BOTONES =====
        btn_frame = tk.Frame(self, bg="#f6f1e7")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Ejecutar Iterativo", width=20,
                  command=self._run_iterative).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Ejecutar Recursivo (DV)", width=20,
                  command=self._run_recursive).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Volver", bg="#d9534f", fg="white",
                  command=self._go_back).pack(side="left", padx=10)

        # ===== GRÁFICA =====
        graph_frame = ttk.LabelFrame(self, text="Comparación de tiempos")
        graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.bars = self.ax.bar(["Iterativo", "Recursivo"], [0, 0])
        self.ax.set_ylabel("Milisegundos")
        self.ax.set_title("Comparación de algoritmos PI")

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===============================
    # ACTUALIZACIONES
    # ===============================
    def _update_console(self, line, text):
        self.output_text.config(state="normal")
        self.output_text.delete(f"{line}.0", f"{line}.end")
        self.output_text.insert(f"{line}.0", text)
        self.output_text.config(state="disabled")

    def _update_graph(self):
        self.bars[0].set_height(self.time_iter)
        self.bars[1].set_height(self.time_rec)

        max_t = max(self.time_iter, self.time_rec, 1)
        self.ax.set_ylim(0, max_t * 1.2)
        self.canvas.draw_idle()

    # ===============================
    # EJECUCIÓN
    # ===============================
    def _run_iterative(self):
        res, ms = PiAlgorithms.pi_iterative(self.digits)
        self.time_iter = ms

        self._update_console(
            1,
            f"Iterativo: {ms:.4f} ms | π ≈ {res[:80]}..."
        )
        self._update_graph()

    def _run_recursive(self):
        res, ms = PiAlgorithms.pi_recursive_dv(self.digits)
        self.time_rec = ms

        self._update_console(
            2,
            f"Recursivo: {ms:.4f} ms | π ≈ {res[:80]}..."
        )
        self._update_graph()

    def _go_back(self):
        self.destroy()
        self.on_back()
