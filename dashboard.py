import json
import datetime
import tkinter as tk
import user_auth as user
import task_manager as tm
from PIL import Image, ImageTk  
from tkinter import ttk, messagebox
from tkinter import ttk, messagebox, simpledialog, scrolledtext 

class DashboardApp:
    def __init__(self, root, username, x):
        self.root = root
        self.username = username
        self.root.title(f"Dashboard - {username}")
        self.root.geometry("400x500")
        self.create_dashboard(x)

    def create_dashboard(self, x):
        # Clear existing widgets
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Sesuaikan ukuran jendela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 
        
        # Hitung 90% dari lebar dan tinggi layar
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
    
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Load gambar
        self.bg_image= Image.open("13.png")  # Ganti dengan path gambar Anda
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        # Buat canvas untuk menampilkan gambar latar belakang
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Tambahkan gambar latar belakang ke canvas
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        
        # Dashboard Title
        title_label = tk.Label(self.root, text="Task Management Dashboard", 
                                font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)
        
        # Dashboard Buttons
        buttons_frame = tk.Frame(self.canvas, bg="#17224d")  # Set background color for the frame
        buttons_frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=300)  # Center the frame
        
        #Create Button
        dashboard_options = [
            ("Tambah Tugas", self.open_add_task),
            ("Daftar Tugas", self.open_task_list),
            ("Riwayat Tugas", self.open_task_history),
            ("Tambah Rangkuman", self.open_task_summary)
        ]
        
        for text, command in dashboard_options:
            button = ttk.Button(buttons_frame, text=text, command=command)
            button.pack(fill='x', pady=10)
        
        # Logout Button
        logout_button = ttk.Button(self.root, text="Logout", command=self.logout)
        logout_button.place(relx=0.5, rely=0.85, anchor='center', width=100, height=50)  # Center the frame

        if x == 0:
            try:
                with open("tasks.json", "r") as f:
                    tasks = json.load(f)
                    
                    # Filter tasks for current user
                    tasks = [
                        task for task in tasks
                        if task.get('username', '') == self.username
                    ]
                    
                    for i in range(0, len(tasks)):
                        messagebox.showinfo("Reminder", f"Mata kuliah: {tasks[i]["matkul"]}\nDeskripsi: {tasks[i]["deskripsi"]}\nPrioritas: {tasks[i]["prioritas"]}\nTenggat: {tasks[i]["tenggat"]}\nProgress: {tasks[i]["progress"]} %")
            except FileNotFoundError:
                messagebox.showinfo("Info", "Belum ada tugas!")
            
    def open_add_task(self):
        self.root.destroy()
        root_task = tk.Tk()
        root_task.attributes('-fullscreen', True)
        root_task.overrideredirect(True)
        
        tm.AplikasiPengingatTugas(root_task, self.username)
        root_task.mainloop()
    
    def open_task_list(self):
        # Create a new window to show task list
        self.root.withdraw()
        task_list_window = tk.Toplevel(self.root)
        task_list_window.title("Daftar Tugas")
        screen_width = task_list_window.winfo_screenwidth()
        screen_height = task_list_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        task_list_window.geometry(f"{window_width}x{window_height}")
        task_list_window.configure(bg="#17224d") 
        
        def back_dashboard():
            task_list_window.destroy()
            self.root.deiconify()
        
        # Create Back Button
        back_button = ttk.Button(task_list_window, text="Kembali ke Dashboard", 
                                command=back_dashboard)
        back_button.pack(pady=10)
        
        # Sorting Frame
        sorting_frame = tk.Frame(task_list_window)
        sorting_frame.pack(pady=10)
        
        # Sorting Label
        sorting_label = tk.Label(sorting_frame, text="Sortir Berdasarkan:", font=("Helvetica", 10), bg='#17224d', fg='white')
        sorting_label.pack(side=tk.LEFT)
        
        # Sorting Dropdown
        sort_var = tk.StringVar(value="Prioritas")
        sort_dropdown = ttk.Combobox(sorting_frame, textvariable=sort_var, 
                                    values=["Prioritas", "Deadline", "Progress"], 
                                    state="readonly", width=10)
        sort_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Create Treeview to show tasks
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas', 'Progress')
        tree = ttk.Treeview(task_list_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        # Load tasks
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                
                # Filter tasks for current user
                tasks = [
                    task for task in tasks
                    if task.get('username', '') == self.username
                ]
                
                def sort_tasks(tasks, sort_by):
                    with open("tasks.json", "r") as f:
                        tasks = json.load(f)
                    def prioritas_key(task):
                        prioritas_map = {'Tinggi': 1, 'Sedang': 2, 'Rendah': 3}
                        return prioritas_map.get(task['prioritas'], 4)
                    
                    if sort_by == "Prioritas":
                        return sorted(tasks, key=prioritas_key)
                    elif sort_by == "Deadline":
                        return sorted(tasks, key=lambda x: x['tenggat'])
                    elif sort_by == "Progress":
                        return sorted(tasks, key=lambda x: x['progress'], reverse=True)
                    return tasks
                
                def update_treeview():
                    # Clear existing items
                    for item in tree.get_children():
                        tree.delete(item)
                    
                    # Get current sorting method
                    current_sort = sort_var.get()
                    sorted_tasks = sort_tasks(tasks, current_sort)
                    
                    # Insert sorted tasks
                    for task in sorted_tasks:
                        tree.insert('', 'end', values=(
                            task['matkul'], task['deskripsi'], task['tenggat'], 
                            task['prioritas'], f"{task['progress']}%"
                        ))
                
                # Initial population of treeview
                update_treeview()
                
                # Bind sorting dropdown to update function
                sort_dropdown.bind('<<ComboboxSelected>>', lambda e: update_treeview())
                
                tree.pack(expand=True, fill='both', padx=10, pady=10)
            
                
        except FileNotFoundError:
            messagebox.showinfo("Info", "Tidak ada tugas yang tersedia.")
        
        tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Update Progress Button
        def update_progress():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Pilih tugas yang akan diperbarui!")
                return
            
            # Open progress update dialog
            new_progress = simpledialog.askinteger(
                "Update Progress", 
                "Masukkan progress baru (0-100):", 
                minvalue=0, maxvalue=100
            )
            
            if new_progress is not None:
                # Update task progress in file
                with open("tasks.json", "r") as f:
                    tasks = json.load(f)
                
                item_values = tree.item(selected_item[0])['values']
                task_to_update = None
                
                for task in tasks:
                    if (task['matkul'] == item_values[0] and 
                        task['deskripsi'] == item_values[1] and 
                        task['tenggat'] == item_values[2]):
                        task['progress'] = new_progress
                        task_to_update = task  # Simpan referensi tugas yang diupdate
                        break
                
                if new_progress == 100 and task_to_update:
                    # Pindahkan tugas ke riwayat
                    try:
                        with open("riwayat_tugas.json", "r") as f:
                            riwayat_tasks = json.load(f)
                    except FileNotFoundError:
                        riwayat_tasks = []  # Jika file tidak ada, buat list baru
                    
                    # Tambahkan tugas ke riwayat
                    riwayat_tasks.append(task_to_update)
                    
                    # Simpan riwayat tugas
                    with open("riwayat_tugas.json", "w") as f:
                        json.dump(riwayat_tasks, f, indent=4)
                    print("Data berhasil disimpan ke riwayat_tugas.json")
                    
                    # Hapus tugas dari daftar tugas
                    tasks.remove(task_to_update)
                    messagebox.showinfo("Sukses", "Tugas telah selesai dan dipindahkan ke riwayat tugas!")
                else:
                    messagebox.showinfo("Sukses", "Progress berhasil diperbarui!")
                
                # Simpan kembali tugas yang telah diperbarui
                with open("tasks.json", "w") as f:
                    json.dump(tasks, f, indent=4)
                
                # Refresh treeview
                if new_progress == 100:
                    tree.delete(selected_item[0])  # Hapus item dari treeview
                else:
                    tree.item(selected_item[0], values=(
                        item_values[0], item_values[1], item_values[2], 
                        item_values[3], f"{new_progress}%"
                    ))
        
        update_button = tk.Button(
            task_list_window,
            text="Perbarui Progress",
            command=update_progress,
            bg="#28a745",  # Green background
            fg="white",    # White text
            font=("Helvetica", 10)
        )
        update_button.pack(pady=10)
        
        def delete_task():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Pilih tugas yang akan dihapus!")
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus tugas ini?")
            if confirm:
                item_values = tree.item(selected_item[0])['values']
                # Remove task from memory
                for task in tasks:
                    if (task['matkul'] == item_values[0] and 
                        task['deskripsi'] == item_values[1] and 
                        task['tenggat'] == item_values[2]):
                        tasks.remove(task)
                        break
                
                # Save updated tasks back to file
                with open("tasks.json", "w") as f:
                    json.dump(tasks, f, indent=4)
                
                # Refresh treeview
                tree.delete(selected_item[0])
                
        delete_button = tk.Button(task_list_window, text="Hapus Tugas", command=delete_task, bg='#d20505', fg='white')
        delete_button.pack(pady=10)


    def open_task_history(self):
        # Create a new window to show task history
        self.root.withdraw()
        task_history_window = tk.Toplevel(self.root)
        screen_width = task_history_window.winfo_screenwidth()
        screen_height = task_history_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        task_history_window.geometry(f"{window_width}x{window_height}")
        task_history_window.title("Riwayat Tugas")
        task_history_window.configure(bg='#17224d')
        
        def back_dashboard():
            task_history_window.destroy()
            self.root.deiconify()
        
        # Create Back Button
        back_button = ttk.Button(task_history_window, text="Kembali ke Dashboard", 
                                command=back_dashboard)
        back_button.pack(pady=10)
        
        # Create Treeview to show task history
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Status')
        tree = ttk.Treeview(task_history_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Load tasks and filter completed or overdue tasks
        try:
            with open("riwayat_tugas.json", "r") as f:
                tasks = json.load(f)
                today = datetime.datetime.now().date()
                
                history_tasks = []
                for task in tasks:
                    task_date = datetime.datetime.strptime(task['tenggat'], '%Y-%m-%d').date()
                    
                    # If task is 100% complete or past deadline
                    if task['progress'] == 100 or task_date < today:
                        status = "Selesai" if task['progress'] == 100 else "Melewati Deadline"
                        history_tasks.append((
                            task['matkul'], task['deskripsi'], task['tenggat'], status
                        ))
                
                for ht in history_tasks:
                    tree.insert('', 'end', values=ht)
        except FileNotFoundError:
            messagebox.showinfo("Info", "Tidak ada riwayat tugas.")
        
        tree.pack(expand=True, fill='both', padx=10, pady=10)

    def open_task_summary(self):
        # Create a new window to add task summary
        self.root.withdraw()
        summary_window = tk.Toplevel(self.root)
        screen_width = summary_window.winfo_screenwidth()
        screen_height = summary_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        summary_window.geometry(f"{window_width}x{window_height}")
        summary_window.title("Tambah Rangkuman Tugas")
        summary_window.configure(bg='#17224d')
        
        def back_dashboard():
            summary_window.destroy()
            self.root.deiconify()
        
        # Create Back Button
        back_button = ttk.Button(summary_window, text="Kembali ke Dashboard", 
                                command=back_dashboard)
        back_button.pack(pady=10)
        
        # Create Treeview to show tasks for summary
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas')
        tree = ttk.Treeview(summary_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        # Large summary text area
        summary_frame = tk.Frame(summary_window)
        summary_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        summary_text = scrolledtext.ScrolledText(summary_frame, 
                                                 wrap=tk.WORD, 
                                                 height=15, 
                                                 font=("Helvetica", 12))
        summary_text.pack(fill='both', expand=True)
        
        # Load tasks
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                
                 # Filter tugas untuk username saat ini
                tasks = [task for task in tasks if task['username'] == self.username]
                
                    # Try to load existing summaries
                try:
                    with open("task_summaries.json", "r") as sf:
                        existing_summaries = json.load(sf)
                        # Filter rangkuman untuk username saat ini
                        existing_summaries = {k: v for k, v in existing_summaries.items() 
                                            if k.startswith(f"{self.username}_")}
                except FileNotFoundError:
                    existing_summaries = {}
                
                for task in tasks:
                    # Gunakan username sebagai prefix untuk kunci rangkuman
                    summary_key = f"{self.username}_{task['matkul']}_{task['deskripsi']}"
                    existing_summary = existing_summaries.get(summary_key, "")
                    
                    tree.insert('', 'end', values=(
                        task['matkul'], task['deskripsi'], task['tenggat'], 
                        task['prioritas'], existing_summary
                    ))
        except FileNotFoundError:
            messagebox.showinfo("Info", "Tidak ada tugas yang tersedia.")
        
        tree.pack(fill='x', padx=10, pady=10)
        
        def on_task_select(event):
            selected_item = tree.selection()
            if selected_item:
                # Get selected task details
                item_values = tree.item(selected_item[0])['values']
                summary_key = f"{item_values[0]}_{item_values[1]}"
                
                # Load existing summary if available
                try:
                    with open("task_summaries.json", "r") as f:
                        summaries = json.load(f)
                    existing_summary = summaries.get(summary_key, "")
                    summary_text.delete(1.0, tk.END)
                    summary_text.insert(tk.END, existing_summary)
                except FileNotFoundError:
                    summary_text.delete(1.0, tk.END)
        
        def save_summary():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Pilih tugas untuk ditambahkan ringkasan!")
                return
            
            # Get task details
            item_values = tree.item(selected_item[0])['values']
            summary_key = f"{item_values[0]}_{item_values[1]}"
            
            # Get summary text
            summary = summary_text.get(1.0, tk.END).strip()
            
            if summary:
                # Load or create summaries
                try:
                    with open("task_summaries.json", "r") as f:
                        summaries = json.load(f)
                except FileNotFoundError:
                    summaries = {}
                
                # Save summary
                summaries[summary_key] = summary
                
                with open("task_summaries.json", "w") as f:
                    json.dump(summaries, f, indent=4)
                
                # Update treeview
                tree.item(selected_item[0], values=(
                    item_values[0], item_values[1], item_values[2], 
                    item_values[3], summary
                ))
                
                messagebox.showinfo("Sukses", "Rangkuman berhasil disimpan!")
        
        # Bind treeview selection
        tree.bind('<<TreeviewSelect>>', on_task_select)
        
        # Save Summary Button
        save_summary_button = tk.Button(summary_window, text="Simpan Rangkuman", command=save_summary, bg='#03d030', fg='white')
        save_summary_button.pack(pady=10)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        user.UserAuthApp(root)
        root.mainloop()
