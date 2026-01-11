import tkinter as tk
from tkinter import ttk, messagebox
import random

# Importaciones matplotlib
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from algoritmos.karatsuba import karatsuba_recursive, karatsuba_iterative

class KaratsubaInputScreen(tk.Toplevel):
    def __init__(self, master, data_manager, on_back_callback):
        super().__init__(master)
        self.dm = data_manager
        self.on_back = on_back_callback # Callback para volver
        
        self.title("Configuración Karatsuba")
        self.geometry("600x500")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)
        
        self.input_mode = tk.StringVar(value="manual")
        
        self._center()
        self._create_widgets()
        self._toggle_inputs()

    def _center(self):
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 500) // 2
        self.geometry(f"600x500+{x}+{y}")

    def _create_widgets(self):
        tk.Label(self, text="Entrada de Datos para Karatsuba", font=("Helvetica", 14, "bold"), bg="#f6f1e7").pack(pady=20)

        # Modos
        mode_frame = tk.Frame(self, bg="#f6f1e7")
        mode_frame.pack(pady=10)
        tk.Radiobutton(mode_frame, text="Ingreso Manual", variable=self.input_mode, value="manual", bg="#f6f1e7", command=self._toggle_inputs).pack(side="left", padx=20)
        tk.Radiobutton(mode_frame, text="Generación Aleatoria", variable=self.input_mode, value="random", bg="#f6f1e7", command=self._toggle_inputs).pack(side="left", padx=20)

        # Manual Frame
        self.manual_frame = tk.LabelFrame(self, text="Datos Manuales", bg="#e4efd9", fg="#2e3d2f")
        self.manual_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(self.manual_frame, text="Número 1:", bg="#e4efd9").grid(row=0, column=0, padx=10, pady=10)
        self.entry_num1 = tk.Entry(self.manual_frame, width=30)
        self.entry_num1.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.manual_frame, text="Número 2:", bg="#e4efd9").grid(row=1, column=0, padx=10, pady=10)
        self.entry_num2 = tk.Entry(self.manual_frame, width=30)
        self.entry_num2.grid(row=1, column=1, padx=10, pady=10)

        # Random Frame
        self.random_frame = tk.LabelFrame(self, text="Configuración Aleatoria", bg="#e4efd9", fg="#2e3d2f")
        self.random_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(self.random_frame, text="Cifras:", bg="#e4efd9").pack(side="left", padx=10, pady=20)
        self.entry_digits = tk.Entry(self.random_frame, width=10)
        self.entry_digits.pack(side="left", padx=10)

        # Botones Acción
        btn_box = tk.Frame(self, bg="#f6f1e7")
        btn_box.pack(pady=20)

        tk.Button(btn_box, text="Cargar y Continuar", bg="#333", fg="white", font=("Helvetica", 10, "bold"),
                  command=self._on_continue).pack(side="left", padx=10, ipadx=10, ipady=5)
        
        tk.Button(btn_box, text="Volver", bg="#d9534f", fg="white", font=("Helvetica", 10, "bold"),
                  command=self._go_back).pack(side="left", padx=10, ipadx=10, ipady=5)

    def _toggle_inputs(self):
        mode = self.input_mode.get()
        if mode == "manual":
            for child in self.manual_frame.winfo_children(): child.configure(state="normal")
            for child in self.random_frame.winfo_children(): child.configure(state="disabled")
        else:
            for child in self.manual_frame.winfo_children(): child.configure(state="disabled")
            for child in self.random_frame.winfo_children(): child.configure(state="normal")

    def _on_continue(self):
        try:
            num1, num2 = self._get_numbers()
            # Pasamos la referencia de esta ventana para poder volver a ella
            KaratsubaExecutionScreen(self.master, num1, num2, on_back_callback=self._restore_self)
            self.withdraw() # Ocultamos esta ventana en lugar de destruirla
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")

    def _get_numbers(self):
        mode = self.input_mode.get()
        if mode == "manual":
            v1, v2 = self.entry_num1.get().strip(), self.entry_num2.get().strip()
            if not v1 or not v2: raise ValueError
            return int(v1), int(v2)
        else:
            d = int(self.entry_digits.get())
            if d <= 0: raise ValueError
            s, e = 10**(d-1), (10**d)-1
            return random.randint(s, e), random.randint(s, e)

    def _go_back(self):
        self.destroy()
        self.on_back()

    def _restore_self(self):
        self.deiconify() # Volver a mostrar esta ventana

class KaratsubaExecutionScreen(tk.Toplevel):
    def __init__(self, master, num1, num2, on_back_callback):
        super().__init__(master)
        self.num1 = num1
        self.num2 = num2
        self.on_back = on_back_callback
        
        self.result_rec = None
        self.time_rec = None
        self.result_iter = None
        self.time_iter = None
        
        self.title("Ejecución Karatsuba")
        self.geometry("900x750") 
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)
        self._center()
        self._create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 750) // 2
        self.geometry(f"900x750+{x}+{y}")

    def _create_widgets(self):
        # 1. Info Superior
        top_frame = tk.Frame(self, bg="#f6f1e7")
        top_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        n1s, n2s = str(self.num1), str(self.num2)
        dn1 = (n1s[:40] + '...') if len(n1s) > 40 else n1s
        dn2 = (n2s[:40] + '...') if len(n2s) > 40 else n2s

        tk.Label(top_frame, text=f"Número A: {dn1}", bg="#e4efd9", anchor="w").pack(fill="x", pady=2)
        tk.Label(top_frame, text=f"Número B: {dn2}", bg="#e4efd9", anchor="w").pack(fill="x", pady=2)

        # 2. Consola de Resultados
        result_frame = tk.LabelFrame(self, text="Consola de Resultados", bg="#f6f1e7")
        result_frame.pack(fill="x", padx=20, pady=5)
        self.output_text = tk.Text(result_frame, height=10, state="disabled", font=("Consolas", 9))
        self.output_text.pack(fill="both", padx=10, pady=5)

        # 3. Controles
        control_frame = tk.Frame(self, bg="#f6f1e7")
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Botones Ejecución
        btn_frame = tk.Frame(control_frame, bg="#f6f1e7")
        btn_frame.pack(side="left")
        tk.Button(btn_frame, text="Ejecutar Recursivo", bg="#ddd", command=self._run_recursive).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Ejecutar Iterativo", bg="#ddd", command=self._run_iterative).pack(fill="x", pady=2)
        
        # Tiempos Display
        time_frame = tk.Frame(control_frame, bg="#f6f1e7")
        time_frame.pack(side="left", padx=20)
        tk.Label(time_frame, text="T. Recursivo:", bg="#f6f1e7").grid(row=0, column=0)
        self.lbl_rec = tk.Label(time_frame, text="-- ms", bg="white", width=12, relief="sunken")
        self.lbl_rec.grid(row=0, column=1)
        tk.Label(time_frame, text="T. Iterativo:", bg="#f6f1e7").grid(row=1, column=0)
        self.lbl_iter = tk.Label(time_frame, text="-- ms", bg="white", width=12, relief="sunken")
        self.lbl_iter.grid(row=1, column=1)

        # Botón Gráfico y Volver
        right_frame = tk.Frame(control_frame, bg="#f6f1e7")
        right_frame.pack(side="right")
        
        self.btn_graph = tk.Button(right_frame, text="📉 Ver Gráfico", state="disabled", bg="#2e3d2f", fg="white", command=self._embed_graph)
        self.btn_graph.pack(side="top", fill="x", pady=2)
        
        tk.Button(right_frame, text="Volver", bg="#d9534f", fg="white", command=self._go_back).pack(side="top", fill="x", pady=2)

        # 4. Gráfico Frame
        self.graph_frame = tk.LabelFrame(self, text="Comparativa Visual", bg="#f6f1e7")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.lbl_placeholder = tk.Label(self.graph_frame, text="Ejecute ambos algoritmos para ver el gráfico.", bg="#f6f1e7", fg="gray")
        self.lbl_placeholder.pack(expand=True)

    def _log(self, msg):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")

    def _run_recursive(self):
        self._log(">>> Calculando Recursivo...")
        self.update()
        try:
            res, ms = karatsuba_recursive(self.num1, self.num2)
            self.result_rec = res
            self.time_rec = ms
            self.lbl_rec.config(text=f"{ms:.4f} ms")
            
            # MOSTRAR RESULTADO COMPLETO
            self._log(f"   [ÉXITO] Tiempo: {ms:.4f} ms")
            self._log(f"   RESULTADO: {res}")
            self._log("-" * 40)
            
            self._check_graph_enable()
        except RecursionError:
            self._log("   [ERROR] Stack Overflow.")
            self.time_rec = -1

    def _run_iterative(self):
        self._log(">>> Calculando Iterativo...")
        self.update()
        try:
            res, ms = karatsuba_iterative(self.num1, self.num2)
            self.result_iter = res
            self.time_iter = ms
            self.lbl_iter.config(text=f"{ms:.4f} ms")
            
            # MOSTRAR RESULTADO COMPLETO
            self._log(f"   [ÉXITO] Tiempo: {ms:.4f} ms")
            self._log(f"   RESULTADO: {res}")
            self._log("-" * 40)
            
            self._check_graph_enable()
        except Exception as e:
            self._log(f"   [ERROR] {str(e)}")

    def _check_graph_enable(self):
        if self.time_rec is not None and self.time_iter is not None and self.time_rec != -1:
            self.btn_graph.config(state="normal")

    def _embed_graph(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Matplotlib no instalado.")
            return
        
        for w in self.graph_frame.winfo_children(): w.destroy()
        
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor('#f6f1e7')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#f6f1e7')
        
        bars = ax.bar(['Recursivo', 'Iterativo'], [self.time_rec, self.time_iter], color=['#ff9999', '#66b3ff'], width=0.5)
        ax.set_title('Tiempo de Ejecución (ms)')
        
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2., h, f'{h:.4f}', ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _go_back(self):
        self.destroy()
        self.on_back()