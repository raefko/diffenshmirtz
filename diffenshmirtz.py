import os
import difflib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from tkinter import filedialog


def find_files(directory, extensions):
    """Recursively find files in directory with given extensions."""
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                relative_path = os.path.relpath(
                    os.path.join(root, file), start=directory
                )
                matches.append(relative_path)
    return matches


def diff_files(file1, file2):
    """Generate a diff between two files."""
    with open(file1, "r") as f1, open(file2, "r") as f2:
        diff = difflib.unified_diff(
            f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2
        )
    return list(diff)


class FileDiffApp:
    def __init__(self, root, dir1, dir2, extensions):
        self.root = root
        self.dir1 = dir1
        self.dir2 = dir2
        self.extensions = tuple(extensions.split(","))

        self.update_files()  # Initialize file lists and sets
        self.create_widgets()
        self.populate_tabs()

    def create_widgets(self):
        # Set modern style
        style = ttk.Style(self.root)
        style.configure("TNotebook", background="#f5f5f5")
        style.configure(
            "TNotebook.Tab",
            padding=[10, 5],
            relief="flat",
            background="#e0e0e0",
            foreground="#333333",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff")],
            foreground=[("selected", "#007bff")],
        )
        style.configure("TFrame", background="#f5f5f5")
        style.configure(
            "TButton",
            padding=[10, 5],
            relief="flat",
            background="#007bff",
            foreground="#ffffff",
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "TButton",
            background=[("pressed", "#0056b3"), ("active", "#0056b3")],
        )
        style.configure(
            "TListbox",
            padding=[5],
            background="#ffffff",
            foreground="#333333",
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "TScrollbar",
            background="#cccccc",
            troughcolor="#e0e0e0",
            arrowcolor="#333333",
        )

        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Unique Files Tab
        self.unique_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.unique_tab, text="Unique Files")

        self.unique_listbox_frame = ttk.Frame(self.unique_tab)
        self.unique_listbox_frame.pack(expand=1, fill="both", padx=5, pady=5)

        self.unique_listbox = tk.Listbox(
            self.unique_listbox_frame, selectmode=tk.SINGLE
        )
        self.unique_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.unique_scrollbar = tk.Scrollbar(
            self.unique_listbox_frame,
            orient=tk.VERTICAL,
            command=self.unique_listbox.yview,
        )
        self.unique_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.unique_listbox.config(yscrollcommand=self.unique_scrollbar.set)

        self.unique_listbox.bind("<<ListboxSelect>>", self.show_unique_files)

        # Differences Tab
        self.diff_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.diff_tab, text="Differences")

        self.diff_listbox_frame = ttk.Frame(self.diff_tab)
        self.diff_listbox_frame.pack(expand=1, fill="both", padx=5, pady=5)

        self.diff_listbox = tk.Listbox(
            self.diff_listbox_frame, selectmode=tk.SINGLE
        )
        self.diff_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.diff_scrollbar = tk.Scrollbar(
            self.diff_listbox_frame,
            orient=tk.VERTICAL,
            command=self.diff_listbox.yview,
        )
        self.diff_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.diff_listbox.config(yscrollcommand=self.diff_scrollbar.set)

        self.diff_listbox.bind("<<ListboxSelect>>", self.show_diff)

        # Change Extensions Button
        self.change_ext_button = ttk.Button(
            self.root, text="Change Extensions", command=self.change_extensions
        )
        self.change_ext_button.pack(pady=10, fill="x", padx=10)

    def update_files(self):
        """Update file lists based on current extensions."""
        self.files1 = find_files(self.dir1, self.extensions)
        self.files2 = find_files(self.dir2, self.extensions)

        self.files1_set = set(self.files1)
        self.files2_set = set(self.files2)

        self.common_files = self.files1_set & self.files2_set
        self.unique_to_dir1 = self.files1_set - self.files2_set
        self.unique_to_dir2 = self.files2_set - self.files1_set

    def populate_tabs(self):
        """Populate tabs with current file data."""
        if not hasattr(self, "unique_to_dir1"):
            return

        self.unique_listbox.delete(0, tk.END)
        for file in self.unique_to_dir1:
            self.unique_listbox.insert(tk.END, f"Unique in {self.dir1}: {file}")
        for file in self.unique_to_dir2:
            self.unique_listbox.insert(tk.END, f"Unique in {self.dir2}: {file}")

        self.diff_listbox.delete(0, tk.END)
        for file in self.common_files:
            file1 = os.path.join(self.dir1, file)
            file2 = os.path.join(self.dir2, file)
            diff = diff_files(file1, file2)
            if diff:
                self.diff_listbox.insert(tk.END, file)

    def change_extensions(self):
        """Prompt for new file extensions and update the view."""
        new_extensions = simpledialog.askstring(
            "File Extensions",
            "Enter new comma-separated file extensions (e.g., py,txt):",
        )
        if new_extensions:
            self.extensions = tuple(new_extensions.split(","))
            self.update_files()
            self.populate_tabs()

    def show_unique_files(self, event):
        selected = self.unique_listbox.curselection()
        if selected:
            file_info = self.unique_listbox.get(selected[0])
            messagebox.showinfo("Unique File", file_info)

    def show_diff(self, event):
        selected = self.diff_listbox.curselection()
        if selected:
            file = self.diff_listbox.get(selected[0])
            file1 = os.path.join(self.dir1, file)
            file2 = os.path.join(self.dir2, file)
            diff = diff_files(file1, file2)

            diff_window = tk.Toplevel(self.root)
            diff_window.title(f"Differences for {file}")

            text_area = scrolledtext.ScrolledText(
                diff_window,
                wrap=tk.WORD,
                font=("Courier New", 10),
                bg="#f5f5f5",
            )
            text_area.pack(expand=1, fill="both", padx=10, pady=10)
            text_area.insert(tk.END, "".join(diff))
            text_area.configure(state="disabled")


def main():
    root = tk.Tk()
    root.title("File Diff Viewer")
    root.geometry("800x600")  # Set initial window size

    # Get directory paths and extensions from the user
    dir1 = filedialog.askdirectory(title="Select the first directory")
    dir2 = filedialog.askdirectory(title="Select the second directory")

    if not dir1 or not dir2:
        messagebox.showerror("Error", "Both directories must be selected!")
        root.destroy()
        return

    extensions = simpledialog.askstring(
        "File Extensions",
        "Enter comma-separated file extensions (e.g., py,txt):",
    )

    if not extensions:
        messagebox.showerror("Error", "File extensions are required!")
        root.destroy()
        return

    app = FileDiffApp(root, dir1, dir2, extensions)
    root.mainloop()


if __name__ == "__main__":
    main()
