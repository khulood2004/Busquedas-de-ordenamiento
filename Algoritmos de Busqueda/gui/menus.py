import tkinter as tk
from tkinter import messagebox

class MainSelectionScreen(tk.Toplevel):
    def __init__(self, master, on_sorting_callback, on_divide_callback, on_back_callback):
        super().__init__(master)
        self.on_sorting = on_sorting_callback
        self.on_divide = on_divide_callback

        self.on_back = on_back_callback # Callback para volver
        
        self.title("Selección de Categoría")
        self.geometry("600x450") # Un poco más alto para el botón volver
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)
        self._center()
        self._create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 450) // 2
        self.geometry(f"600x450+{x}+{y}")

    def _create_widgets(self):
        tk.Label(self, text="Seleccione una Categoría", font=("Helvetica", 16, "bold"), bg="#f6f1e7").pack(pady=30)

        # Opciones Principales
        tk.Button(
            self, text="Algoritmos de Busqueda\n(Secuencial, Binaria)", 
            font=("Helvetica", 11), bg="#e4efd9", width=35, height=3,
            command=self._go_sorting
        ).pack(pady=10)

        tk.Button(
            self, text="Algoritmos Divide y Vencerás\n(Karatsuba, Strassen...)", 
            font=("Helvetica", 11), bg="#e4efd9", width=35, height=3,
            command=self._go_divide
        ).pack(pady=10)

        # Botón Volver
        tk.Frame(self, bg="#f6f1e7").pack(pady=10) # Espaciador
        tk.Button(
            self, text="⬅ Volver al Inicio", 
            bg="#d9534f", fg="white", font=("Helvetica", 10, "bold"),
            command=self._go_back
        ).pack(pady=10, ipadx=10)

    def _go_sorting(self):
        self.destroy()
        self.on_sorting()

    def _go_divide(self):
        self.destroy()
        self.on_divide()

    def _go_back(self):
        self.destroy()
        self.on_back()


class DivideMenuScreen(tk.Toplevel):
    def __init__(self, master, on_karatsuba_callback,on_strassen_callback,on_pi_callback,on_back_callback):
        super().__init__(master)
        self.on_karatsuba = on_karatsuba_callback
        self.on_strassen = on_strassen_callback
        self.on_pi = on_pi_callback
        self.on_back = on_back_callback
        
        self.title("Algoritmos de tipo Divide y Vencerás")
        self.geometry("500x450")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)
        self._center()
        self._create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 450) // 2
        self.geometry(f"500x450+{x}+{y}")

    def _create_widgets(self):
        tk.Label(self, text="Algoritmos de tipo Divide y Vencerás", font=("Helvetica", 14, "bold"), bg="#f6f1e7").pack(pady=30)

        # Opciones
        tk.Button(
            self, text="Multiplicación de Karatsuba", 
            font=("Helvetica", 10), bg="#e4efd9", width=30, height=2,
            command=self._go_karatsuba
        ).pack(pady=10)

        tk.Button(
            self, text="Matricial de Strassen", 
            font=("Helvetica", 10), bg="#e4efd9", width=30, height=2,
            command=self._go_strassen
        ).pack(pady=10)

        tk.Button(
            self, text="Generación de PI (10000 cifras)", 
            font=("Helvetica", 10), bg="#e4efd9", width=30, height=2,
            command=self._go_pi 
        ).pack(pady=10)

        # Botón Volver
        tk.Button(
            self, text="⬅ Volver", 
            bg="#d9534f", fg="white", font=("Helvetica", 10, "bold"),
            command=self._go_back
        ).pack(pady=20, ipadx=10)

    def _go_karatsuba(self):
        self.destroy()
        self.on_karatsuba()

    def _go_strassen(self):
        self.destroy()
        self.on_strassen()
    
    def _go_pi(self):
        self.destroy()
        self.on_pi()

    def _go_back(self):
        self.destroy()
        self.on_back()
        
    