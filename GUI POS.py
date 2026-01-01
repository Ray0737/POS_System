import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os 
import calendar

### INITIAL CONFIGURATION ###

users = {"Ray": "010410"}
# Menu items with prices
menu_items = {
    "Thai Tea": 45.00,
    "Milk Tea": 40.00,
    "Matcha": 55.00,
    "Drip Coffee": 60.00
}
staff = ["Ray", "View", "Gain"]

current_user = None 
cart = []

### JSON FILE SYSTEM ###

def get_data_file_path(username):
    return f"{username}_pos_data.json"

def save_data_to_json():
    global current_user, tree
    if not current_user:
        messagebox.showerror("Error", "No user logged in.")
        return
    
    records = []
    for item in tree.get_children():
        values = tree.item(item, 'values')
        records.append({
            "item": values[0],
            "status": values[1],
            "type": values[2],
            "timestamp": values[3],
            "notes": values[4],
            "staff": values[5],
            "total": values[6]
        })

    try:
        with open(get_data_file_path(current_user), 'w') as f:
            json.dump(records, f, indent=4)
        messagebox.showinfo("Success", "Data saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Save failed: {e}")

def load_data_from_json():
    global current_user, tree
    file_path = get_data_file_path(current_user)
    if not os.path.exists(file_path): return
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        tree.delete(*tree.get_children())
        for r in data:
            tree.insert("", tk.END, values=(r["item"], r["status"], r["type"], r["timestamp"], r["notes"], r["staff"], r["total"]))
    except Exception as e:
        print(f"Load error: {e}")

### POS LOGIC ###

def add_to_cart():
    item = item_var.get()
    try:
        qty = int(qty_entry.get())
        if qty <= 0: raise ValueError
    except:
        messagebox.showwarning("Input Error", "Please enter a valid quantity.")
        return

    price = menu_items[item] * qty
    cart.append({"item": item, "qty": qty, "price": price})
    update_cart_display()

def update_cart_display():
    cart_list.delete(0, tk.END)
    subtotal = 0
    for i in cart:
        cart_list.insert(tk.END, f"{i['item']} x{i['qty']} - {i['price']:.2f} THB")
        subtotal += i['price']
    
    tax = subtotal * 0.07
    total = subtotal + tax
    total_label.config(text=f"Total (Inc. 7% VAT): {total:.2f} THB")

def checkout():
    global cart
    if not cart:
        messagebox.showwarning("Empty Cart", "No items to checkout.")
        return
    
    subtotal = sum(item['price'] for item in cart)
    total = subtotal * 1.07
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = ", ".join([f"{i['item']}x{i['qty']}" for i in cart])
    
    # Add to main ledger
    tree.insert("", 0, values=(summary, "Completed ✅", "SALE", timestamp, notes_entry.get(), staff_var.get(), f"{total:.2f}"))
    
    # Clear cart
    cart = []
    update_cart_display()
    notes_entry.delete(0, tk.END)
    messagebox.showinfo("POS", f"Transaction Complete: {total:.2f} THB")

### UI HELPERS ###

def update_clock(label):
    label.config(text=datetime.now().strftime("%H:%M:%S"))
    label.after(1000, update_clock, label)

def login():
    global current_user
    username = user_entry.get()
    password = code_entry.get()
    if username in users and users[username] == password:
        current_user = username
        login_root.destroy()
        main_window()
    else:
        messagebox.showerror("Auth Error", "Invalid Credentials")

### WINDOWS ###

    
def display_login():
    global user_entry, code_entry, login_root
    login_root = tk.Tk()
    login_root.title("POS System Login")
    login_root.geometry("400x200")
    
    input_frame = tk.Frame(login_root)
    input_frame.pack(pady=20)
    
    password_frame = tk.Frame(login_root)
    password_frame.pack(pady=5)
    
    tk.Label(input_frame, text="System Login").pack(side="top", pady=10)
    tk.Label(input_frame, text="Username:").pack(side="left")
    user_entry = tk.Entry(input_frame, width=30)
    user_entry.pack(padx=10, side="left")

    tk.Label(password_frame, text="Password:").pack(side="left")
    code_entry = tk.Entry(password_frame, width=30, show="*")
    code_entry.pack(padx=10, side="left")

    tk.Button(login_root, text="Submit", command=login).pack(pady=15)
    login_root.mainloop()

def main_window():
    global tree, item_var, qty_entry, cart_list, total_label, staff_var, notes_entry
    
    root = tk.Tk()
    root.title(f"Cafe POS & Manager - User: {current_user}")
    root.geometry("1200x700")

    # --- TOP POS BAR ---
    pos_frame = tk.LabelFrame(root, text="Point of Sale", padx=10, pady=10)
    pos_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(pos_frame, text="Item:").grid(row=0, column=0)
    item_var = tk.StringVar(value="Thai Tea")
    tk.OptionMenu(pos_frame, item_var, *menu_items.keys()).grid(row=0, column=1, padx=5)

    tk.Label(pos_frame, text="Qty:").grid(row=0, column=2)
    qty_entry = tk.Entry(pos_frame, width=5)
    qty_entry.insert(0, "1")
    qty_entry.grid(row=0, column=3, padx=5)

    tk.Button(pos_frame, text="Add to Cart", command=add_to_cart, bg="green", fg="white").grid(row=0, column=4, padx=5)

    # --- CART & TOTALS ---
    cart_frame = tk.Frame(root)
    cart_frame.pack(fill="x", padx=10)

    cart_list = tk.Listbox(cart_frame, height=5, width=50)
    cart_list.pack(side="left", padx=5)

    action_frame = tk.Frame(cart_frame)
    action_frame.pack(side="left", padx=20)

    total_label = tk.Label(action_frame, text="Total: 0.00 THB", font=("Arial", 12, "bold"))
    total_label.pack()

    tk.Label(action_frame, text="Staff:").pack(side="left")
    staff_var = tk.StringVar(value=current_user)
    tk.OptionMenu(action_frame, staff_var, *staff).pack(side="left")

    tk.Button(action_frame, text="CHECKOUT", command=checkout, bg="#11294F", fg="white", font=("Arial", 10, "bold"), height=2).pack(padx=10)

    # --- LEDGER / TASK VIEW ---
    ledger_frame = tk.LabelFrame(root, text="Transaction History & Tasks")
    ledger_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Item/Task", "Status", "Type", "Timestamp", "Notes", "Staff", "Amount")
    tree = ttk.Treeview(ledger_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    
    tree.pack(side="left", fill="both", expand=True)

    # Right side Controls
    ctrl_frame = tk.Frame(ledger_frame)
    ctrl_frame.pack(side="right", fill="y", padx=5)

    tk.Label(ctrl_frame, text="Transaction Notes:").pack()
    notes_entry = tk.Entry(ctrl_frame)
    notes_entry.pack(pady=5)

    tk.Button(ctrl_frame, text="Save Data", command=save_data_to_json, width=15).pack(pady=5)
    tk.Button(ctrl_frame, text="Delete Entry", command=lambda: tree.delete(tree.selection()), width=15).pack(pady=5)
    
    clock_label = tk.Label(root, text="", font=("Arial", 10))
    clock_label.pack(side="bottom", anchor="e", padx=10)
    update_clock(clock_label)

    load_data_from_json()
    root.mainloop()

if __name__ == "__main__":
    display_login()