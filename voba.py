import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime
import json
from tkcalendar import Calendar
import threading
import time
import os
from PIL import Image, ImageTk
from tkinter.font import Font

class UserAuthApp:
    def _init_(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        
        self.users_file = "users.json"
        self.load_users()
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
    
        # Membuka dan menyesuaikan ukuran gambar
        bg_image = Image.open(r"SIGN UP page.png")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)
        
        # Menampilkan gambar sebagai background
        background_label = tk.Label(root, image=bg_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = bg_image  # Menyimpan referensi gambar

        self.create_widgets()

    def create_widgets(self):
        
        self.tab_control = ttk.Notebook(self.root)

        self.register_tab = ttk.Frame(self.tab_control)
        self.login_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.register_tab, text='Register')
        self.tab_control.add(self.login_tab, text='Login')
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.place(x=640, y=200, width=430, height=450)

        self.create_register_widgets()
        self.create_login_widgets()

    def create_register_widgets(self):
        
         # Username
        ttk.Label(self.register_tab, text="Username:", font=("Arial", 12)).place(x=20, y=50)
        self.reg_username = ttk.Entry(self.register_tab, font=("Arial", 12))
        self.reg_username.place(x=120, y=50, width=200)

        # Password
        ttk.Label(self.register_tab, text="Password:", font=("Arial", 12)).place(x=20, y=100)
        self.reg_password = ttk.Entry(self.register_tab, show="*", font=("Arial", 12))
        self.reg_password.place(x=120, y=100, width=200)

        # Register Button
        ttk.Button(self.register_tab, text="Register", command=self.register_user).place(x=150, y=150)

    def create_login_widgets(self):
       
        ttk.Label(self.login_tab, text="Username:", font=("Arial", 12)).place(x=20, y=50)
        self.login_username = ttk.Entry(self.login_tab, font=("Arial", 12))
        self.login_username.place(x=120, y=50, width=200)

        # Password
        ttk.Label(self.login_tab, text="Password:", font=("Arial", 12)).place(x=20, y=100)
        self.login_password = ttk.Entry(self.login_tab, show="*", font=("Arial", 12))
        self.login_password.place(x=120, y=100, width=200)

        # Login Button
        ttk.Button(self.login_tab, text="Login", command=self.login_user).place(x=150, y=150)


    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        if username in self.users:
            messagebox.showerror("Error", "Username already exists!")
            return

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields!")
            return

        self.users[username] = password
        self.save_users()
        messagebox.showinfo("Success", "User  registered successfully!")
        self.reg_username.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if username in self.users and self.users[username] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.login_username.delete(0, tk.END)
            self.login_password.delete(0, tk.END)
            akar = tk.Tk()
            AplikasiPengingatTugas(akar)
            akar.mainloop()
            
        else:
            messagebox.showerror("Error", "Invalid username or password!")

class AplikasiPengingatTugas:
    def _init_(self, akar):
        self.akar = akar
        self.akar.title("Aplikasi Pengingat Tugas Kuliah")
        self.akar.geometry("1920x1080")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
    
        # Membuka dan menyesuaikan ukuran gambar
        bg_image = Image.open(r"Halaman utama.png")
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)
        
        # Menampilkan gambar sebagai background
        background_label = tk.Label(root, image=bg_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = bg_image  # Menyimpan referensi gambar
        
        # Mengatur font
        self.font_judul = font.Font(family="Helvetica", size=14, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=10)
        self.font_entry = font.Font(family="Helvetica", size=10)
        
        # Mengatur warna latar belakang
        self.akar.configure(bg="#f0f0f0")  # Warna latar belakang biru
        
        self.daftar_tugas = []
        self.muat_tugas()
        self.siapkan_antarmuka()
        
        self.thread_pengingat = threading.Thread(target=self.cek_pengingat, daemon=True)
        self.thread_pengingat.start()

    def siapkan_antarmuka(self):
        bingkai_utama = ttk.Frame(self.akar, padding="10")
        bingkai_utama.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Judul aplikasi
        judul = tk.Label(bingkai_utama, text="Pengingat Tugas Kuliah", font=self.font_judul, bg="#f0f0f0")
        judul.grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(bingkai_utama, text="Mata Kuliah:", font=self.font_label).grid(row=1, column=0, pady=5, sticky='w')
        self.entri_matkul = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_matkul.grid(row=1, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Deskripsi Tugas:", font=self.font_label).grid(row=2, column=0, pady=5, sticky='w')
        self.entri_deskripsi = ttk.Entry(bingkai_utama, width=30, font=self.font_entry)
        self.entri_deskripsi.grid(row=2, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Tenggat Waktu:", font=self.font_label).grid(row=3, column=0, pady=5, sticky='w')
        self.kalender = Calendar(bingkai_utama, selectmode='day', date_pattern='y-mm-dd')
        self.kalender.grid(row=3, column=1, pady=5)

        ttk.Label(bingkai_utama, text="Prioritas:", font=self.font_label).grid(row=4, column=0, pady=5, sticky='w')
        self.var_prioritas = tk.StringVar()
        self.combo_prioritas = ttk.Combobox(bingkai_utama, textvariable=self.var_prioritas, font=self.font_entry)
        self.combo_prioritas['values'] = ('Tinggi', 'Sedang', 'Rendah')
        self.combo_prioritas.grid(row=4, column=1, pady=5)
        self.combo_prioritas.set('Sedang')

        ttk.Label(bingkai_utama, text="Progress (%):", font=self.font_label).grid(row=5, column=0, pady=5, sticky='w')
        self.var_progress = tk.StringVar(value="0")
        self.entri_progress = ttk.Entry(bingkai_utama, textvariable=self.var_progress, font=self.font_entry)
        self.entri_progress.grid(row=5, column=1, pady=5)

        bingkai_tombol = ttk.Frame(bingkai_utama)
        bingkai_tombol.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Tombol Logout
        ttk.Button(bingkai_utama, text="Logout", command=self.logout).grid(row=8, column=0, columnspan=2, pady=10)
        
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
        
        self.pohon.grid(row=7, column=0, columnspan=2, pady=10)
        
        scrollbar = ttk.Scrollbar(bingkai_utama, orient=tk.VERTICAL, command=self.pohon.yview)
        scrollbar.grid(row=7, column=2, sticky='ns')
        self.pohon.configure(yscrollcommand=scrollbar.set)

        self.perbarui_daftar_tugas()
        
    def logout(self):
        self.akar.destroy()  # Menutup jendela pengingat tugas
        root = tk.Tk()  # Membuka kembali jendela login
        app = UserAuthApp(root)
        root.mainloop()

    def tambah_tugas(self):
        matkul = self.entri_matkul.get()
        deskripsi = self.entri_deskripsi.get()
        tenggat = self.kalender.get_date()
        prioritas = self.combo_prioritas.get()  # Ambil nilai prioritas
        progress = self.entri_progress.get()    # Ambil nilai progress
        
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
    
        # Debugging nilai variabel
        print(f"Matkul: {matkul}, Deskripsi: {deskripsi}, Tenggat: {tenggat}, Prioritas: {prioritas}, Progress: {progress}")

        # Validasi: Semua field harus diisi
        # if not all([matkul, deskripsi, tenggat, prioritas]):
        #     messagebox.showerror("Error", "Semua field harus diisi!")
        #     return

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
                progress = int(progress)  # Ensure the progress is an integer
            except ValueError:
                messagebox.showerror("Error", "Progress harus berupa angka!")
                return

            if not (0 <= progress <= 100):
                messagebox.showerror("Error", "Progress harus antara 0 dan 100!")
                return

            self.daftar_tugas[index]['progress'] = progress  # Update progress tugas
            print(f"Progress yang baru: {self.daftar_tugas[index]['progress']}")  # Log progress baru
            self.simpan_tugas()  # Simpan perubahan ke dalam file JSON
            self.perbarui_daftar_tugas()  # Refresh daftar tugas yang ditampilkan
            self.bersihkan_form()  # Kosongkan form input setelah pembaruan
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
                
                if sisa_hari <= 3 and tugas['progress'] != '100':
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