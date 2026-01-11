import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
import matplotlib.pyplot as plt

# ===============================
# STRASSEN RECURSIVO
# ===============================
def strassen_rec(A, B):
    n = A.shape[0]
    if n == 1:
        return A * B

    mid = n // 2
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    M1 = strassen_rec(A11 + A22, B11 + B22)
    M2 = strassen_rec(A21 + A22, B11)
    M3 = strassen_rec(A11, B12 - B22)
    M4 = strassen_rec(A22, B21 - B11)
    M5 = strassen_rec(A11 + A12, B22)
    M6 = strassen_rec(A21 - A11, B11 + B12)
    M7 = strassen_rec(A12 - A22, B21 + B22)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    return np.vstack((np.hstack((C11, C12)),
                      np.hstack((C21, C22))))


# ===============================
# STRASSEN ITERATIVO (SIMULADO)
# ===============================
def strassen_iter(A, B):
    stack = [(A, B, False)]
    results = []

    while stack:
        A, B, combine = stack.pop()
        n = A.shape[0]

        if n == 1:
            results.append(A * B)
            continue

        mid = n // 2
        A11, A12 = A[:mid, :mid], A[:mid, mid:]
        A21, A22 = A[mid:, :mid], A[mid:, mid:]
        B11, B12 = B[:mid, :mid], B[:mid, mid:]
        B21, B22 = B[mid:, :mid], B[mid:, mid:]

        if not combine:
            stack.append((A, B, True))
            stack.extend([
                (A12 - A22, B21 + B22, False),
                (A21 - A11, B11 + B12, False),
                (A11 + A12, B22, False),
                (A22, B21 - B11, False),
                (A11, B12 - B22, False),
                (A21 + A22, B11, False),
                (A11 + A22, B11 + B22, False)
            ])
        else:
            M1, M2, M3, M4, M5, M6, M7 = results[-7:]
            results = results[:-7]

            C11 = M1 + M4 - M5 + M7
            C12 = M3 + M5
            C21 = M2 + M4
            C22 = M1 - M2 + M3 + M6

            results.append(np.vstack((np.hstack((C11, C12)),
                                      np.hstack((C21, C22)))))
    return results[0]


# ===============================
# INTERFAZ GRÁFICA
# ===============================
class StrassenApp(tk.Toplevel):
    def __init__(self, master, on_back_callback):
        super().__init__(master)
        self.on_back = on_back_callback

        self.title("Algoritmo de Strassen")
        self.geometry("900x600")
        self.minsize(900, 600)
        self.resizable(False, False)

        self.mode = tk.StringVar(value="random")
        self.entries_A = []
        self.entries_B = []

        self.time_rec = 0
        self.time_iter = 0

        self.create_widgets()
        self.center_window()

    def center_window(self):
        self.update_idletasks()

        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")



    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(pady=10)

        ttk.Label(top, text="Tamaño (potencia de 2):").grid(row=0, column=0)
        self.size_entry = ttk.Entry(top, width=5)
        self.size_entry.insert(0, "2")
        self.size_entry.grid(row=0, column=1, padx=5)

        mode_frame = ttk.LabelFrame(self, text="Modo de matrices")
        mode_frame.pack(pady=5)

        ttk.Radiobutton(mode_frame, text="Aleatorias",
                        variable=self.mode, value="random").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="Manuales",
                        variable=self.mode, value="manual").grid(row=0, column=1, padx=10)

        ttk.Button(self, text="Generar matrices",
                   command=self.generate_inputs).pack(pady=10)

        self.matrix_frame = ttk.Frame(self)
        self.matrix_frame.pack()

        action = ttk.Frame(self)
        action.pack(pady=10)

        ttk.Button(action, text="Ejecutar Recursivo",
                   command=self.run_recursive).grid(row=0, column=0, padx=10)
        ttk.Button(action, text="Ejecutar Iterativo",
                   command=self.run_iterative).grid(row=0, column=1, padx=10)

        result = ttk.LabelFrame(self, text="Tiempos (ms)")
        result.pack(pady=10)

        ttk.Label(result, text="Recursivo:").grid(row=0, column=0)
        self.rec_label = ttk.Label(result, text="0.0")
        self.rec_label.grid(row=0, column=1)

        ttk.Label(result, text="Iterativo:").grid(row=1, column=0)
        self.iter_label = ttk.Label(result, text="0.0")
        self.iter_label.grid(row=1, column=1)

        ttk.Button(self, text="Mostrar gráfico",
                   command=self.plot).pack(pady=10)

        ttk.Button(self, text="⬅ Volver", command=self._go_back).pack()
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container)
        canvas.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        scroll_x = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        canvas.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.matrix_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.matrix_frame, anchor="nw")

        self.matrix_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

    # ===============================
    # MATRICES
    # ===============================
    def generate_inputs(self):
        n = int(self.size_entry.get())

        if not self.is_power_of_two(n):
            messagebox.showerror(
                "Tamaño inválido",
                "El tamaño debe ser una potencia de 2\n(Ej: 2, 4, 8, 16, 32...)"
            )
            return
    
        for w in self.matrix_frame.winfo_children():
            w.destroy()

        self.entries_A.clear()
        self.entries_B.clear()

        n = int(self.size_entry.get())

        frameA = ttk.LabelFrame(self.matrix_frame, text="Matriz A")
        frameB = ttk.LabelFrame(self.matrix_frame, text="Matriz B")
        frameA.grid(row=0, column=0, padx=30)
        frameB.grid(row=0, column=1, padx=30)

        for i in range(n):
            rowA, rowB = [], []
            for j in range(n):
                ea = ttk.Entry(frameA, width=4, justify="center")
                eb = ttk.Entry(frameB, width=4, justify="center")
                ea.grid(row=i, column=j, padx=2, pady=2)
                eb.grid(row=i, column=j, padx=2, pady=2)

                if self.mode.get() == "random":
                    ea.insert(0, np.random.randint(0, 10))
                    eb.insert(0, np.random.randint(0, 10))

                rowA.append(ea)
                rowB.append(eb)
            self.entries_A.append(rowA)
            self.entries_B.append(rowB)

    def is_power_of_two(self, n):
        return n > 0 and (n & (n - 1)) == 0
    
    def read_matrices(self):
        try:
            n = len(self.entries_A)
            A = np.zeros((n, n), dtype=int)
            B = np.zeros((n, n), dtype=int)

            for i in range(n):
                for j in range(n):
                    A[i, j] = int(self.entries_A[i][j].get())
                    B[i, j] = int(self.entries_B[i][j].get())
            return A, B
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return None, None

    # ===============================
    # EJECUCIÓN
    # ===============================
    def run_recursive(self):
        if not self.entries_A:
            messagebox.showwarning("Aviso", "Primero genera las matrices")
            return
        A, B = self.read_matrices()
        if A is None:
            return

        start = time.perf_counter()
        strassen_rec(A, B)
        self.time_rec = (time.perf_counter() - start) * 1000
        self.rec_label.config(text=f"{self.time_rec:.4f}")
    
    def run_iterative(self):
        if not self.entries_A:
            messagebox.showwarning("Aviso", "Primero genera las matrices")
            return
        A, B = self.read_matrices()
        if A is None:
            return

        start = time.perf_counter()
        strassen_iter(A, B)
        self.time_iter = (time.perf_counter() - start) * 1000
        self.iter_label.config(text=f"{self.time_iter:.4f}")

    def plot(self):
        if self.time_rec == 0 or self.time_iter == 0:
            messagebox.showwarning("Aviso", "Ejecuta ambos métodos primero")
            return

        plt.bar(["Recursivo", "Iterativo"],
                [self.time_rec, self.time_iter])
        plt.ylabel("Milisegundos")
        plt.title("Comparación Strassen")
        plt.show()

    def _go_back(self):
        self.destroy()
        self.on_back()

