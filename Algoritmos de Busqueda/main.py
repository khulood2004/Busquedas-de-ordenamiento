import tkinter as tk
# Importamos todas las pantallas
from gui.Strassen import StrassenApp
from gui.welcome import WelcomeScreen
from gui.input import InputOptionsScreen
from gui.menus import MainSelectionScreen, DivideMenuScreen
from gui.karatsuba_screens import KaratsubaInputScreen
from gui.search_algorithms import SearchAlgorithmScreen
from gui.order_choice import OrderChoiceScreen
from algoritmos.data_manager import DataManager
import algoritmos.sorts as sorts

class AppController:
    def __init__(self, master):
        self.master = master
        self.dm = DataManager()
        self.master.withdraw()
        self.show_welcome_screen()

    # --- 1. BIENVENIDA ---
    def show_welcome_screen(self):
        WelcomeScreen(
            self.master,
            next_callback=self.show_main_selection
        )

    # --- 2. SELECCIÓN PRINCIPAL ---
    def show_main_selection(self):
        MainSelectionScreen(
            self.master,
            on_sorting_callback=self.show_sorting_input,  # Rama Original
            on_divide_callback=self.show_divide_menu,     # Rama Nueva
            on_back_callback=self.show_welcome_screen
        )

    # ================= RAMA A: ORIGINAL (Búsqueda y Ordenamiento) =================
    
    # Paso A1: Ingreso de Datos
    def show_sorting_input(self):
        InputOptionsScreen(
            self.master,
            data_manager=self.dm,
            next_callback=self.show_order_choice, # Vamos a la elección de orden
            on_back_callback=self.show_main_selection
        )

    # Paso A2: ¿Ordenar o Desordenar? (RESTAURADO)
    def show_order_choice(self):
        OrderChoiceScreen(
            self.master,
            data_manager=self.dm,
            next_callback=self.show_original_search_flow, # Siguiente paso: lógica de ordenamiento
            on_back_callback=self.show_sorting_input
        )

    # Paso A3: Lógica Condicional + Interfaz Original
    def show_original_search_flow(self):
        # Verificamos qué eligió el usuario en el DataManager
        if self.dm.order_mode == "ordered":
            # Si quiere ordenados, aplicamos Quicksort interno
            data = self.dm.get_data_copy()
            try:
                sorted_data, _ = sorts.quicksort_recursive(data)
                # Actualizamos los datos en el gestor
                sorted_str = ",".join(map(str, sorted_data))
                self.dm.set_data_manual(sorted_str)
            except RecursionError:
                print("Advertencia: Falló el ordenamiento por exceso de recursión.")
        
        # Si eligió 'unordered', no hacemos nada y pasamos los datos tal cual.

        # Abrimos la ventana final restaurada
        SearchAlgorithmScreen(
            self.master,
            data_manager=self.dm,
            on_back_callback=self.show_order_choice
        )

    # ================= RAMA B: DIVIDE Y VENCERÁS (KARATSUBA) =================
    
    def show_divide_menu(self):
        DivideMenuScreen(
            self.master,
            on_karatsuba_callback=self.show_karatsuba_input,
            on_strassen_callback=self.show_strassen,
            on_back_callback=self.show_main_selection
        )

    def show_karatsuba_input(self):
        KaratsubaInputScreen(
            self.master,
            data_manager=self.dm,
            on_back_callback=self.show_divide_menu
        )
    def show_strassen(self):
        StrassenApp(
            self.master,
            on_back_callback=self.show_divide_menu
    )

if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()