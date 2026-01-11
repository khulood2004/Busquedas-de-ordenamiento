import tkinter as tk


class WelcomeScreen(tk.Toplevel):
    def __init__(self, master, next_callback):
        super().__init__(master)

        self.next_callback = next_callback
        self.title("Bienvenido")
        self.geometry("500x300")
        self.configure(bg="#f6f1e7")
        self.resizable(False, False)

        self._center()
        self.create_widgets()

    def _center(self):
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 300) // 2
        self.geometry(f"500x300+{x}+{y}")

    def create_widgets(self):
        tk.Label(
            self,
            text="Algoritmos de ordenamiento",
            font=("Helvetica", 18, "bold"),
            bg="#f6f1e7"
        ).pack(pady=40)

        tk.Label(
            self,
            text="Grupo 6",
            font=("Helvetica", 11),
            bg="#f6f1e7"
        ).pack(pady=10)

        tk.Button(
            self,
            text="Iniciar",
            font=("Helvetica", 12, "bold"),
            width=15,
            command=self._next
        ).pack(pady=30)

    def _next(self):
        self.destroy()
        self.next_callback()
