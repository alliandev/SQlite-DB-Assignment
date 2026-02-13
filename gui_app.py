import tkinter as tk
from tkinter import messagebox
import database


class CoffeeBeanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Bean Library")
        self.root.geometry("700x500")

        self.connection = database.connect()
        database.create_tables(self.connection)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Coffee Bean Library", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Bean Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Method:").grid(row=0, column=2, padx=5)
        self.method_entry = tk.Entry(input_frame, width=20)
        self.method_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Rating (0-100):").grid(row=0, column=4, padx=5)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=0, column=5, padx=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Bean", width=15, command=self.add_bean).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View All", width=15, command=self.view_all).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Search Name", width=15, command=self.search_name).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Best Method", width=15, command=self.best_method).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Delete Bean", width=15, command=self.delete_bean).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Search Rating", width=15, command=self.search_rating).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Update Rating", width=15, command=self.update_rating).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Clear Results", width=15, command=self.clear_results).grid(row=1, column=3, padx=5, pady=5)

        self.result_box = tk.Text(self.root, height=15, width=80)
        self.result_box.pack(pady=10)

    def clear_results(self):
        self.result_box.delete("1.0", tk.END)

    def display_beans(self, beans):
        self.clear_results()
        if not beans:
            self.result_box.insert(tk.END, "No beans found.\n")
            return

        for bean in beans:
            self.result_box.insert(
                tk.END,
                f"{bean['name']} ({bean['method']}) - {bean['rating']}/100\n"
            )

    def add_bean(self):
        name = self.name_entry.get().strip()
        method = self.method_entry.get().strip()

        try:
            rating = int(self.rating_entry.get())
            if rating < 0 or rating > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 0 and 100.")
            return

        database.add_bean(self.connection, name, method, rating)
        messagebox.showinfo("Success", "Bean added successfully!")
        self.view_all()

    def view_all(self):
        beans = database.get_all_beans(self.connection)
        self.display_beans(beans)

    def search_name(self):
        name = self.name_entry.get().strip()
        beans = database.get_beans_by_name(self.connection, name)
        self.display_beans(beans)

    def best_method(self):
        name = self.name_entry.get().strip()
        bean = database.get_best_preparation_for_bean(self.connection, name)

        self.clear_results()

        if bean:
            self.result_box.insert(
                tk.END,
                f"Best preparation for {bean['name']}:\n"
                f"{bean['method']} - {bean['rating']}/100\n"
            )
        else:
            self.result_box.insert(tk.END, "No bean found.\n")

    def delete_bean(self):
        name = self.name_entry.get().strip()
        database.delete_bean(self.connection, name)
        messagebox.showinfo("Deleted", "Bean(s) deleted.")
        self.view_all()

    def search_rating(self):
        try:
            rating = int(self.rating_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid rating.")
            return

        beans = database.get_beans_by_rating(self.connection, rating)
        self.display_beans(beans)

    def update_rating(self):
        name = self.name_entry.get().strip()

        try:
            rating = int(self.rating_entry.get())
            if rating < 0 or rating > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be between 0 and 100.")
            return

        database.update_bean_rating(self.connection, name, rating)
        messagebox.showinfo("Updated", "Rating updated.")
        self.view_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeBeanApp(root)
    root.mainloop()
