import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog, scrolledtext  # Tambahkan scrolledtext di sini
import datetime
import json
import dashboard as dash
from tkcalendar import Calendar
import threading
import time
import os
from tkinter import Canvas
from PIL import Image, ImageTk 

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
        dash.DashboardApp(root_dashboard, self.username)  
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