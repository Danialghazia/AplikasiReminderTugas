import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog, scrolledtext  # Tambahkan scrolledtext di sini
import datetime
import json
from tkcalendar import Calendar
import threading
import time
import os

class UserAuthApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x600")
        self.root.configure(bg="#ffffff")

        self.users_file = "users.json"

        self.create_main_widgets()

    def create_main_widgets(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Logo or Title
        title_label = tk.Label(main_frame, text="Task Manager", 
                                font=("Helvetica", 24, "bold"), 
                                fg="#333333", bg="#ffffff")
        title_label.pack(pady=(20, 30))

        # Log In Button
        login_button = tk.Button(main_frame, text="Log In Now", 
                                 command=self.show_login_page,
                                 font=("Helvetica", 14), 
                                 bg="#4CAF50", fg="white", 
                                 relief=tk.FLAT, 
                                 padx=20, pady=10)
        login_button.pack(fill='x', pady=10)

        # Sign Up Button
        signup_button = tk.Button(main_frame, text="Sign Up Now", 
                                  command=self.show_register_page,
                                  font=("Helvetica", 14), 
                                  bg="#2196F3", fg="white", 
                                  relief=tk.FLAT, 
                                  padx=20, pady=10)
        signup_button.pack(fill='x', pady=10)
        
    def show_register_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Back Button
        back_button = tk.Button(main_frame, text="← Back", 
                                command=self.create_main_widgets,
                                font=("Helvetica", 12), 
                                bg="#ffffff", fg="#333333", 
                                relief=tk.FLAT)
        back_button.pack(anchor='w', pady=(0, 20))

        # Title
        title_label = tk.Label(main_frame, text="Sign Up", 
                               font=("Helvetica", 24, "bold"), 
                               fg="#333333", bg="#ffffff")
        title_label.pack(pady=(0, 30))

        # Username Entry
        username_frame = tk.Frame(main_frame, bg="#ffffff")
        username_frame.pack(fill='x', pady=10)
        
        username_label = tk.Label(username_frame, text="Username", 
                                  font=("Helvetica", 12), 
                                  bg="#ffffff", fg="#666666")
        username_label.pack(anchor='w')
        
        self.register_user = tk.Entry(username_frame, 
                                       font=("Helvetica", 14), 
                                       bg="#f0f0f0", 
                                       relief=tk.FLAT, 
                                       width=30)
        self.register_user.pack(fill='x', ipady=8)

    def show_login_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Back Button
        back_button = tk.Button(main_frame, text="← Back", 
                                command=self.create_main_widgets,
                                font=("Helvetica", 12), 
                                bg="#ffffff", fg="#333333", 
                                relief=tk.FLAT)
        back_button.pack(anchor='w', pady=(0, 20))

        # Title
        title_label = tk.Label(main_frame, text="Log In", 
                               font=("Helvetica", 24, "bold"), 
                               fg="#333333", bg="#ffffff")
        title_label.pack(pady=(0, 30))

        # Username Entry
        username_frame = tk.Frame(main_frame, bg="#ffffff")
        username_frame.pack(fill='x', pady=10)
        
        username_label = tk.Label(username_frame, text="Username", 
                                  font=("Helvetica", 12), 
                                  bg="#ffffff", fg="#666666")
        username_label.pack(anchor='w')
        
        self.login_username = tk.Entry(username_frame, 
                                       font=("Helvetica", 14), 
                                       bg="#f0f0f0", 
                                       relief=tk.FLAT, 
                                       width=30)
        self.login_username.pack(fill='x', ipady=8)
        
        # Password Entry
        password_frame = tk.Frame(main_frame, bg="#ffffff")
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password", 
                                  font=("Helvetica", 12), 
                                  bg="#ffffff", fg="#666666")
        password_label.pack(anchor='w')
        
        self.login_password = tk.Entry(password_frame, 
                                       show='*', 
                                       font=("Helvetica", 14), 
                                       bg="#f0f0f0", 
                                       relief=tk.FLAT, 
                                       width=30)
        self.login_password.pack(fill='x', ipady=8)

        # Login Button
        login_button = tk.Button(main_frame, text="Log In Now", 
                                 command=self.go_to_dashboard_from_login,
                                 font=("Helvetica", 14), 
                                 bg="#4CAF50", fg="white", 
                                 relief=tk.FLAT, 
                                 padx=20, pady=10)
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
        
        

        # Here, you should validate the username and password
        # For now, let's assume the login is successful
        if username and password:  # You would normally check against stored user data
            self.root.destroy()
            dashboard_root = tk.Tk()
            DashboardApp(dashboard_root, username)
            dashboard_root.mainloop()
        else:
            messagebox.showerror("Error", "Please enter username and password!")

    def show_register_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Back Button
        back_button = tk.Button(main_frame, text="← Back", 
                                command=self.create_main_widgets,
                                font=("Helvetica", 12), 
                                bg="#ffffff", fg="#333333", 
                                relief=tk.FLAT)
        back_button.pack(anchor='w', pady=(0, 20))

        # Title
        title_label = tk.Label(main_frame, text="Sign Up", 
                               font=("Helvetica", 24, "bold"), 
                               fg="#333333", bg="#ffffff")
        title_label.pack(pady=(0, 30))

        # Username Entry
        username_frame = tk.Frame(main_frame, bg="#ffffff")
        username_frame.pack(fill='x', pady=10)
        
        username_label = tk.Label(username_frame, text="Username", 
                                  font=("Helvetica", 12), 
                                  bg="#ffffff", fg="#666666")
        username_label.pack(anchor='w')
        
        self.reg_username = tk.Entry(username_frame, 
                                     font=("Helvetica", 14), 
                                     bg="#f0f0f0", 
                                     relief=tk.FLAT, 
                                     width=30)
        self.reg_username.pack(fill='x', ipady=8)
        
        # Password Entry
        password_frame = tk.Frame(main_frame, bg="#ffffff")
        password_frame.pack(fill='x', pady=10)
        
        password_label = tk.Label(password_frame, text="Password", 
                                  font=("Helvetica", 12), 
                                  bg="#ffffff", fg="#666666")
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

        # Here you would typically check if the username already exists
        # and validate the password. For demonstration, we will just
        # assume registration is successful if both fields are filled.

        if username and password:
            # Save the user to the users.json file
            try:
                if os.path.exists(self.users_file):
                    with open(self.users_file, "r") as f:
                        users = json.load(f)
                else:
                    users = {}

                if username in users:
                    messagebox.showerror("Error", "Username already exists!")
                else:
                    users[username] = password  # Store the username and password
                    with open(self.users_file, "w") as f:
                        json.dump(users, f)

                    messagebox.showinfo("Success", "Registration successful!")
                    self.go_to_dashboard_from_login()  # Redirect to dashboard
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please enter username and password!")

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
            messagebox.showerror("Error", "User  database not found. Please register first.")
        

        
class DashboardApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Dashboard - {username}")
        self.root.geometry("400x500")
        
        self.create_dashboard()

    def create_dashboard(self):
        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        
        # Dashboard Title
        title_label = tk.Label(self.root, text="Task Management Dashboard", 
                                font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)
        
        # Dashboard Buttons
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(expand=True, fill='both', padx=50)
        
        dashboard_options = [
            ("Tambah Tugas", self.open_add_task),
            ("Daftar Tugas", self.open_task_list),
            ("Riwayat Tugas", self.open_task_history),
            ("Tambah Ringkasan", self.open_task_summary)
        ]
        
        for text, command in dashboard_options:
            button = ttk.Button(buttons_frame, text=text, command=command)
            button.pack(fill='x', pady=10)
        
        # Logout Button
        logout_button = ttk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(side='bottom', pady=20)

    def open_add_task(self):
        self.root.destroy()
        root_task = tk.Tk()
        task_app = AplikasiPengingatTugas(root_task)
        root_task.mainloop()

    def open_task_list(self):
        # Create a new window to show task list
        task_list_window = tk.Toplevel(self.root)
        task_list_window.title("Daftar Tugas")
        task_list_window.geometry("800x600")
        
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
                for task in tasks:
                    tree.insert('', 'end', values=(
                        task['matkul'], task['deskripsi'], task['tenggat'], 
                        task['prioritas'], f"{task['progress']}%"
                    ))
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
        
        update_button = ttk.Button(task_list_window, text="Perbarui Progress", command=update_progress)
        update_button.pack(pady=10)

    def open_task_history(self):
        # Create a new window to show task history
        task_history_window = tk.Toplevel(self.root)
        task_history_window.title("Riwayat Tugas")
        task_history_window.geometry("800x600")
        
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
        summary_window.title("Tambah Ringkasan Tugas")
        summary_window.geometry("800x800")
        
        # Create Back Button
        back_button = ttk.Button(summary_window, text="Kembali ke Dashboard", 
                                command=summary_window.destroy)
        back_button.pack(pady=10)
        
        # Create Treeview to show tasks for summary
        columns = ('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas', 'Ringkasan')
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
                
                # Try to load existing summaries
                try:
                    with open("task_summaries.json", "r") as sf:
                        existing_summaries = json.load(sf)
                except FileNotFoundError:
                    existing_summaries = {}
                
                for task in tasks:
                    # Check if summary already exists
                    summary_key = f"{task['matkul']}_{task['deskripsi']}"
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
                
                messagebox.showinfo("Sukses", "Ringkasan berhasil disimpan!")
        
        # Bind treeview selection
        tree.bind('<<TreeviewSelect>>', on_task_select)
        
        # Save Summary Button
        save_summary_button = ttk.Button(summary_window, text="Simpan Ringkasan", command=save_summary)
        save_summary_button.pack(pady=10)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = UserAuthApp(root)
        root.mainloop()

# The AplikasiPengingatTugas class remains the same as in the previous implementation
class AplikasiPengingatTugas:
    def init(self, akar):
        self.akar = akar
        self.akar.title("Tambah Tugas")
        self.akar.geometry("800x600")
        
        # Font settings
        self.font_judul = font.Font(family="Helvetica", size=14, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=10)
        self.font_entry = font.Font(family="Helvetica", size=10)
        
        # Background color
        self.akar.configure(bg="#f0f0f0")
        
        self.daftar_tugas = []
        self.muat_tugas()
        self.siapkan_antarmuka()
        
        self.thread_pengingat = threading.Thread(target=self.cek_pengingat, daemon=True)
        self.thread_pengingat.start()

    def kembali_ke_dashboard(self):
        self.akar.destroy()
        root_dashboard = tk.Tk()
        DashboardApp(root_dashboard, "Pengguna")  # You might want to pass the actual username
        root_dashboard.mainloop()

    def siapkan_antarmuka(self):
        bingkai_utama = ttk.Frame(self.akar, padding="10")
        bingkai_utama.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tombol Kembali ke Dashboard
        tombol_kembali = ttk.Button(bingkai_utama, text="Kembali ke Dashboard", command=self.kembali_ke_dashboard)
        tombol_kembali.grid(row=0, column=0, pady=10, sticky='w')
        
        # Judul aplikasi
        judul = tk.Label(bingkai_utama, text="Tambah Tugas Kuliah", font=self.font_judul, bg="#f0f0f0")
        judul.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(bingkai_utama, text="Mata Kuliah:", font=self.font_label).grid(row=2, column=0, pady=5, sticky='w')
        self.entri_matkul = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_matkul.grid(row=2, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Deskripsi Tugas:", font=self.font_label).grid(row=3, column=0, pady=5, sticky='w')
        self.entri_deskripsi = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_deskripsi.grid(row=3, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Tenggat Waktu:", font=self.font_label).grid(row=4, column=0, pady=5, sticky='w')
        self.kalender = Calendar(bingkai_utama, selectmode='day', date_pattern='y-mm-dd')
        self.kalender.grid(row=4, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Prioritas:", font=self.font_label).grid(row=5, column=0, pady=5, sticky='w')
        self.var_prioritas = tk.StringVar()
        self.combo_prioritas = ttk.Combobox(bingkai_utama, textvariable=self.var_prioritas, font=self.font_entry)
        self.combo_prioritas['values'] = ('Tinggi', 'Sedang', 'Rendah')
        self.combo_prioritas.grid(row=5, column=1, pady=5)
        self.combo_prioritas.set('Sedang')

        ttk.Label(bingkai_utama, text="Progress (%):", font=self.font_label).grid(row=6, column=0, pady=5, sticky='w')
        self.var_progress = tk.StringVar(value="0")
        self.entri_progress = ttk.Entry(bingkai_utama, textvariable=self.var_progress, font=self.font_entry)
        self.entri_progress.grid(row=6, column=1, pady=5)

        bingkai_tombol = ttk.Frame(bingkai_utama)
        bingkai_tombol.grid(row=7, column=0, columnspan=2, pady=10)
        
        style = ttk.Style()
        style.configure('TButton', font=self.font_label)
        
        ttk.Button(bingkai_tombol, text="Tambah Tugas", command=self.tambah_tugas).pack(side=tk.LEFT, padx=5)
        ttk.Button(bingkai_tombol, text="Perbarui Progress", command=self.perbarui_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(bingkai_tombol, text="Hapus Tugas", command=self.hapus_tugas).pack(side=tk.LEFT, padx=5)

        # Mengatur style untuk Treeview
        style.configure("Treeview", font=self.font_entry)
        style.configure("Treeview.Heading", font=self.font_label)

        self.pohon = ttk.Treeview(bingkai_utama, columns=('Mata Kuliah', 'Deskripsi', 'Tenggat', 'Prioritas', 'Progress'), 
                                show='headings', height=10)
        
        self.pohon.heading('Mata Kuliah', text='Mata Kuliah')
        self.pohon.heading('Deskripsi', text='Deskripsi')
        self.pohon.heading('Tenggat', text='Tenggat')
        self.pohon.heading('Prioritas', text='Prioritas')
        self.pohon.heading('Progress', text='Progress')
        
        self.pohon.grid(row=8, column=0, columnspan=2, pady=10)
        
        scrollbar = ttk.Scrollbar(bingkai_utama, orient=tk.VERTICAL, command=self.pohon.yview)
        scrollbar.grid(row=8, column=2, sticky='ns')
        self.pohon.configure(yscrollcommand=scrollbar.set)

        self.perbarui_daftar_tugas()
        
    def tambah_tugas(self):
        matkul = self.entri_matkul.get()
        deskripsi = self.entri_deskripsi.get()
        tenggat = self.kalender.get_date()
        prioritas = self.combo_prioritas.get()
        progress = self.entri_progress.get()
        
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
            'matkul': str(matkul),
            'deskripsi': str(deskripsi),
            'tenggat': tenggat,
            'prioritas': prioritas,
            'progress': int(progress)
        }

        self.daftar_tugas.append(tugas)
        self.simpan_tugas()
        self.perbarui_daftar_tugas()
        self.bersihkan_form()

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
            self.simpan_tugas()
            self.perbarui_daftar_tugas()
            self.bersihkan_form()
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
        with open("tasks.json", "w") as f:
            if self.daftar_tugas:  # Hanya simpan jika ada data
                json.dump(self.daftar_tugas, f, indent=4)
            else:
                f.write("")  # Kosongkan file jika tidak ada data

    def muat_tugas(self):
        if os.path.exists("tasks.json"):  # Periksa apakah file tasks.json ada
            with open("tasks.json", "r") as f:
                data = f.read().strip()  # Baca isi file dan hapus spasi
                if data:  # Jika file tidak kosong
                    try:
                        self.daftar_tugas = json.loads(data)
                    except json.JSONDecodeError:
                        self.daftar_tugas = []  # Jika data tidak valid, gunakan daftar kosong
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