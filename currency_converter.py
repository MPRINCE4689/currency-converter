import tkinter as tk
from tkinter import ttk
import csv

# Main window setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("600x500")
root.resizable(False, False)

# Currency options
currencies = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CHF", "CNY", "SGD"]
from_currency = tk.StringVar(value=currencies[0])
to_currency = tk.StringVar(value=currencies[1])

# Frame for input
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(pady=10)

# Amount entry
tk.Label(input_frame, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

# From dropdown
tk.Label(input_frame, text="From:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
from_dropdown = tk.OptionMenu(input_frame, from_currency, *currencies)
from_dropdown.grid(row=1, column=1, padx=5, pady=5)

# To dropdown
tk.Label(input_frame, text="To:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
to_dropdown = tk.OptionMenu(input_frame, to_currency, *currencies)
to_dropdown.grid(row=2, column=1, padx=5, pady=5)

# Static exchange rates (Updated)
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.8654,
    "GBP": 0.76,
    "INR": 86.09,
    "JPY": 144.17,
    "CAD": 1.35,
    "AUD": 1.48,
    "CHF": 0.90,
    "CNY": 7.25,
    "SGD": 1.36
}
history_records = []

# Result label (shown in GUI)
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Arial", 11), fg="green")
result_label.pack(pady=(0, 5))

# Conversion logic
def convert_currency():
    try:
        amount_str = amount_entry.get().strip()
        amount = float(amount_str)
    except ValueError:
        result_var.set("Please enter a valid number.")
        return

    from_cur = from_currency.get()
    to_cur = to_currency.get()

    if from_cur == to_cur:
        result_amount = amount
        rate_used = 1.0
    else:
        rate_from = exchange_rates.get(from_cur)
        rate_to = exchange_rates.get(to_cur)
        if rate_from is None or rate_to is None:
            result_var.set("Unsupported currency selected.")
            return
        rate_used = rate_to / rate_from
        result_amount = amount * rate_used

    result_amount_str = f"{result_amount:.2f}"
    rate_used_str = f"{rate_used:.4f}"
    

    # Show result in GUI
    result_var.set(f"{amount_str} {from_cur} = {result_amount_str} {to_cur}")

    # Add to history
    history_records.append([amount_str, from_cur, to_cur, result_amount_str, rate_used_str,])
    history_table.insert("", "end", values=(amount_str, from_cur, to_cur, result_amount_str, rate_used_str))

# Convert button
convert_btn = tk.Button(input_frame, text="Convert Currency", command=convert_currency, bg="#008080", fg="white")
convert_btn.grid(row=3, column=0, columnspan=2, pady=10)



# ===== HISTORY SECTION =====
history_frame = tk.Frame(root, padx=10, pady=5)
history_frame.pack(fill="x")
tk.Label(history_frame, text="Conversion History", font=("Arial", 12, "bold")).pack(side="left")

# Export and Clear buttons
buttons_frame = tk.Frame(history_frame)
buttons_frame.pack(side="right")

def export_history():
    if not history_records:
        return
    filename = "conversion_history.csv"
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Amount", "From", "To", "Result", "Rate", "Timestamp"])
            writer.writerows(history_records)
    except Exception:
        pass  # silently ignore

def clear_history():
    history_records.clear()
    for row in history_table.get_children():
        history_table.delete(row)

tk.Button(buttons_frame, text="Export CSV", bg="#008080", fg="white", command=export_history).pack(side="left", padx=5)
tk.Button(buttons_frame, text="Clear History", bg="#008080", fg="white", command=clear_history).pack(side="left")

# Treeview Table for History
columns = ("Amount", "From", "To", "Result", "Rate", "Time")
history_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    history_table.heading(col, text=col)
    history_table.column(col, width=80 if col != "Time" else 140)
history_table.pack(fill="both", expand=True, padx=10, pady=5)

# Scrollbars
scroll_y = tk.Scrollbar(history_table, orient="vertical", command=history_table.yview)
scroll_x = tk.Scrollbar(history_table, orient="horizontal", command=history_table.xview)
history_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

# Start the app
root.mainloop()