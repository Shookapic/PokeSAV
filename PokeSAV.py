import sys
import tkinter as tk
from tkinter import filedialog

def name_to_hex(name):
    hex_map = {'a': 0x80, 'b': 0x81, 'c': 0x82, 'd': 0x83, 'e': 0x84, 'f': 0x85, 'g': 0x86, 'h': 0x87, 'i': 0x88, 'j': 0x89, 'k': 0x8A, 'l': 0x8B, 'm': 0x8C, 'n': 0x8D, 'o': 0x8E, 'p': 0x8F, 'q': 0x90, 'r': 0x91, 's': 0x92, 't': 0x93, 'u': 0x94, 'v': 0x95, 'w': 0x96, 'x': 0x97, 'y': 0x98, 'z': 0x99, ' ': 0x50}
    name_hex = [hex_map[c] for c in name.lower()]
    while len(name_hex) < 7:
        name_hex.append(hex_map[' '])
    return name_hex

def fix_checksum(file_path):
    with open(file_path, "rb+") as f:
        sav = bytearray(f.read())
        checksum = 0xff
        for i in sav[0x2598:0x3523]:
            checksum -= i
        sav[0x3523] = checksum & 0xff
        f.seek(0, 0)
        f.write(sav)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Save files", "*.sav")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def add_item():
    try:
        id_hex = int(entry_id.get(), 16)
        number = int(entry_quantity.get())
        file_path = entry_file.get()

        with open(file_path, "rb+") as f:
            sav = bytearray(f.read())
            if sav[0x25C9] <= 0x20:
                sav[0x25C9] += 1
                next_ff_index = sav.index(0xFF, 0x25C9)
                sav[next_ff_index] = id_hex
                sav[next_ff_index + 1] = number
                sav[next_ff_index + 2] = 0xFF
                f.seek(0, 0)
                f.write(sav)
                fix_checksum(file_path)
                result_label.config(text=f"Added item -> {hex(id_hex)} Quantity: {number}\nChecksum fixed too. You can quit now.")
            else:
                result_label.config(text="Cannot add item. Checksum is invalid.")
    except ValueError:
        result_label.config(text="Invalid input. Please enter valid values.")

def change_name():
    name = entry_name.get()
    file_path = entry_file.get()
    name_hex = name_to_hex(name)

    with open(file_path, "rb+") as f:
        sav = bytearray(f.read())
        sav[0x2598:0x2598 + 7] = name_hex
        f.seek(0, 0)
        f.write(sav)

    fix_checksum(file_path)

    result_label.config(text=f"Name changed to {name}\nChecksum fixed too. You can quit now.")

# GUI setup
root = tk.Tk()
root.title("Pokesave Editor")

# File Entry
label_file = tk.Label(root, text="File Path:")
label_file.grid(row=0, column=0, padx=5, pady=5)
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
button_load = tk.Button(root, text="Load File", command=load_file)
button_load.grid(row=0, column=3, padx=5, pady=5)

# Add Item Entry
label_id = tk.Label(root, text="ID (0x01 to 0xFF):")
label_id.grid(row=1, column=0, padx=5, pady=5)
entry_id = tk.Entry(root, width=10)
entry_id.grid(row=1, column=1, padx=5, pady=5)
label_quantity = tk.Label(root, text="Quantity (1 to 99):")
label_quantity.grid(row=1, column=2, padx=5, pady=5)
entry_quantity = tk.Entry(root, width=10)
entry_quantity.grid(row=1, column=3, padx=5, pady=5)
button_add_item = tk.Button(root, text="Add Item", command=add_item)
button_add_item.grid(row=1, column=4, padx=5, pady=5)

# Change Name Entry
label_name = tk.Label(root, text="New Name (7 characters):")
label_name.grid(row=2, column=0, padx=5, pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
button_change_name = tk.Button(root, text="Change Name", command=change_name)
button_change_name.grid(row=2, column=3, padx=5, pady=5)

# Result Label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=5, pady=10)

root.mainloop()
