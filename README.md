Tugas Membuat Aplikasi 
# Kelas A, Kelompok 9.
# Daftar Anggota Kelompok:
1. I0324006, Fadzli Fiyannuba, [FadzliFiyannuba](https://github.com/FadzliFiyannuba)
2. I0324018, Luthfia Amanda, [Luthfia17](https://github.com/Luthfia17)
3. I0324041, Danial Ghazi Arsyad, [Danialghazia](https://github.com/Danialghazia)

# Judul Tugas:
Aplikasi Reminder Tugas 

# Deskripsi singkat tugas:
Aplikasi yang berfungsi sebagai reminder tugas atau pekerjaan yang sedang atau akan dilakukan. ⁠Program ini akan mengingatkan pengguna untuk sisa deadline tugas yang kita input. Program ini berbasis dekstop yang menggunakan bantuan database .json

# Fitur-Fitur Aplikasi: 
1. Aplikasi ini memungkinkan pengguna untuk menginput Matkul Tugas, Deskripsi Tugas, Deadline Tugas, Skala Prioritas Tugas, dan Progress Tugas.
2. Data-data tugas yang sudah diinput oleh pengguna akan tersimpan ke database .json sehingga data akan terus tersimpan setiap pengguna menginput/mengupdate progress tugas.
3. Aplikasi akan otomatis memberi reminder deadline tugas yang sudah di input setiap pengguna mengrun aplikasi.
4. Aplikasi akan mengurutkan Tugas berdasarkan skala prioritas, deadline, dan progress nya.
5. Aplikasi ini memungkinkan pengguna untuk mengupdate progress tugas dan memberikan deskripsi lanjutan (notes) pada tugas yang sudah dikerjakan.
6. Aplikasi ini dapat menambahkan materi rangkuman untuk menunjang pengerjaan tugas yang di input.
7. Aplikasi dapat menampilkan riwayat tugas yang sudah diselesaikan pengguna ataupun ketika tugas telah selesai dikerjakan

# Library
1. Tkinter.
2. Datetime.
3. Tkcalendar.
4. Threading.
5. .JSON
6. Time.
7. Pillow.
8. OS.

# Site Map
![Site Map](https://github.com/user-attachments/assets/6cbb5a2a-ceb1-4815-a782-3ba3bab21b41)

# Flowchart
![Flowchart drawio](https://github.com/user-attachments/assets/5d50d945-b61d-4ad7-a1b8-c017be748293)

# Flowchart Revisi 1
![Flowchart new](https://github.com/user-attachments/assets/5b050668-dab6-4496-a826-42ae485f6302)


# Flowchart Fix
![Flowchart fix (3)](https://github.com/user-attachments/assets/ab071d32-794d-4f44-b34b-95640d021fae)

# Deskripsi Flowchart
Diagram alir di atas menjelaskan bagaimana alur kerja dari sebuah Aplikasi Pengingat Tugas yang bernama "Remind Me". Ketika pengguna menjalankan aplikasi ini, program akan mengarahkan pengguna ke Halaman Register. Jika pengguna belum memiliki akun, pengguna diwajibkan melakukan Sign Up atau membuat akun terlebih dahulu dengan mengisi username dan password. Setelah registrasi berhasil, pengguna menuju ke halaman login untuk mengakses akun yang sudah terdaftar dengan mengisi username dan password. Jika berhasil login, program mengarahkan pengguna menuju halaman dashboard yang berisi 4 menu utama, yang berarti data pengguna sudah terbaca di database json. Dan jika tidak berhasil login, berarti username atau password yang diinput pengguna tidak sesuai atau terdaftar pada database.
Pada menu dashboard terdiri 4 menu utama, yaitu : 
1.Tambah tugas : Pada menu ini pengguna ditampilkan halaman untuk menginput data tugas. Pengguna dapat menginput tugas dengan mengisi (matkul, deskripsi tugas, tenggat waktu, prioritas tugas yang terdiri dari rendah; sedang; dan tinggi, dan progress tugas. Setelah menambahkan tugas, tugas berhasil disimpan di database. Jika ingin keluar dari menu halaman tambah tugas, pengguna bisa menekan tombol “kembali ke dashboard” dan jika tidak ingin keluar dari menu, maka pengguna masih berada di tampilan halaman menu tambah tugas. 
2.Daftar tugas : Pada menu ini pengguna diperlihatkan daftar tugas yang sudah diinput sebelumnya di menu daftar tugas. Selain itu, pengguna juga bisa menyortir tugas mereka berdasarkan skala prioritas, deadline, dan progress tugas. Pengguna juga bisa memperbarui progress tugas dan menghapus tugas yang ingin dihapus. Jika ingin keluar dari menu daftar tugas, pengguna bisa menekan tombol “kembali ke dashboard” dan jika tidak ingin keluar dari menu, maka pengguna masih berada di tampilan halaman menu daftar tugas. 
3.Riwayat tugas : Pada menu ini pengguna diperlihatkan tampilan daftar status tugas yang sudah selesai berdasarkan progress tugas 100% dan status tugas yang sudah melewati deadline. 
4.Tambah rangkuman : Pada menu ini pengguna diperlihatkan tampilan untuk menginput rangkuman dengan memilih tugas yang ada. Tambah rangkuman di sini berfungsi agar jika kita menambahkan tugas bisa menambahkan materi dari tugas tersebut. Setelah menambahkan rangkuman tugas, tugas berhasil disimpan di database. Jika ingin keluar dari menu halaman tambah rangkuman, pengguna bisa menekan tombol “kembali ke dashboard” dan jika tidak ingin keluar dari menu, maka pengguna masih berada di tampilan halaman menu tambah rangkuman. 
Jika sudah tidak ada menu yang dipilih, maka pengguna bisa menekan button logout untuk keluar dari program tersebut. 



