import tkinter as tk
from tkinter import messagebox
from algoritmos.data_manager import DataManager

class InputOptionsScreen(tk.Toplevel):
    def __init__(self, master, data_manager: DataManager, next_callback, on_back_callback):
        super().__init__(master)

        self.dm = data_manager
        self.next_callback = next_callback
        self.on_back = on_back_callback
        
        # Variable para controlar el modo (Manual vs Aleatorio)
        self.input_mode = tk.StringVar(value="manual")

        self.title("Ingreso de Datos")
        self.geometry("600x500")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self._center()
        self.create_widgets()
        
        # Inicializar estado de los campos (uno activo, otro inactivo)
        self._toggle_inputs()

    def _center(self):
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 500) // 2
        self.geometry(f"600x500+{x}+{y}")

    def create_widgets(self):
        tk.Label(
            self,
            text="INGRESO DE DATOS",
            font=("Helvetica", 18, "bold"),
            bg="#f6f1e7"
        ).pack(pady=20)

        # --- SELECCIÓN DE MODO (Radiobuttons) ---
        mode_frame = tk.Frame(self, bg="#f6f1e7")
        mode_frame.pack(pady=10)
        
        # Botón redondo para Manual
        rb1 = tk.Radiobutton(
            mode_frame, 
            text="Ingreso Manual", 
            variable=self.input_mode, 
            value="manual", 
            bg="#f6f1e7", 
            command=self._toggle_inputs,
            font=("Helvetica", 10)
        )
        rb1.pack(side="left", padx=20)
        
        # Botón redondo para Aleatorio
        rb2 = tk.Radiobutton(
            mode_frame, 
            text="Generación Aleatoria", 
            variable=self.input_mode, 
            value="random", 
            bg="#f6f1e7", 
            command=self._toggle_inputs,
            font=("Helvetica", 10)
        )
        rb2.pack(side="left", padx=20)

        # --- ÁREA MANUAL ---
        self.manual_frame = tk.LabelFrame(
            self, 
            text="Datos Manuales", 
            bg="#e4efd9", 
            fg="#2e3d2f"
        )
        self.manual_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            self.manual_frame, 
            text="Ingrese números enteros separados por coma:", 
            bg="#e4efd9"
        ).pack(pady=(10, 5))
        
        self.manual_entry = tk.Entry(self.manual_frame, width=50)
        self.manual_entry.pack(pady=(0, 15), padx=10)

        # --- ÁREA ALEATORIA ---
        self.random_frame = tk.LabelFrame(
            self, 
            text="Configuración Aleatoria", 
            bg="#e4efd9", 
            fg="#2e3d2f"
        )
        self.random_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            self.random_frame, 
            text="Cantidad de números a generar:", 
            bg="#e4efd9"
        ).pack(side="left", padx=20, pady=20)
        
        self.random_entry = tk.Entry(self.random_frame, width=15)
        self.random_entry.pack(side="left", padx=10)

        # --- BOTONES DE ACCIÓN ---
        btn_frame = tk.Frame(self, bg="#f6f1e7")
        btn_frame.pack(pady=20)

        # Botón único para procesar según la selección
        tk.Button(
            btn_frame,
            text="Cargar Datos y Continuar",
            bg="#333",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self._process_data
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

        # Botón Volver
        tk.Button(
            btn_frame,
            text="⬅ Volver",
            bg="#d9534f",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self._go_back
        ).pack(side="left", padx=10, ipadx=10, ipady=5)

    def _toggle_inputs(self):
        """Habilita o deshabilita los campos según el radiobutton seleccionado"""
        mode = self.input_mode.get()
        
        if mode == "manual":
            # Habilitar manual
            for child in self.manual_frame.winfo_children():
                child.configure(state="normal")
            # Deshabilitar aleatorio
            for child in self.random_frame.winfo_children():
                child.configure(state="disabled")
        else:
            # Deshabilitar manual
            for child in self.manual_frame.winfo_children():
                child.configure(state="disabled")
            # Habilitar aleatorio
            for child in self.random_frame.winfo_children():
                child.configure(state="normal")

    def _process_data(self):
        """Lee los datos según el modo activo y avanza"""
        mode = self.input_mode.get()
        
        try:
            if mode == "manual":
                val = self.manual_entry.get()
                if not val.strip():
                    raise ValueError("El campo manual está vacío.")
                self.dm.set_data_manual(val)
                messagebox.showinfo("OK", "Datos manuales cargados correctamente")
                
            else: # Random
                val = self.random_entry.get()
                if not val.strip():
                    raise ValueError("Ingrese la cantidad de números.")
                count = int(val)
                self.dm.set_data_random(count)
                messagebox.showinfo("OK", f"Se generaron {count} números aleatorios correctamente")
            
            # Si todo sale bien, avanzamos
            self._next()
            
        except ValueError as e:
            # Captura errores de conversión o validación del DataManager
            messagebox.showerror("Error de Datos", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def _next(self):
        self.destroy()
        self.next_callback()

    def _go_back(self):
        self.destroy()
        self.on_back()