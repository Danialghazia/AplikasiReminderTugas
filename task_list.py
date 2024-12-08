# task_list.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import datetime

class TaskListApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Daftar Tugas")
        self.root.geometry("800x600")
        self.tasks = []
        self.create_task_list()

    def create_task_list(self):
        # Create a frame for the task list
        frame = ttk.Frame(self.root)
        frame.pack(fill='both', expand=True)

        # Create a Treeview to display tasks
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas', 'Progress')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Load tasks
        self.load_tasks()

        # Create buttons for updating and deleting tasks
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        update_button = ttk.Button(button_frame, text="Perbarui Progress", command=self.update_progress)
        update_button.pack(side='left', padx=5)

        delete_button = ttk.Button(button_frame, text="Hapus Tugas", command=self.delete_task)
        delete_button.pack(side='left', padx=5)

        back_button = ttk.Button(button_frame, text="Kembali ke Dashboard", command=self.root.destroy)
        back_button.pack(side='left', padx=5)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                all_tasks = json.load(f)
                # Filter tasks for the current user
                self.tasks = [task for task in all_tasks if task.get('username') == self.username]
                for task in self.tasks:
                    self.tree.insert('', 'end', values=(
                        task['matkul'],
                        task['deskripsi'],
                        task['tenggat'],
                        task['prioritas'],
                        f"{task['progress']}%"
                    ))
        except FileNotFoundError:
            messagebox.showinfo("Info", "Tidak ada tugas yang tersedia.")

    def update_progress(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih tugas yang akan diperbarui!")
            return

        new_progress = simpledialog.askinteger("Update Progress", "Masukkan progress baru (0-100):", minvalue=0, maxvalue=100)
        if new_progress is not None:
            item_values = self.tree.item(selected_item[0])['values']
            for task in self.tasks:
                if (task['matkul'] == item_values[0] and
                        task['deskripsi'] == item_values[1] and
                        task['tenggat'] == item_values[2]):
                    task['progress'] = new_progress
                    break

            # Save updated tasks back to file
            self.save_tasks()

            # Update the treeview
            self.tree.item(selected_item[0], values=(
                item_values[0],
                item_values[1],
                item_values[2],
                item_values[3],
                f"{new_progress}%"
            ))

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih tugas yang akan dihapus!")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus tugas ini?")
        if confirm:
            item_values = self.tree.item(selected_item[0])['values']
            for task in self.tasks:
                if (task['matkul'] == item_values[0] and
                        task['deskripsi'] == item_values[1] and
                        task['tenggat'] == item_values[2]):
                    self.tasks.remove(task)
                    break

            # Save updated tasks back to file
            self.save_tasks()

            # Remove the item from the treeview
            self.tree.delete(selected_item[0])

    def save_tasks(self):
        try:
            with open("tasks.json", "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saat menyimpan tugas: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskListApp(root, "username")  #