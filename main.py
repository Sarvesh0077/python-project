import tkinter as tk
from tkinter import messagebox
import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS contacts
                            (id INTEGER PRIMARY KEY,
                             name TEXT,
                             email TEXT,
                             phone TEXT,
                             address TEXT)''')
        self.conn.commit()

    def add_contact(self, name, email, phone, address):
        self.c.execute("INSERT INTO contacts (name, email, phone, address) VALUES (?, ?, ?, ?)", (name, email, phone, address))
        self.conn.commit()

    def get_all_contacts(self):
        self.c.execute("SELECT * FROM contacts")
        return self.c.fetchall()

    def delete_contact(self, contact_id):
        self.c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        self.conn.commit()

class ContactManagementApp:
    def __init__(self, root, database_handler):
        self.root = root
        self.root.title("Contact Management System")
        self.db = database_handler

        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.grid(row=1, column=0, sticky="e")
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=1, column=1)

        self.phone_label = tk.Label(root, text="Phone:")
        self.phone_label.grid(row=2, column=0, sticky="e")
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=2, column=1)

        self.address_label = tk.Label(root, text="Address:")
        self.address_label.grid(row=3, column=0, sticky="e")
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=3, column=1)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, columnspan=2)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=5, columnspan=2)

        self.contact_listbox = tk.Listbox(root, width=40)
        self.contact_listbox.grid(row=6, columnspan=2)

        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if name and email and phone and address:
            self.db.add_contact(name, email, phone, address)
            contact_info = f"Name: {name}, Email: {email}, Phone: {phone}, Address: {address}"
            self.contact_listbox.insert(tk.END, contact_info)
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact_info = self.contact_listbox.get(selected_index)
            contact_id = contact_info.split(",")[0].split(":")[1].strip()
            self.db.delete_contact(contact_id)
            self.contact_listbox.delete(selected_index)

    def load_contacts(self):
        contacts = self.db.get_all_contacts()
        for contact in contacts:
            contact_info = f"ID: {contact[0]}, Name: {contact[1]}, Email: {contact[2]}, Phone: {contact[3]}, Address: {contact[4]}"
            self.contact_listbox.insert(tk.END, contact_info)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    db = DatabaseHandler()
    root = tk.Tk()
    app = ContactManagementApp(root, db)
    root.mainloop()
