import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime
import json
from tkcalendar import Calendar
import threading
import time
import os

class UserAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User  Authentication")
        self.root.geometry("300x250")

        self.users_file = "users.json"
        self.load_users()

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.register_tab = ttk.Frame(self.tab_control)
        self.login_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.register_tab, text='Register')
        self.tab_control.add(self.login_tab, text='Login')
        self.tab_control.pack(expand=1, fill='both')

        self.create_register_widgets()
        self.create_login_widgets()

    def create_register_widgets(self):
        ttk.Label(self.register_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.reg_username = ttk.Entry(self.register_tab)
        self.reg_username.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.register_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.reg_password = ttk.Entry(self.register_tab, show='*')
        self.reg_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.register_tab, text="Register", command=self.register_user).grid(row=2, columnspan=2, pady=10)

    def create_login_widgets(self):
        ttk.Label(self.login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.login_username = ttk.Entry(self.login_tab)
        self.login_username.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.login_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.login_password = ttk.Entry(self.login_tab, show='*')
        self.login_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.login_tab, text="Login", command=self.login_user).grid(row=2, columnspan=2, pady=10)

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
    def __init__(self, akar):
        self.akar = akar
        self.akar.title("Aplikasi Pengingat Tugas Kuliah")
        self.akar.geometry("800x600")
        
        # Mengatur font
        self.font_judul = font.Font(family="Helvetica", size=14, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=10)
        self.font_entry = font.Font(family="Helvetica", size=10)
        
        # Mengatur warna latar belakang
        self.akar.configure(bg="#f0f0f0")  # Warna latar belakang abu-abu muda
        
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
        combo_prioritas = ttk.Combobox(bingkai_utama, textvariable=self.var_prioritas, font=self.font_entry)
        combo_prioritas['values'] = ('Tinggi', 'Sedang', 'Rendah')
        combo_prioritas.grid(row=4, column=1, pady=5)
        combo_prioritas.set('Sedang')

        ttk.Label(bingkai_utama, text="Progress (%):", font=self.font_label).grid(row=5, column=0, pady=5, sticky='w')
        self.var_progress = tk.StringVar(value="0")
        self.entri_progress = ttk.Entry(bingkai_utama, textvariable=self.var_progress, font=self.font_entry)
        self.entri_progress.grid(row=5, column=1, pady=5)

        bingkai_tombol = ttk.Frame(bingkai_utama)
        bingkai_tombol.grid(row=6, column=0, columnspan=2, pady=10)
        
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

    def tambah_tugas(self):
        matkul = self.entri_matkul.get()
        deskripsi = self.entri_deskripsi.get()
        tenggat = self.kalender.get_date()
        prioritas = self.var_prioritas.get()
        progress = self.var_progress.get()

        if not all([matkul, deskripsi, tenggat, prioritas]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        tugas = {
            'matkul': matkul,
            'deskripsi': deskripsi,
            'tenggat': tenggat,
            'prioritas': prioritas,
            'progress': progress
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
            progress = self.var_progress.get()
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
        with open('tugas.json', 'w') as f:
            json.dump(self.daftar_tugas, f)

    def muat_tugas(self):
        try:
            with open('tugas.json', 'r') as f:
                self.daftar_tugas = json.load(f)
        except FileNotFoundError:
            self.daftar_tugas = []

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