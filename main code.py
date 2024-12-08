import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog, scrolledtext  # Tambahkan scrolledtext di sini
import datetime
import json
from tkcalendar import Calendar
import threading
import time
import os
from tkinter import Canvas
from PIL import Image, ImageTk  

class UserAuthApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("   ")
        self.root.geometry("400x600")
    
        self.users_file = "users.json"

        self.create_main_widgets()

    def create_main_widgets(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Sesuaikan ukuran jendela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 
        
        # Hitung 100% dari lebar dan tinggi layar
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Load gambar
        self.bg_image= Image.open("12.png")  # Ganti dengan path gambar Anda
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        # Buat canvas untuk menampilkan gambar latar belakang
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Tambahkan gambar latar belakang ke canvas
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
     
        # Log In Button
        login_button = tk.Button(self.root, text="Log In Now", 
                                 command=self.show_login_page,
                                 font=("Helvetica", 14), 
                                 bg="#4CAF50", fg="white", 
                                 relief=tk.FLAT, 
                                 padx=5, pady=5)
        login_button.place(x=screen_width//2 - 150, y=screen_height//2)

        # Sign Up Button
        signup_button = tk.Button(self.root, text="Sign Up Now", 
                                  command=self.show_register_page,
                                  font=("Helvetica", 14), 
                                  bg="#2196F3", fg="white", 
                                  relief=tk.FLAT, 
                                  padx=5, pady=5)
        signup_button.place(x=screen_width//2 + 50, y=screen_height//2)

    def show_login_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Sesuaikan ukuran jendela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 
        
        # Load gambar
        self.bg_image= Image.open("19.png")  # Ganti dengan path gambar Anda
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        # Buat canvas untuk menampilkan gambar latar belakang
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Tambahkan gambar latar belakang ke canvas
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#17224d", relief=tk.RAISED)  # Tambahkan border untuk memperjelas
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=400)  # Atur posisi dan ukuran frame

        # Back Button
        back_button = tk.Button(main_frame, text="← Back", 
                                command=self.create_main_widgets,
                                font=("Helvetica", 12, "bold"), 
                                bg="#17224d", fg="#ffffff", 
                                relief=tk.FLAT)
        back_button.pack(anchor='w', pady=(0, 20))

        # Title
        title_label = tk.Label(main_frame, text="Log In", 
                               font=("Helvetica", 24, "bold"), 
                               fg="#ffffff", bg="#17224d")
        title_label.pack(pady=(0, 30))

        # Username Entry
        username_frame = tk.Frame(main_frame, bg="#17224d")
        username_frame.pack(fill='x', pady=10)
        
        username_label = tk.Label(username_frame, text="Username", 
                                  font=("Helvetica", 12, "bold"), 
                                  bg="#17224d", fg="#ffffff")
        username_label.pack(anchor='w')
        
        self.login_username = tk.Entry(username_frame, 
                                       font=("Helvetica", 14), 
                                       bg="#f0f0f0", 
                                       relief=tk.FLAT, 
                                       width=30)
        self.login_username.pack(fill='x', ipady=8)
        
        # Password Entry
        password_frame = tk.Frame(main_frame, bg="#17224d")
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password", 
                                  font=("Helvetica", 12, "bold"), 
                                  bg="#17224d", fg="#ffffff")
        password_label.pack(anchor='w')
        
        self.login_password = tk.Entry(password_frame, 
                                       show='*', 
                                       font=("Helvetica", 14), 
                                       bg="#f0f0f0", 
                                       relief=tk.FLAT, 
                                       width=30)
        self.login_password.pack(fill='x', ipady=8)

        # Login Button
        login_button = tk.Button(main_frame, text="Log In", 
                         command=self.login_user,
                         font=("Helvetica", 14), 
                         bg="#4CAF50", fg="white", 
                         relief=tk.FLAT, padx=20, pady=10)
        login_button.pack(fill='x', pady=10)         

    def go_to_dashboard_from_login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)

            if username in users and users[username] == password:
                self.root.destroy()
                dashboard_root = tk.Tk()
                DashboardApp(dashboard_root, username)
                dashboard_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except FileNotFoundError:
            messagebox.showerror("Error", "User  database not found. Please register first.")

    def show_register_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Sesuaikan ukuran jendela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 
        
        # Load gambar
        self.bg_image= Image.open("19.png")  # Ganti dengan path gambar Anda
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        # Buat canvas untuk menampilkan gambar latar belakang
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Tambahkan gambar latar belakang ke canvas
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#17224d", relief=tk.RAISED)  # Tambahkan border untuk memperjelas
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=400)  # Atur posisi dan ukuran frame

        # Back Button
        back_button = tk.Button(main_frame, text="← Back", 
                                command=self.create_main_widgets,
                                font=("Helvetica", 12, "bold"), 
                                bg="#17224d", fg="#ffffff", 
                                relief=tk.FLAT)
        back_button.pack(anchor='w', pady=(0, 20))

        # Title
        title_label = tk.Label(main_frame, text="Sign Up", 
                               font=("Helvetica", 24, "bold"), 
                               fg="#ffffff", bg="#17224d")
        title_label.pack(pady=(0, 30))

        # Username Entry
        username_frame = tk.Frame(main_frame, bg="#17224d")
        username_frame.pack(fill='x', pady=10)
        
        username_label = tk.Label(username_frame, text="Username", 
                                  font=("Helvetica", 12), 
                                  bg="#17224d", fg="#ffffff")
        username_label.pack(anchor='w')
        
        self.reg_username = tk.Entry(username_frame, 
                                     font=("Helvetica", 14), 
                                     bg="#f0f0f0", 
                                     relief=tk.FLAT, 
                                     width=30)
        self.reg_username.pack(fill='x', ipady=8)
        
        # Password Entry
        password_frame = tk.Frame(main_frame, bg="#17224d")
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password", 
                                  font=("Helvetica", 12), 
                                  bg="#17224d", fg="#ffffff")
        password_label.pack(anchor='w')
        
        self.reg_password = tk.Entry(password_frame, 
                                     show='*', 
                                     font=("Helvetica", 14), 
                                     bg="#f0f0f0", 
                                     relief=tk.FLAT, 
                                     width=30)
        self.reg_password.pack(fill='x', ipady=8)

        # Register Button
        register_button = tk.Button(main_frame, text="Sign Up", 
                                    command=self.register_user,
                                    font=("Helvetica", 14), 
                                    bg="#2196F3", fg="white", 
                                    relief=tk.FLAT, 
                                    padx=20, pady=10)
        register_button.pack(fill='x', pady=20)


    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        # Di sini Anda biasanya akan memeriksa apakah nama pengguna sudah ada dan mengisi kata sandi. Sebagai contoh, kita akan menganggap pendaftaran berhasil jika kedua kolom terisi.

        if username and password:
            # Simpan data pengguna ke file users.json
            try:
                if os.path.exists(self.users_file):
                    with open(self.users_file, "r") as f:
                        users = json.load(f)
                else:
                    users = {}

                if username in users:
                    messagebox.showerror("Error", "Username sudah terdaftar!")
                else:
                    users[username] = password  # Menyimpan Username dan Password
                    with open(self.users_file, "w") as f:
                        json.dump(users, f)

                    messagebox.showinfo("Success", "Registrasi Berhasil!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error! Terjadi Kesalahan: {e}")
        else:
            messagebox.showerror("Error", "Harap masukkan username dan password dengan benar!")

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        # Validate login
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)

            if username in users and users[username] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.go_to_dashboard_from_login()  # Redirect to dashboard
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Database pengguna tidak ditemukan. Harap Sign In terlebih dahulu.!")
        
        
class DashboardApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Dashboard - {username}")
        self.root.geometry("400x500")
        
        self.create_dashboard()

    def create_dashboard(self):
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
        logout_button.place(relx=0.35, rely=0.85, anchor='center', width=100, height=50)  # Center the frame

        # Tambahkan tombol Selesai
        selesai_button = ttk.Button(self.root, text="Selesai", command=self.selesai_program)
        selesai_button.place(relx=0.65, rely=0.85, anchor='center', width=100, height=50)  # Geser ke kanan sedikit

    def selesai_program(self):
        # Konfirmasi sebelum menutup program
        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mengakhiri program?")
        if konfirmasi:
            self.root.quit()  # Menutup window saat ini
            self.root.destroy()  # Memastikan window ditutup
            exit()  # Keluar dari program secara keseluruhan
            
    def open_add_task(self):
        self.root.destroy()
        root_task = tk.Tk()
        root_task.attributes('-fullscreen', True)
        root_task.overrideredirect(True)
        
        task_app = AplikasiPengingatTugas(root_task, self.username)
        root_task.mainloop()
    
    def open_task_list(self):
        # Create a new window to show task list
        task_list_window = tk.Toplevel(self.root)
        task_list_window.title("Daftar Tugas")
        screen_width = task_list_window.winfo_screenwidth()
        screen_height = task_list_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        task_list_window.geometry(f"{window_width}x{window_height}")
        task_list_window.configure(bg="#17224d") 
        
        # Create Back Button
        back_button = ttk.Button(task_list_window, text="Kembali ke Dashboard", 
                                command=task_list_window.destroy)
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
                for task in tasks:
                    if (task['matkul'] == item_values[0] and 
                        task['deskripsi'] == item_values[1] and 
                        task['tenggat'] == item_values[2]):
                        task['progress'] = new_progress
                        break
                
                with open("tasks.json", "w") as f:
                    json.dump(tasks, f, indent=4)
                
                # Refresh treeview
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

        # Optional: You can also add a refresh button to reload tasks from the file
        def refresh_tasks():
            # Clear existing items in the treeview
            for item in tree.get_children():
                tree.delete(item)

            # Load tasks again
            try:
                with open("tasks.json", "r") as f:
                    tasks = json.load(f)
                    for task in tasks:
                        tree.insert('', 'end', values=(
                            task['matkul'], task['deskripsi'], task['tenggat'], 
                            task['prioritas'], f"{task['progress']}%"
                        ))
            except FileNotFoundError:
                messagebox.showinfo("Info", "Tidak ada tugas yang tersedia.")

    

    def open_task_history(self):
        # Create a new window to show task history
        task_history_window = tk.Toplevel(self.root)
        screen_width = task_history_window.winfo_screenwidth()
        screen_height = task_history_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        task_history_window.geometry(f"{window_width}x{window_height}")
        task_history_window.title("Riwayat Tugas")
        task_history_window.configure(bg='#17224d')
        
        # Create Back Button
        back_button = ttk.Button(task_history_window, text="Kembali ke Dashboard", 
                                command=task_history_window.destroy)
        back_button.pack(pady=10)
        
        # Create Treeview to show task history
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Status')
        tree = ttk.Treeview(task_history_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Load tasks and filter completed or overdue tasks
        try:
            with open("tasks.json", "r") as f:
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
        summary_window = tk.Toplevel(self.root)
        screen_width = summary_window.winfo_screenwidth()
        screen_height = summary_window.winfo_screenheight()
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 1)
        summary_window.geometry(f"{window_width}x{window_height}")
        summary_window.title("Tambah Rangkuman Tugas")
        summary_window.configure(bg='#17224d')
        
        # Create Back Button
        back_button = ttk.Button(summary_window, text="Kembali ke Dashboard", 
                                command=summary_window.destroy)
        back_button.pack(pady=10)
        
        # Create Treeview to show tasks for summary
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas', 'Rangkuman')
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
        app = UserAuthApp(root)
        root.mainloop()


class AplikasiPengingatTugas:
    def __init__(self, akar, username):
        self.username = username
        self.akar = akar
        self.akar.title("Tambah Tugas")
        self.akar.geometry("800x600")
        
        style = ttk.Style()
        style.configure('TLabel',
                    background='#17224d', 
                    foreground='white', 
                    font=('Helvetica', 16, 'bold'))
        
        # Font settings
        self.font_judul = font.Font(family="Helvetica", size=14, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=10)
        self.font_entry = font.Font(family="Helvetica", size=10)
        
        # Background color
        self.akar.configure(bg="#17224d")
        
        self.daftar_tugas = []
        self.muat_tugas()
        self.siapkan_antarmuka()
        
        self.thread_pengingat = threading.Thread(target=self.cek_pengingat, daemon=True)
        self.thread_pengingat.start()
        
      
    def siapkan_antarmuka(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#17224d")
        
        # Buat bingkai utama dengan latar belakang
        bingkai_utama = ttk.Frame(self.akar, padding="10", style="Custom.TFrame")
        bingkai_utama.pack(fill="both", expand=True)

        # Tombol Kembali ke Dashboard
        tombol_kembali = ttk.Button(bingkai_utama, text="Kembali ke Dashboard", command=self.kembali_ke_dashboard)
        tombol_kembali.grid(row=0, column=0, pady=10, sticky='w')

        # Judul aplikasi
        judul = tk.Label(bingkai_utama, text="Tambah Tugas Kuliah", font=self.font_judul, bg="#17224d", fg='white')
        judul.grid(row=1, column=0, columnspan=2, pady=10)

        # Input untuk Mata Kuliah
        ttk.Label(bingkai_utama, text="Mata Kuliah:", font=self.font_label).grid(row=2, column=0, pady=5, sticky='w')
        self.entri_matkul = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_matkul.grid(row=2, column=1, pady=5, sticky='ew')

        # Input untuk Deskripsi Tugas
        ttk.Label(bingkai_utama, text="Deskripsi Tugas:", font=self.font_label).grid(row=3, column=0, pady=5, sticky='w')
        self.entri_deskripsi = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_deskripsi.grid(row=3, column=1, pady=5, sticky='ew')

        # Input untuk Tenggat Waktu
        ttk.Label(bingkai_utama, text="Tenggat Waktu:", font=self.font_label).grid(row=4, column=0, pady=5, sticky='w')
        self.kalender = Calendar(bingkai_utama, selectmode='day', date_pattern='y-mm-dd')
        self.kalender.grid(row=4, column=1, pady=5, sticky='ew')

        # Input untuk Prioritas
        ttk.Label(bingkai_utama, text="Prioritas:", font=self.font_label).grid(row=5, column=0, pady=5, sticky='w')
        self.var_prioritas = tk.StringVar()
        self.combo_prioritas = ttk.Combobox(bingkai_utama, textvariable=self.var_prioritas, font=self.font_entry)
        self.combo_prioritas['values'] = ('Tinggi', 'Sedang', 'Rendah')
        self.combo_prioritas.grid(row=5, column=1, pady=5, sticky='ew')
        self.combo_prioritas.set('Sedang')

        # Input untuk Progress
        ttk.Label(bingkai_utama, text="Progress (%):", font=self.font_label).grid(row=6, column=0, pady=5, sticky='w')
        self.var_progress = tk.StringVar(value="0")
        self.entri_progress = ttk.Entry(bingkai_utama, textvariable=self.var_progress, font=self.font_entry)
        self.entri_progress.grid(row=6, column=1, pady=5, sticky='ew')

        # Tombol untuk Menambah Tugas
        add_task_button = ttk.Button(bingkai_utama, text="Tambah Tugas", command=self.tambah_tugas, style='TButton')
        add_task_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Atur agar kolom kedua (kolom input) mengisi ruang yang tersedia
        bingkai_utama.columnconfigure(1, weight=1)

        # Atur agar baris dan kolom lainnya tidak mengubah ukuran
        for i in range(8):
            bingkai_utama.rowconfigure(i, weight=0)
        bingkai_utama.rowconfigure(7, weight=1)  # Tombol tambah tugas di baris terakhir 
    
    def tambah_tugas(self):
        matkul = self.entri_matkul.get()
        deskripsi = self.entri_deskripsi.get()
        tenggat = self.kalender.get_date()
        prioritas = self.combo_prioritas.get()
        progress = self.entri_progress.get()
        
        # Validasi prioritas
        prioritas_valid = ['Tinggi', 'Sedang', 'Rendah']
        if prioritas not in prioritas_valid:
            messagebox.showerror("Error", "Prioritas hanya boleh Tinggi, Sedang, atau Rendah!")
            return
        
        print("Mata Kuliah:", matkul)
        print("Deskripsi:", deskripsi)
        print("Tenggat:", tenggat)
        print("Prioritas:", prioritas)
        print("Progress:", progress)
        
        # Validasi: Mata Kuliah tidak boleh hanya angka
        if matkul.isdigit():
            messagebox.showerror("Error", "Mata Kuliah tidak boleh hanya angka!")
            return
        
        try:
            progress = int(progress)        
        except ValueError:
            messagebox.showerror("Error", "Progress harus berupa angka!")
            return

        # Validasi: Tenggat waktu harus lebih dari hari ini
        tanggal_sekarang = datetime.datetime.now().date()
        tanggal_tenggat = datetime.datetime.strptime(tenggat, '%Y-%m-%d').date()

        if tanggal_tenggat <= tanggal_sekarang:
            messagebox.showerror("Error", "Tenggat waktu harus lebih dari hari ini!")
            return

        if not (0 <= progress <= 100):
            messagebox.showerror("Error", "Progress harus antara 0 dan 100!")
            return
    
        # Validasi: Semua field harus diisi
        if not all([matkul, deskripsi]):
            messagebox.showerror("Error", "Mata Kuliah dan Deskripsi harus diisi!")
            return

        tugas = {
            'username': self.username,
            'matkul': str(matkul),
            'deskripsi': str(deskripsi),
            'tenggat': tenggat,
            'prioritas': prioritas,
            'progress': int(progress)
        }

        self.daftar_tugas.append(tugas)
        self.simpan_tugas()
        
        # Tambahkan messagebox konfirmasi
        messagebox.showinfo("Sukses", "Tugas berhasil ditambahkan!")
        self.perbarui_daftar_tugas()
        self.bersihkan_form()
        
    def kembali_ke_dashboard(self):
        self.akar.destroy()
        root_dashboard = tk.Tk()
        DashboardApp(root_dashboard, self.username)  
        root_dashboard.mainloop()    

    def perbarui_progress(self):
        item_terpilih = self.pohon.selection()
        if not item_terpilih:
            messagebox.showerror("Error", "Pilih tugas yang akan diperbarui!")
            return

        item = self.pohon.item(item_terpilih)
        index = self.cari_tugas_berdasarkan_nilai(item['values'])

        if index is not None:
            progress = self.entri_progress.get()

            try:
                progress = int(progress)
            except ValueError:
                messagebox.showerror("Error", "Progress harus berupa angka!")
                return

            if not (0 <= progress <= 100):
                messagebox.showerror("Error", "Progress harus antara 0 dan 100!")
                return

            self.daftar_tugas[index]['progress'] = progress
            
            # Jika progress 100%, tambahkan ke riwayat tugas
            if progress == 100:
                self.add_to_task_history(self.daftar_tugas[index])
                del self.daftar_tugas[index]  # Hapus tugas dari daftar
            self.simpan_tugas()
            self.perbarui_daftar_tugas()
            self.bersihkan_form()
        else:
            messagebox.showerror("Error", "Tugas tidak ditemukan!")

    def add_to_task_history(self, task):
        # Simpan tugas ke riwayat tugas
        try:
            if os.path.exists("task_history.json"):
                with open("task_history.json", "r") as f:
                    history = json.load(f)
            else:
                history = []

            history.append({
                'matkul': task['matkul'],
                'deskripsi': task['deskripsi'],
                'tenggat': task['tenggat'],
                'status': "Tugas telah selesai"
            })

            with open("task_history.json", "w") as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saat menyimpan riwayat tugas: {e}")
            
        else:
            messagebox.showerror("Error", "Tugas tidak ditemukan!")

    def hapus_tugas(self):
        item_terpilih = self.pohon.selection()
        if not item_terpilih:
            messagebox.showerror("Error", "Pilih tugas yang akan dihapus!")
            return

        item = self.pohon.item(item_terpilih)
        index = self.cari_tugas_berdasarkan_nilai(item['values'])

        if index is not None:
            del self.daftar_tugas[index]
            self.simpan_tugas()
            self.perbarui_daftar_tugas()
            self.bersihkan_form()
        else:
            messagebox.showerror("Error", "Tugas tidak ditemukan!")

    def cari_tugas_berdasarkan_nilai(self, nilai):
        for i, tugas in enumerate(self.daftar_tugas):
            if (tugas['matkul'] == nilai[0] and 
                tugas['deskripsi'] == nilai[1] and 
                tugas['tenggat'] == nilai[2]):
                return i
        return None

    def bersihkan_form(self):
        self.entri_matkul.delete(0, tk.END)
        self.entri_deskripsi.delete(0, tk.END)
        self.var_progress.set("0")
        self.var_prioritas.set('Sedang')

    def perbarui_daftar_tugas(self):
        for item in self.pohon.get_children():
            self.pohon.delete(item)
        
        for tugas in sorted(self.daftar_tugas, key=lambda x: (self.nilai_prioritas(x['prioritas']), x['tenggat'])):
            self.pohon.insert('', tk.END, values=(
                tugas['matkul'],
                tugas['deskripsi'],
                tugas['tenggat'],
                tugas['prioritas'],
                f"{tugas['progress']}%"
            ))

    def nilai_prioritas(self, prioritas):
        peta_prioritas = {'Tinggi': 1, 'Sedang': 2, 'Rendah': 3}
        return peta_prioritas.get(prioritas, 4)

    def simpan_tugas(self):
        try:
            # Baca seluruh tugas yang ada
            with open("tasks.json", "r") as f:
                existing_tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_tasks = []
        
        # Hapus tugas untuk pengguna saat ini dari existing_tasks
        existing_tasks = [
            task for task in existing_tasks 
            if task.get('username') != self.username
        ]
        
        # Tambahkan tugas baru untuk pengguna saat ini
        existing_tasks.extend(self.daftar_tugas)
        
        # Simpan kembali ke file
        with open("tasks.json", "w") as f:
            json.dump(existing_tasks, f, indent=4)

    def muat_tugas(self):
        if os.path.exists("tasks.json"):  # Periksa apakah file tasks.json ada
            with open("tasks.json", "r") as f:
                data = f.read().strip()  # Baca isi file dan hapus spasi
                if data:  # Jika file tidak kosong
                    try:
                        # Baca seluruh tugas dari file
                        with open("tasks.json", "r") as f:
                            all_tasks = json.load(f)
                        
                        # Filter tugas untuk username saat ini
                        self.daftar_tugas = [
                            tugas for tugas in all_tasks 
                            if tugas.get('username') == self.username
                        ]
                    except (FileNotFoundError, json.JSONDecodeError):
                        # Jika file tidak ditemukan atau error parsing, inisialisasi daftar tugas kosong
                        self.daftar_tugas = []
                else:
                    self.daftar_tugas = []  # Jika file kosong, gunakan daftar kosong
        else:
            self.daftar_tugas = []  # Jika file tidak ada, gunakan daftar kosong

    def cek_pengingat(self):
        while True:
            tanggal_sekarang = datetime.datetime.now().date()
            for tugas in self.daftar_tugas:
                tenggat = datetime.datetime.strptime(tugas['tenggat'], '%Y-%m-%d').date()
                sisa_hari = (tenggat - tanggal_sekarang).days
                
                if sisa_hari <= 3 and tugas['progress'] < 100:
                    prioritas = tugas['prioritas']
                    if (prioritas == 'Tinggi' and sisa_hari <= 3) or \
                       (prioritas == 'Sedang' and sisa_hari <= 2) or \
                       (prioritas == 'Rendah' and sisa_hari <= 1):
                        messagebox.showwarning(
                            "Pengingat!",
                            f"Tugas {tugas['matkul']}: {tugas['deskripsi']}\n"
                            f"Tenggat dalam {sisa_hari} hari!\n"
                            f"Progress: {tugas['progress']}%"
                        )
                        
            time.sleep(3600)  # Cek setiap jam
    
if __name__ == '__main__':
    root = tk.Tk()
    app = UserAuthApp(root)
    root.mainloop()
    
    
    