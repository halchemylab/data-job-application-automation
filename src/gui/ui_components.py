import tkinter as tk

def create_section_divider(parent, text):
    divider = tk.Label(parent, text=text, font=("Arial", 16, "bold"), bg="#e0e0e0", fg="black", width=60)
    divider.pack(pady=15, fill='x')

def create_description(parent, text):
    description = tk.Label(parent, text=text, font=("Arial", 11), fg="gray40", bg="white", wraplength=650, justify="left")
    description.pack(pady=5)

def create_labeled_entry(parent, label_text, variable):
    frame = tk.Frame(parent, bg="white")
    frame.pack(fill='x', pady=5)

    label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="white", fg="black", anchor="w")
    label.pack(side="top", anchor="w")

    if isinstance(variable, str):
        entry = tk.Entry(frame, width=80, font=("Arial", 12), bg="#f9f9f9", fg="black", insertbackground="black")
        setattr(parent, variable, entry)
    else:
        entry = tk.Entry(frame, textvariable=variable, width=80, font=("Arial", 12), bg="#f9f9f9", fg="black", insertbackground="black")
    entry.pack(side="top", anchor="w")
    return entry
