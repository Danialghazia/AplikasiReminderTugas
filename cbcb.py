import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import json
import os
from PIL import Image, ImageTk
import cbcb1  # Import the dashboard module

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication")
        self.root.geometry("1000x800")
        
        self.users_file = "users.json"
        self.create_main_widgets()

    def create_main_widgets(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Background setup
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.bg_image = Image.open("12.png")
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
     
        # Login and Signup Buttons
        login_button = tk.Button(self.root, text="Log In", 
                                 command=self.show_login_page,
                                 font=("Helvetica", 14), 
                                 bg="#4CAF50", fg="white", 
                                 relief=tk.FLAT, 
                                 padx=20, pady=10)
        login_button.place(x=screen_width//2 - 150, y=screen_height//2)

        signup_button = tk.Button(self.root, text="Sign Up", 
                                  command=self.show_register_page,
                                  font=("Helvetica", 14), 
                                  bg="#2196F3", fg="white", 
                                  relief=tk.FLAT, 
                                  padx=20, pady=10)
        signup_button.place(x=screen_width//2 + 50, y=screen_height//2)

    def show_login_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Background setup similar to main page
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.bg_image = Image.open("19.png")
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#17224d", relief=tk.RAISED)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=400)

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

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
                
                
            if username in users and users[username] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()  # Close authentication window
                root_dashboard = tk.Tk()
                cbcb1.DashboardApp(root_dashboard, username)  # Inisialisasi DashboardApp
                root_dashboard.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found. Please register first.")


    def show_register_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Background setup similar to main page
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.bg_image = Image.open("19.png")
        self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#17224d", relief=tk.RAISED)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=400)

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

        if username and password:
            try:
                if os.path.exists(self.users_file):
                    with open(self.users_file, "r") as f:
                        users = json.load(f)
                else:
                    users = {}

                if username in users:
                    messagebox.showerror("Error", "Username sudah terdaftar!")
                else:
                    users[username] = password
                    with open(self.users_file, "w") as f:
                        json.dump(users, f)

                    messagebox.showinfo("Success", "Registrasi Berhasil!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error! Terjadi Kesalahan: {e}")
        else:
            messagebox.showerror("Error", "Harap masukkan username dan password dengan benar!")
def main():
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
