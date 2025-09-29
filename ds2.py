import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import random
import csv
import os
import math

# Global step counters
insertionsteps = mergesteps = heapsteps = quicksteps = bubblesteps = 0

# Sorting algorithms (as before, truncated for brevity)
def insertion_sort(arr, n):
    global insertionsteps
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            insertionsteps += 1  # Comparison
            arr[j + 1] = arr[j]
            insertionsteps += 1  # Movement
            j -= 1
        arr[j + 1] = key
        insertionsteps += 1  # Insertion

def merge_sort(arr, l, r):
    global mergesteps
    if l < r:
        m = l + (r - l) // 2
        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)

def merge(arr, l, m, r):
    global mergesteps
    n1 = m - l + 1
    n2 = r - m
    L = arr[l:l + n1]
    R = arr[m + 1:m + 1 + n2]

    i = j = 0
    k = l
    while i < n1 and j < n2:
        mergesteps += 1  # Comparison
        if L[i] <= R[j]:
            arr[k] = L[i]
            mergesteps += 1  # Movement
            i += 1
        else:
            arr[k] = R[j]
            mergesteps += 1  # Movement
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        mergesteps += 1  # Movement
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        mergesteps += 1  # Movement
        j += 1
        k += 1

def heap_sort(arr, n):
    global heapsteps
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapsteps += 1  # Swap
        heapify(arr, i, 0)

def heapify(arr, n, i):
    global heapsteps
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        heapsteps += 1  # Comparison
        largest = l
    if r < n and arr[r] > arr[largest]:
        heapsteps += 1  # Comparison
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapsteps += 1  # Swap
        heapify(arr, n, largest)

def quick_sort(arr, low, high):
    global quicksteps
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    global quicksteps
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        quicksteps += 1  # Comparison
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            quicksteps += 1  # Swap
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    quicksteps += 1  # Swap
    return i + 1
    
def bubble_sort(arr, n):
    global bubblesteps
    for i in range(n - 1):
        for j in range(n - i - 1):
            bubblesteps += 1  # Comparison
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                bubblesteps += 1  # Swap

def generate_test_data(size, case="average"):
    """Generate a list of integers for testing based on the selected case."""
    if case == "best":
        return list(range(size))  # Best case: already sorted
    elif case == "worst":
        return list(range(size, 0, -1))  # Worst case: reverse sorted
    else:
        return [random.randint(1, 100) for _ in range(size)]  # Average case: random

def save_test_data(arr):
    """Save the generated test data to a CSV file."""
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if filepath:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Value"])
            for index, value in enumerate(arr):
                writer.writerow([index, value])
        messagebox.showinfo("Success", f"Test data saved to {filepath}")

def get_asymptotic_complexity(algorithm_name, sizes, case):
    if algorithm_name in ["Insertion Sort", "Bubble Sort"]:
        if case == "best":
            return [n for n in sizes]  # O(n)
        else:  # Average and worst
            return [n * n for n in sizes]  # O(n^2)
    elif algorithm_name in ["Merge Sort", "Heap Sort"]:
        return [n * math.log(n, 2) for n in sizes]  # O(n log n) for all cases
    elif algorithm_name == "Quick Sort":
        if case == "best" or case == "average":
            return [n * math.log(n, 2) for n in sizes]  # O(n log n)
        else:  # Worst case
            return [n * n for n in sizes]  # O(n^2)
    return []

def compare_with_asymptotic_gui(algorithm_name, arr, case="average"):
    """Compare the selected algorithm with its asymptotic complexity."""
    global insertionsteps, mergesteps, heapsteps, quicksteps, bubblesteps
    n = len(arr)
    sizes = range(10, n + 1, 10)
    algorithm_steps = []

    for size in sizes:
        sub_arr = arr[:size]
        insertionsteps = mergesteps = heapsteps = quicksteps = bubblesteps = 0

        if algorithm_name == "Insertion Sort":
            insertion_sort(sub_arr, size)
            algorithm_steps.append(insertionsteps)
        elif algorithm_name == "Merge Sort":
            merge_sort(sub_arr, 0, size - 1)
            algorithm_steps.append(mergesteps)
        elif algorithm_name == "Heap Sort":
            heap_sort(sub_arr, size)
            algorithm_steps.append(heapsteps)
        elif algorithm_name == "Quick Sort":
            quick_sort(sub_arr, 0, size - 1)
            algorithm_steps.append(quicksteps)
        elif algorithm_name == "Bubble Sort":
            bubble_sort(sub_arr, size)
            algorithm_steps.append(bubblesteps)

    plt.figure(figsize=(10, 5))
    plt.plot(sizes, algorithm_steps, label=f"{algorithm_name} Steps", color="blue", marker="o")

    asymptotic = get_asymptotic_complexity(algorithm_name, sizes, case)
    plt.plot(sizes, asymptotic, label=f"Asymptotic ({case.capitalize()} Case)", color="red", linestyle="--")
    
    plt.xlabel("Array Size")
    plt.ylabel("Number of Steps")
    plt.title(f"{algorithm_name} vs Asymptotic Complexity ({case.capitalize()} Case)")
    plt.legend()
    plt.show()

def compare_multiple_algorithms_gui(selected_algorithms, arr):
    """Compare multiple selected algorithms."""
    global insertionsteps, mergesteps, heapsteps, quicksteps, bubblesteps
    n = len(arr)
    sizes = range(10, n + 1, 10)
    algorithm_steps_dict = {alg: [] for alg in selected_algorithms}

    for size in sizes:
        for algorithm in selected_algorithms:
            sub_arr = arr[:size].copy()
            insertionsteps = mergesteps = heapsteps = quicksteps = bubblesteps = 0

            if algorithm == "Insertion Sort":
                insertion_sort(sub_arr, size)
                algorithm_steps_dict[algorithm].append(insertionsteps)
            elif algorithm == "Merge Sort":
                merge_sort(sub_arr, 0, size - 1)
                algorithm_steps_dict[algorithm].append(mergesteps)
            elif algorithm == "Heap Sort":
                heap_sort(sub_arr, size)
                algorithm_steps_dict[algorithm].append(heapsteps)
            elif algorithm == "Quick Sort":
                quick_sort(sub_arr, 0, size - 1)
                algorithm_steps_dict[algorithm].append(quicksteps)
            elif algorithm == "Bubble Sort":
                bubble_sort(sub_arr, size)
                algorithm_steps_dict[algorithm].append(bubblesteps)

    plt.figure(figsize=(12, 6))
    for algorithm, steps in algorithm_steps_dict.items():
        plt.plot(sizes, steps, label=f"{algorithm} Steps", marker="o")

    plt.xlabel("Array Size")
    plt.ylabel("Number of Steps")
    plt.title("Comparison of Sorting Algorithms")
    plt.legend()
    plt.show()

def save_graph():
    """Save the current graph to a file."""
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filepath:
        plt.savefig(filepath)
        messagebox.showinfo("Success", f"Graph saved to {filepath}")

def export_steps_to_csv(steps, filename="algorithm_steps.csv"):
    """Export the steps to a CSV file."""
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if filepath:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Steps"])
            for algorithm, step_list in steps.items():
                for step in step_list:
                    writer.writerow([algorithm, step])
        messagebox.showinfo("Success", f"Steps exported to {filepath}")

def setup_gui():
    """Set up the GUI."""
    root = tk.Tk()
    root.title("Sorting Algorithm Visualizer")
    root.geometry("600x700")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 12), padding=6)
    style.configure("TLabel", font=("Helvetica", 12), padding=6)
    style.configure("TNotebook", tabposition='n')
    style.configure("TCombobox", padding=6)
    style.configure("TEntry", padding=6)

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    # Single Algorithm Tab
    single_tab = ttk.Frame(notebook)
    notebook.add(single_tab, text="Single Algorithm")

    single_algo_frame = ttk.Frame(single_tab, padding="10")
    single_algo_frame.pack(fill="both", expand=True)

    single_algo_label = ttk.Label(single_algo_frame, text="Select Algorithm:")
    single_algo_label.grid(row=0, column=0, pady=5, sticky="w")

    single_algo_combobox = ttk.Combobox(single_algo_frame, values=["Insertion Sort", "Merge Sort", "Heap Sort", "Quick Sort", "Bubble Sort"], state="readonly")
    single_algo_combobox.grid(row=0, column=1, pady=5, sticky="ew")
    single_algo_combobox.current(0)

    single_algo_size_label = ttk.Label(single_algo_frame, text="Enter Array Size:")
    single_algo_size_label.grid(row=1, column=0, pady=5, sticky="w")

    single_algo_size_entry = ttk.Entry(single_algo_frame)
    single_algo_size_entry.grid(row=1, column=1, pady=5, sticky="ew")

    single_algo_case_label = ttk.Label(single_algo_frame, text="Select Case:")
    single_algo_case_label.grid(row=2, column=0, pady=5, sticky="w")

    single_algo_case_combobox = ttk.Combobox(single_algo_frame, values=["best", "average", "worst"], state="readonly")
    single_algo_case_combobox.grid(row=2, column=1, pady=5, sticky="ew")
    single_algo_case_combobox.current(1)  # Default to "average"

    def on_single_compare():
        try:
            algo = single_algo_combobox.get()
            size = int(single_algo_size_entry.get())
            case = single_algo_case_combobox.get()
            if size <= 0:
                raise ValueError("Size must be a positive integer.")
            arr = generate_test_data(size, case)
            compare_with_asymptotic_gui(algo, arr, case)  # Pass the case parameter
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    single_compare_button = ttk.Button(single_algo_frame, text="Compare", command=on_single_compare)
    single_compare_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Multi-Algorithm Tab
    multi_tab = ttk.Frame(notebook)
    notebook.add(multi_tab, text="Multiple Algorithms")

    multi_algo_frame = ttk.Frame(multi_tab, padding="10")
    multi_algo_frame.pack(fill="both", expand=True)

    multi_algo_label = ttk.Label(multi_algo_frame, text="Select Algorithms:")
    multi_algo_label.grid(row=0, column=0, pady=5, sticky="w")

    multi_algo_listbox = tk.Listbox(multi_algo_frame, selectmode=tk.MULTIPLE, height=5)
    for alg in ["Insertion Sort", "Merge Sort", "Heap Sort", "Quick Sort", "Bubble Sort"]:
        multi_algo_listbox.insert(tk.END, alg)
    multi_algo_listbox.grid(row=0, column=1, pady=5, sticky="ew")

    multi_algo_size_label = ttk.Label(multi_algo_frame, text="Enter Array Size:")
    multi_algo_size_label.grid(row=1, column=0, pady=5, sticky="w")

    multi_algo_size_entry = ttk.Entry(multi_algo_frame)
    multi_algo_size_entry.grid(row=1, column=1, pady=5, sticky="ew")

    multi_algo_case_label = ttk.Label(multi_algo_frame, text="Select Case:")
    multi_algo_case_label.grid(row=2, column=0, pady=5, sticky="w")

    multi_algo_case_combobox = ttk.Combobox(multi_algo_frame, values=["best", "average", "worst"], state="readonly")
    multi_algo_case_combobox.grid(row=2, column=1, pady=5, sticky="ew")
    multi_algo_case_combobox.current(1)  # Default to "average"

    def on_multi_compare():
        try:
            selected_indices = multi_algo_listbox.curselection()
            selected_algorithms = [multi_algo_listbox.get(i) for i in selected_indices]
            if len(selected_algorithms) < 2:
                raise ValueError("Select at least two algorithms.")
            size = int(multi_algo_size_entry.get())
            case = multi_algo_case_combobox.get()
            if size <= 0:
                raise ValueError("Size must be a positive integer.")
            arr = generate_test_data(size, case)
            compare_multiple_algorithms_gui(selected_algorithms, arr)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    multi_compare_button = ttk.Button(multi_algo_frame, text="Compare", command=on_multi_compare)
    multi_compare_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Save and Export Buttons
    save_button = ttk.Button(root, text="Save Graph", command=save_graph)
    save_button.pack(pady=5)

    # Save Test Data Button
    def on_save_test_data():
        try:
            size = int(single_algo_size_entry.get())
            case = single_algo_case_combobox.get()
            if size <= 0:
                raise ValueError("Size must be a positive integer.")
            arr = generate_test_data(size, case)
            save_test_data(arr)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    save_test_data_button = ttk.Button(root, text="Save Test Data", command=on_save_test_data)
    save_test_data_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()