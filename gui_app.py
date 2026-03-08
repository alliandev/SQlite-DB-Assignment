import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import database


class CoffeeBeanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Bean Library")
        self.root.geometry("800x550")

        # connect to database
        self.connection = database.connect()
        database.create_tables(self.connection)

        # build the UI stuff
        self.create_widgets()

    def create_widgets(self):

        # title label at the top
        title = tk.Label(self.root, text="Coffee Bean Library", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # input section where the user types stuff
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Bean Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame, width=18)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Method:").grid(row=0, column=2, padx=5)
        self.method_entry = tk.Entry(input_frame, width=18)
        self.method_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Rating (0-100):").grid(row=0, column=4, padx=5)
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=0, column=5, padx=5)

        tk.Label(input_frame, text="Bean ID:").grid(row=1, column=0, padx=5)
        self.id_entry = tk.Entry(input_frame, width=10)
        self.id_entry.grid(row=1, column=1, padx=5)

        # sorting dropdowns (felt easier than making more buttons)
        tk.Label(input_frame, text="Sort By:").grid(row=1, column=2, padx=5)
        self.sort_option = ttk.Combobox(input_frame, values=["name", "rating"], width=15)
        self.sort_option.grid(row=1, column=3)

        tk.Label(input_frame, text="Order:").grid(row=1, column=4, padx=5)
        self.order_option = ttk.Combobox(input_frame, values=["ASC", "DESC"], width=10)
        self.order_option.grid(row=1, column=5)

        # button section
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Bean", width=15, command=self.add_bean).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View All", width=15, command=self.view_all).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Search Name", width=15, command=self.search_name).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Best Method", width=15, command=self.best_method).grid(row=0, column=3, padx=5)

        tk.Button(button_frame, text="Delete Bean", width=15, command=self.delete_bean).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Search Rating", width=15, command=self.search_rating).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Update Rating", width=15, command=self.update_rating).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Sort Beans", width=15, command=self.sort_beans).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(button_frame, text="Clear Results", width=15, command=self.clear_results).grid(row=2, column=1, pady=5)

        # results box with scrollbar
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_box = tk.Text(result_frame, height=15, width=90, yscrollcommand=scrollbar.set)
        self.result_box.pack()

        scrollbar.config(command=self.result_box.yview)

    def clear_results(self):
        self.result_box.delete("1.0", tk.END)

    def display_beans(self, beans):

        self.clear_results()

        if not beans:
            self.result_box.insert(tk.END, "No beans found...\n")
            return

        for bean in beans:
            self.result_box.insert(
                tk.END,
                f"ID:{bean['id']} | {bean['name']} ({bean['method']}) - {bean['rating']}/100\n"
            )

    def add_bean(self):

        name = self.name_entry.get().strip()
        method = self.method_entry.get().strip()

        # checking if the user forgot something
        if name == "" or method == "":
            messagebox.showerror("Error", "Name and method can't be empty.")
            return

        try:
            rating = int(self.rating_entry.get())
            if rating < 0 or rating > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 0 and 100.")
            return

        database.add_bean(self.connection, name, method, rating)

        messagebox.showinfo("Success", "Bean added!")
        self.view_all()

    def view_all(self):

        beans = database.get_all_beans(self.connection)
        self.display_beans(beans)

    def search_name(self):

        name = self.name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please type a name to search.")
            return

        beans = database.get_beans_by_name(self.connection, name)
        self.display_beans(beans)

    def best_method(self):

        name = self.name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Enter a bean name first.")
            return

        bean = database.get_best_preparation_for_bean(self.connection, name)

        self.clear_results()

        if bean:
            self.result_box.insert(
                tk.END,
                f"Best preparation for {bean['name']}:\n{bean['method']} - {bean['rating']}/100\n"
            )
        else:
            self.result_box.insert(tk.END, "No bean found.\n")

    def delete_bean(self):

        name = self.name_entry.get().strip()
        bean_id = self.id_entry.get().strip()

        # user has to enter at least something
        if name == "" and bean_id == "":
            messagebox.showerror("Error", "Enter a bean name or ID to delete.")
            return

        try:
            if bean_id:
                bean_id = int(bean_id)
                database.delete_bean_by_id(self.connection, bean_id)
            else:
                database.delete_bean(self.connection, name)
        except ValueError:
            messagebox.showerror("Error", "ID must be a number.")
            return

        messagebox.showinfo("Deleted", "Bean removed (hopefully).")
        self.view_all()

    def search_rating(self):

        try:
            rating = int(self.rating_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid rating number.")
            return

        beans = database.get_beans_by_rating(self.connection, rating)
        self.display_beans(beans)

    def update_rating(self):

        name = self.name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Enter the bean name to update.")
            return

        try:
            rating = int(self.rating_entry.get())
            if rating < 0 or rating > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be between 0 and 100.")
            return

        database.update_bean_rating(self.connection, name, rating)

        messagebox.showinfo("Updated", "Rating changed.")
        self.view_all()

    def sort_beans(self):

        sort_by = self.sort_option.get()
        order = self.order_option.get()

        # user forgot to choose sorting options
        if sort_by == "" or order == "":
            messagebox.showerror("Error", "Choose sort type and order.")
            return

        beans = database.sort_beans(self.connection, sort_by, order)
        self.display_beans(beans)


if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeBeanApp(root)
    root.mainloop()
