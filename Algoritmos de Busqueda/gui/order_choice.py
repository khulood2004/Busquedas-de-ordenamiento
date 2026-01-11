import tkinter as tk
from algoritmos.data_manager import DataManager

class OrderChoiceScreen(tk.Toplevel):
    def __init__(self, master, data_manager: DataManager, next_callback, on_back_callback):
        super().__init__(master)

        self.dm = data_manager
        self.next_callback = next_callback
        self.on_back = on_back_callback

        self.title("Orden de Datos")
        self.geometry("500x350")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self._center()
        self.create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 350) // 2
        self.geometry(f"500x350+{x}+{y}")

    def create_widgets(self):
        tk.Label(
            self,
            text="Seleccione el estado de los datos",
            font=("Helvetica", 14, "bold"),
            bg="#f6f1e7"
        ).pack(pady=30)

        # Botón para ORDENAR (Activa el Quicksort interno en el siguiente paso)
        tk.Button(
            self,
            text="Datos Ordenados\n(Aplicar Quicksort)",
            width=25,
            bg="#e4efd9",
            command=lambda: self._select("ordered")
        ).pack(pady=10)

        # Botón para DESORDENADO (Mantiene los datos como están)
        tk.Button(
            self,
            text="Datos Desordenados\n(Mantener Original)",
            width=25,
            bg="#e4efd9",
            command=lambda: self._select("unordered")
        ).pack(pady=10)
        
        # Botón Volver
        tk.Button(
            self, 
            text="⬅ Volver", 
            bg="#d9534f", 
            fg="white", 
            command=self._go_back
        ).pack(pady=20)

    def _select(self, mode):
        # Guardamos la preferencia. Main.py leerá esto para decidir si ordena o no.
        self.dm.set_order_mode(mode)
        self.destroy()
        self.next_callback()

    def _go_back(self):
        self.destroy()
        self.on_back()