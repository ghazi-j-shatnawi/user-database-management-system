import os
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd

FILE_NAME = "database.xlsx"


def load_data():
    if os.path.exists(FILE_NAME):
        g = pd.read_excel(FILE_NAME)
    else:
        g = pd.DataFrame(columns=["ID", "name", "phone", "addres"])
    return g


def save_data(g):
    g.to_excel(FILE_NAME, index=False)


def clear_table():
    for item in table.get_children():
        table.delete(item)


def show_data(g_data):
    clear_table()

    for _, row in g_data.iterrows():
        table.insert(
            "",
            "end",
            values=(row["ID"], row["name"], row["phone"], row["addres"]),
        )

    users_count.config(text=f"Users: {len(g_data)}")


def refresh_data():
    g_data = load_data()
    show_data(g_data)
    status_label.config(text="Database refreshed successfully")


def open_add_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add User")
    add_window.geometry("450x450")
    add_window.resizable(False, False)
    add_window.configure(bg="#111827")

    add_window.transient(root)
    add_window.grab_set()

    title = tk.Label(
        add_window,
        text="Add New User",
        font=("Segoe UI", 20, "bold"),
        bg="#111827",
        fg="white",
    )
    title.pack(pady=(25, 15))

    form_frame = tk.Frame(add_window, bg="#111827")
    form_frame.pack(fill="x", padx=45)

    tk.Label(
        form_frame,
        text="Name",
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#d1d5db",
    ).pack(anchor="w")
    name_entry = tk.Entry(
        form_frame,
        font=("Segoe UI", 11),
        bg="#1f2937",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    name_entry.pack(fill="x", ipady=7, pady=(3, 12))

    tk.Label(
        form_frame,
        text="Phone",
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#d1d5db",
    ).pack(anchor="w")
    phone_entry = tk.Entry(
        form_frame,
        font=("Segoe UI", 11),
        bg="#1f2937",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    phone_entry.pack(fill="x", ipady=7, pady=(3, 12))

    tk.Label(
        form_frame,
        text="Address",
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#d1d5db",
    ).pack(anchor="w")
    address_entry = tk.Entry(
        form_frame,
        font=("Segoe UI", 11),
        bg="#1f2937",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    address_entry.pack(fill="x", ipady=7, pady=(3, 20))

    def save_new_user():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()

        if name == "" or phone == "" or address == "":
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all information.",
                parent=add_window,
            )
            return

        g_data = load_data()

        if not g_data.empty:
            if g_data["name"].astype(str).str.lower().eq(name.lower()).any():
                messagebox.showerror(
                    "User Exists",
                    "This user already exists.",
                    parent=add_window,
                )
                return

        new_id = 1 if g_data.empty else int(g_data["ID"].max()) + 1

        dict1 = {"ID": new_id, "name": name, "phone": phone, "addres": address}
        z = pd.DataFrame([dict1])
        g_data = pd.concat([g_data, z], ignore_index=True)

        save_data(g_data)
        show_data(g_data)

        status_label.config(text="User added successfully")
        add_window.destroy()
        messagebox.showinfo("Success", "User added successfully.")

    add_btn = tk.Button(
        form_frame,
        text="Add User",
        font=("Segoe UI", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=save_new_user,
    )
    add_btn.pack(fill="x", ipady=8, pady=(5, 0))


def search_user(event=None):
    search_text = search_entry.get().strip()

    if search_text == "":
        messagebox.showwarning("Search", "Please enter something to search.")
        return

    g_data = load_data()

    if g_data.empty:
        messagebox.showinfo("Search", "Database is empty.")
        return

    result = g_data[
        g_data["name"]
        .astype(str)
        .str.contains(search_text, case=False, na=False)
        | g_data["phone"]
        .astype(str)
        .str.contains(search_text, case=False, na=False)
        | g_data["addres"]
        .astype(str)
        .str.contains(search_text, case=False, na=False)
        | g_data["ID"]
        .astype(str)
        .str.contains(search_text, case=False, na=False)
    ]

    show_data(result)

    if result.empty:
        status_label.config(text="No users found")
    else:
        status_label.config(text=f"{len(result)} user(s) found")


def show_all_users():
    g_data = load_data()

    if g_data.empty:
        clear_table()
        users_count.config(text="Users: 0")
        messagebox.showinfo("Database", "Database is empty.")
        return

    show_data(g_data)
    status_label.config(text="Showing all users")


def get_selected_user():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection", "Please select a user first from the list."
        )
        return None

    values = table.item(selected[0], "values")
    return values


def update_user():
    values = get_selected_user()

    if values is None:
        return

    user_id = values[0]
    g_data = load_data()

    result = g_data[g_data["ID"].astype(str) == str(user_id)]

    if result.empty:
        messagebox.showerror("Error", "User not found in database.")
        return

    update_window = tk.Toplevel(root)
    update_window.title("Update User")
    update_window.geometry("450x450")
    update_window.resizable(False, False)
    update_window.configure(bg="#111827")

    update_window.transient(root)
    update_window.grab_set()

    title = tk.Label(
        update_window,
        text="Update User Details",
        font=("Segoe UI", 20, "bold"),
        bg="#111827",
        fg="white",
    )
    title.pack(pady=(25, 15))

    form_frame = tk.Frame(update_window, bg="#111827")
    form_frame.pack(fill="x", padx=45)

    tk.Label(form_frame, text="Name", font=("Segoe UI", 10), bg="#111827", fg="#d1d5db").pack(anchor="w")
    new_name = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white", relief="flat")
    new_name.pack(fill="x", ipady=7, pady=(3, 12))
    new_name.insert(0, str(result.iloc[0]["name"]))

    tk.Label(form_frame, text="Phone", font=("Segoe UI", 10), bg="#111827", fg="#d1d5db").pack(anchor="w")
    new_phone = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white", relief="flat")
    new_phone.pack(fill="x", ipady=7, pady=(3, 12))
    new_phone.insert(0, str(result.iloc[0]["phone"]))

    tk.Label(form_frame, text="Address", font=("Segoe UI", 10), bg="#111827", fg="#d1d5db").pack(anchor="w")
    new_address = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white", relief="flat")
    new_address.pack(fill="x", ipady=7, pady=(3, 20))
    new_address.insert(0, str(result.iloc[0]["addres"]))

    def save_update():
        name = new_name.get().strip()
        phone = new_phone.get().strip()
        address = new_address.get().strip()

        if name == "" or phone == "" or address == "":
            messagebox.showwarning(
                "Missing Information",
                "All information is required.",
                parent=update_window,
            )
            return

        g_data["name"] = g_data["name"].astype(str)
        g_data["phone"] = g_data["phone"].astype(str)
        g_data["addres"] = g_data["addres"].astype(str)

        mask = g_data["ID"].astype(str) == str(user_id)
        g_data.loc[mask, "name"] = name
        g_data.loc[mask, "phone"] = phone
        g_data.loc[mask, "addres"] = address

        save_data(g_data)
        show_data(g_data)

        status_label.config(text="User updated successfully")
        update_window.destroy()
        messagebox.showinfo("Success", "User updated successfully.")

    save_btn = tk.Button(
        form_frame,
        text="Save Changes",
        font=("Segoe UI", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=save_update,
    )
    save_btn.pack(fill="x", ipady=8, pady=(5, 0))


def delete_user():
    values = get_selected_user()

    if values is None:
        return

    user_id = values[0]
    user_name = values[1]

    answer = messagebox.askyesno(
        "Delete User",
        f"Are you sure you want to delete\n\n{user_name} (ID: {user_id})?",
    )

    if not answer:
        return

    g_data = load_data()

    result = g_data[g_data["ID"].astype(str) == str(user_id)]

    if result.empty:
        messagebox.showerror("Error", "User not found.")
        return

    g_data = g_data.drop(result.index).reset_index(drop=True)

    save_data(g_data)
    show_data(g_data)

    status_label.config(text="User deleted successfully")
    messagebox.showinfo("Success", "User deleted successfully.")


def clear_search():
    search_entry.delete(0, tk.END)
    show_all_users()


def exit_program():
    answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if answer:
        root.destroy()


root = tk.Tk()
root.title("User Database")
root.geometry("1100x650")
root.minsize(950, 550)
root.configure(bg="#111827")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1f2937",
    foreground="white",
    rowheight=38,
    fieldbackground="#1f2937",
    borderwidth=0,
    font=("Segoe UI", 10),
)

style.configure(
    "Treeview.Heading",
    background="#374151",
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
)

style.map(
    "Treeview",
    background=[("selected", "#2563eb")],
    foreground=[("selected", "white")],
)

sidebar = tk.Frame(root, bg="#0f172a", width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo = tk.Label(
    sidebar,
    text="USER\nDATABASE",
    font=("Segoe UI", 20, "bold"),
    bg="#0f172a",
    fg="white",
    justify="left",
)
logo.pack(anchor="w", padx=25, pady=(35, 45))


def sidebar_button(text, command):
    button = tk.Button(
        sidebar,
        text=text,
        font=("Segoe UI", 11),
        bg="#0f172a",
        fg="#d1d5db",
        activebackground="#1e293b",
        activeforeground="white",
        anchor="w",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=25,
        command=command,
    )
    button.pack(fill="x", ipady=12)
    return button


sidebar_button("   +   Add User", open_add_window)
sidebar_button("   ⟳   Show All Users", show_all_users)
sidebar_button("   ↻   Refresh", refresh_data)
sidebar_button("   ✕   Delete User", delete_user)

separator = tk.Frame(sidebar, bg="#1e293b", height=1)
separator.pack(fill="x", padx=20, pady=25)

exit_button = tk.Button(
    sidebar,
    text="   Exit",
    font=("Segoe UI", 11),
    bg="#0f172a",
    fg="#f87171",
    activebackground="#1e293b",
    activeforeground="#ef4444",
    anchor="w",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=25,
    command=exit_program,
)
exit_button.pack(fill="x", ipady=12)

main = tk.Frame(root, bg="#111827")
main.pack(side="left", fill="both", expand=True)

header = tk.Frame(main, bg="#111827")
header.pack(fill="x", padx=35, pady=(30, 15))

title = tk.Label(
    header,
    text="Dashboard",
    font=("Segoe UI", 26, "bold"),
    bg="#111827",
    fg="white",
)
title.pack(side="left")

users_count = tk.Label(
    header,
    text="Users: 0",
    font=("Segoe UI", 11),
    bg="#1f2937",
    fg="#93c5fd",
    padx=15,
    pady=7,
)
users_count.pack(side="right")

search_frame = tk.Frame(main, bg="#111827")
search_frame.pack(fill="x", padx=35, pady=(5, 20))

search_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 11),
    bg="#1f2937",
    fg="white",
    insertbackground="white",
    relief="flat",
)
search_entry.pack(side="left", fill="x", expand=True, ipady=10)
search_entry.bind("<Return>", search_user)

search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Segoe UI", 10, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    command=search_user,
)
search_button.pack(side="left", padx=(10, 5), ipady=7)

clear_button = tk.Button(
    search_frame,
    text="Clear",
    font=("Segoe UI", 10),
    bg="#374151",
    fg="white",
    activebackground="#4b5563",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    command=clear_search,
)
clear_button.pack(side="left", padx=(5, 0), ipady=7)

table_frame = tk.Frame(main, bg="#111827")
table_frame.pack(fill="both", expand=True, padx=35)

table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Phone", "Address"),
    show="headings",
    selectmode="browse",
)

table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Phone", text="Phone")
table.heading("Address", text="Address")

table.column("ID", width=70, anchor="center")
table.column("Name", width=220)
table.column("Phone", width=180)
table.column("Address", width=350)

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=table.yview
)
table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

button_frame = tk.Frame(main, bg="#111827")
button_frame.pack(fill="x", padx=35, pady=20)

update_button = tk.Button(
    button_frame,
    text="Update Selected",
    font=("Segoe UI", 10, "bold"),
    bg="#374151",
    fg="white",
    activebackground="#4b5563",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    command=update_user,
)
update_button.pack(side="left", ipady=8)

delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    font=("Segoe UI", 10, "bold"),
    bg="#991b1b",
    fg="white",
    activebackground="#7f1d1d",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    command=delete_user,
)
delete_button.pack(side="left", padx=10, ipady=8)

add_button = tk.Button(
    button_frame,
    text="+ Add User",
    font=("Segoe UI", 10, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    command=open_add_window,
)
add_button.pack(side="right", ipady=8)

status_frame = tk.Frame(main, bg="#0f172a", height=35)
status_frame.pack(fill="x", side="bottom")

status_label = tk.Label(
    status_frame,
    text="Ready",
    font=("Segoe UI", 9),
    bg="#0f172a",
    fg="#9ca3af",
    anchor="w",
)
status_label.pack(padx=20, pady=8)

show_all_users()

root.mainloop()