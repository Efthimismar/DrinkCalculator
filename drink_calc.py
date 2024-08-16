import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.stats import norm

def validate_input(input):
    try:
        value = int(input)
        if value < 0:
            raise ValueError
        return True
    except ValueError:
        return False

def calculate_drinks_for_party(n_guests, sample_data, preferences):
    sample_data = np.array(sample_data)
    sample_mean = np.mean(sample_data)
    sample_std = np.std(sample_data, ddof=1)
    z_score = norm.ppf(0.95)
    estimated_mean = n_guests * sample_mean
    estimated_std = np.sqrt(n_guests) * sample_std
    total_drinks_needed = estimated_mean + z_score * estimated_std
    total_drinks_rounded = int(np.ceil(total_drinks_needed))
    total_preferences = sum(preferences.values())
    drinks_per_type = {}
    for alcohol, count in preferences.items():
        proportion = count / total_preferences
        drinks_per_type[alcohol] = int(np.ceil(total_drinks_rounded * proportion))
    return drinks_per_type

def calculate_bottles_for_preferences(drinks_needed_dict, bottle_sizes, ml_per_drink=50):
    bottles_needed = {}
    for alcohol, drinks_needed in drinks_needed_dict.items():
        total_ml_needed = drinks_needed * ml_per_drink
        large_bottle_ml = bottle_sizes[alcohol]['large']
        small_bottle_ml = bottle_sizes[alcohol]['small']
        
        large_bottles_needed = total_ml_needed // large_bottle_ml
        remaining_ml = total_ml_needed % large_bottle_ml
        
        small_bottles_needed = 0
        if remaining_ml > 0:
            if remaining_ml <= small_bottle_ml:
                small_bottles_needed = 1
            else:
                # Check if one more large bottle is more efficient
                if remaining_ml <= large_bottle_ml:
                    large_bottles_needed += 1
                else:
                    small_bottles_needed = remaining_ml // small_bottle_ml
                    if remaining_ml % small_bottle_ml > 0:
                        small_bottles_needed += 1
                        
        bottles_needed[alcohol] = {"large": large_bottles_needed, "small": small_bottles_needed}
    return bottles_needed

def calculate_total_cost(bottles_needed, prices):
    total_cost = 0
    cost_per_type = {}
    for alcohol, bottles in bottles_needed.items():
        cost = bottles['large'] * prices[alcohol]['large'] + bottles['small'] * prices[alcohol]['small']
        cost_per_type[alcohol] = cost
        total_cost += cost
    return cost_per_type, total_cost

def calculate_and_show():
    try:
        n_guests = number_of_guests_entry.get()
        if not validate_input(n_guests):
            raise ValueError
        n_guests = int(n_guests)
        
        drinks_needed_per_type = calculate_drinks_for_party(n_guests, sample_data, preferences)
        bottles_needed = calculate_bottles_for_preferences(drinks_needed_per_type, bottle_sizes)
        cost_per_type, total_cost = calculate_total_cost(bottles_needed, prices)

        result_message = "Bottles needed per alcohol type:\n"
        for alcohol, bottles in bottles_needed.items():
            result_message += f"  {alcohol.capitalize()}: Large: {bottles['large']}, Small: {bottles['small']}\n"

        result_message += "\nCost per alcohol type:\n"
        for alcohol, cost in cost_per_type.items():
            result_message += f"  {alcohol.capitalize()}: €{cost:.2f}\n"

        result_message += f"\nTotal cost for the party: €{total_cost:.2f}"
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result_message)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of guests.")

def center_window(root, width=600, height=400):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Party Drink Calculator")
center_window(root, 600, 400)

tk.Label(root, text="Enter number of guests:").pack()
number_of_guests_entry = tk.Entry(root)
number_of_guests_entry.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate_and_show)
calculate_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=70)
result_text.pack(pady=10)

# Sample data, preferences, bottle sizes, and prices
sample_data = [4, 3.5, 0, 5, 3.5, 2.5, 3.5, 8.5, 2, 0.5, 0, 3, 3, 1.5,2]
preferences = {"vodka": 8, "rum": 4, "gin": 5}
bottle_sizes = {
    "vodka": {"large": 700, "small": 350},
    "rum": {"large": 700, "small": 350},
    "gin": {"large": 700, "small": 350}
}
prices = {
    "vodka": {"large": 18.85, "small": 9.51},
    "rum": {"large": 21.15, "small": 9.87},
    "gin": {"large": 21.13, "small":9.22 }
}

root.mainloop()
