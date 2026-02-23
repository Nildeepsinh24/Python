import tkinter as tk
from tkinter import messagebox

# --- Object-Oriented Design: Classes for Books and Members ---
class Book:
    """A class to represent a single book in the library."""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_storage_string(self):
        """Formats the book object for saving to a text file."""
        return f"{self.title},{self.author},{self.isbn}\n"

class Member:
    """A class to represent a library member."""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_storage_string(self):
        """Formats the member object for saving to a text file."""
        return f"{self.name},{self.member_id}\n"

# --- Main Application Class ---
class LibraDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LibraDesk - Simple Library Management")
        
        self.books = []
        self.members = []
        
        # --- File I/O and Exception Handling on startup ---
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        """Creates and arranges all the Tkinter GUI elements."""
        # --- Book Management Frame ---
        book_frame = tk.LabelFrame(self.root, text="Book Management", padx=10, pady=10)
        book_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(book_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=2)
        self.book_title_entry = tk.Entry(book_frame)
        self.book_title_entry.grid(row=0, column=1, sticky="ew", pady=2)

        tk.Label(book_frame, text="Author:").grid(row=1, column=0, sticky="w", pady=2)
        self.book_author_entry = tk.Entry(book_frame)
        self.book_author_entry.grid(row=1, column=1, sticky="ew", pady=2)

        tk.Label(book_frame, text="ISBN:").grid(row=2, column=0, sticky="w", pady=2)
        self.book_isbn_entry = tk.Entry(book_frame)
        self.book_isbn_entry.grid(row=2, column=1, sticky="ew", pady=2)

        add_book_button = tk.Button(book_frame, text="Add New Book", command=self.add_book)
        add_book_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # --- Member Management Frame ---
        member_frame = tk.LabelFrame(self.root, text="Member Management", padx=10, pady=10)
        member_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(member_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.member_name_entry = tk.Entry(member_frame)
        self.member_name_entry.grid(row=0, column=1, sticky="ew", pady=2)

        tk.Label(member_frame, text="Member ID:").grid(row=1, column=0, sticky="w", pady=2)
        self.member_id_entry = tk.Entry(member_frame)
        self.member_id_entry.grid(row=1, column=1, sticky="ew", pady=2)

        add_member_button = tk.Button(member_frame, text="Add New Member", command=self.add_member)
        add_member_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_book(self):
        """Gets data from entry fields, creates a Book object, and saves it."""
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()

        if title and author and isbn:
            new_book = Book(title, author, isbn)
            self.books.append(new_book)
            self.save_data()
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            # Clear entry fields
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.book_isbn_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "All book fields are required.")

    def add_member(self):
        """Gets data from entry fields, creates a Member object, and saves it."""
        name = self.member_name_entry.get()
        member_id = self.member_id_entry.get()

        if name and member_id:
            new_member = Member(name, member_id)
            self.members.append(new_member)
            self.save_data()
            messagebox.showinfo("Success", f"Member '{name}' added successfully.")
            # Clear entry fields
            self.member_name_entry.delete(0, tk.END)
            self.member_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "All member fields are required.")
    
    def load_data(self):
        """Loads book and member data from text files."""
        try:
            # Load books
            with open("books.txt", "r") as f:
                for line in f:
                    title, author, isbn = line.strip().split(',')
                    self.books.append(Book(title, author, isbn))
            # Load members
            with open("members.txt", "r") as f:
                for line in f:
                    name, member_id = line.strip().split(',')
                    self.members.append(Member(name, member_id))
        except FileNotFoundError:
            # This is okay if it's the first time running the app
            print("Data files not found. They will be created on the first save.")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading data: {e}")

    def save_data(self):
        """Saves the current list of books and members to text files."""
        try:
            # Save books
            with open("books.txt", "w") as f:
                for book in self.books:
                    f.write(book.to_storage_string())
            # Save members
            with open("members.txt", "w") as f:
                for member in self.members:
                    f.write(member.to_storage_string())
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraDeskApp(root)
    root.mainloop()