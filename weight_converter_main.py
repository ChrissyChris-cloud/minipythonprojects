import tkinter as tk
from tkinter import messagebox

# Conversion function (UNCHANGED)
def convert_weight(weight, unit):
    unit = unit.strip().lower()
    if unit in ["lbs", "lb", "pounds", "pound"]:
        factor = 0.45359237
        result = weight * factor
        return f"{weight:g} lb = {result:.2f} kg"
    elif unit in ["kg", "kgs", "kilograms", "kilogram"]:
        factor = 2.20462262
        result = weight * factor
        return f"{weight:g} kg = {result:.2f} lb"
    else:
        return "Unit must be 'lb' or 'kg'"

# Button callback (UNCHANGED)
def on_convert():
    try:
        weight = float(weight_entry.get())
        if weight < 0:
            messagebox.showerror("Error", "Weight cannot be negative.")
            return
        result_label.config(text=convert_weight(weight, unit_var.get()))
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

# Build GUI (improved layout, expanding entry, better visuals)
root = tk.Tk()
root.title("Weight Converter (lb ↔ kg)")
root.geometry("400x200")
root.minsize(350, 180)

# Configure grid to expand properly
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(3, weight=1)

# Labels and entry
tk.Label(root, text="Weight:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="E")
weight_entry = tk.Entry(root, font=("Arial", 11))
weight_entry.grid(row=0, column=1, padx=10, pady=10, sticky="EW")

tk.Label(root, text="Unit:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="E")
unit_var = tk.StringVar(value="lb")
tk.OptionMenu(root, unit_var, "lb", "kg").grid(row=1, column=1, padx=10, pady=10, sticky="EW")

# Convert button
tk.Button(root, text="Convert", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=on_convert).grid(
    row=2, column=0, columnspan=2, pady=15, padx=10, sticky="EW"
)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12), fg="#333")
result_label.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="NSEW")

root.mainloop()



