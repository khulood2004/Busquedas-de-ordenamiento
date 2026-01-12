# algoritmos/searches.py
from typing import List

# -------- LINEAL --------
def linear_search_iterative(arr: List[int], target: int) -> int:
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1

def linear_search_recursive(arr: List[int], target: int, i: int = 0) -> int:
    if i >= len(arr):
        return -1
    if arr[i] == target:
        return i
    return linear_search_recursive(arr, target, i + 1)

# -------- BINARIA (requiere arr ORDENADO ascendente) --------
def binary_search_iterative(arr: List[int], target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search_recursive(arr: List[int], target: int, low: int = 0, high: int | None = None) -> int:
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    return binary_search_recursive(arr, target, low, mid - 1)
