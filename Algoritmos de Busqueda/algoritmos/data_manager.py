import random
from typing import List


class DataManager:
    """
    Administra datos y selecciones del usuario.
    No contiene algoritmos.
    """

    def __init__(self):
        self._base_data: List[int] = []
        self.order_mode = "unordered"
        self.selected_algorithm = None

    @property
    def base_data(self) -> List[int]:
        return self._base_data

    def get_data_copy(self) -> List[int]:
        return list(self._base_data)

    def clear_data(self):
        self._base_data = []

    def set_data_manual(self, input_string: str):
        try:
            data_list = [
                int(item.strip())
                for item in input_string.split(',')
                if item.strip()
            ]
            if not data_list:
                raise ValueError
            self._base_data = data_list
        except ValueError:
            raise ValueError(
                "Ingrese solo números enteros separados por comas."
            )

    def set_data_random(self, count: int):
        if count <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        self._base_data = [
            random.randint(1, 1_000_000)
            for _ in range(count)
        ]

    def set_order_mode(self, mode: str):
        self.order_mode = mode

    def set_selected_algorithm(self, algorithm_name: str):
        self.selected_algorithm = algorithm_name


