import tkinter as tk
import user_auth as user
import dashboard as dash
import task_manager as tm
import reminders as rmd

# from user_auth import UserAuthApp
# from dashboard import DashboardApp
# from task_manager import AplikasiPengingatTugas
# from reminders import cek_pengingat

if __name__ == '__main__':
    root = tk.Tk()
    user.UserAuthApp(root)
    root.mainloop()