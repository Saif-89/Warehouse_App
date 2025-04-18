import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import subprocess
import sys
import os

REMEMBER_ME_FILE = "remember_me.txt"

class LoginApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Entrepôt Brahem - Admin Login")
        ctk.set_appearance_mode("light")
        
        # Admin credentials
        self.ADMIN_USERNAME = "brahem"
        self.ADMIN_PASSWORD = "brahem"
        
        # Variables
        self.dark_mode = ctk.IntVar(value=0)
        self.remember_me = ctk.IntVar(value=0)
        
        # Load_credentials
        self.load_remembered_credentials()
        
        #UI
        self.create_widgets()
        self.app.mainloop()
    
    def load_remembered_credentials(self):
        """Load saved credentials from file"""
        if os.path.exists(REMEMBER_ME_FILE):
            try:
                with open(REMEMBER_ME_FILE, "r") as f:
                    lines = f.read().splitlines()
                    if len(lines) >= 2:
                        self.saved_username = lines[0]
                        self.saved_password = lines[1]
                        self.remember_me.set(1)
            except Exception as e:
                print(f"Error loading credentials: {e}")

    def create_widgets(self):
        """Create login interface"""
        main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        main_frame.pack(pady=50, padx=50, fill='both', expand=True)
        
        # Title
        ctk.CTkLabel(
            main_frame, 
            text="ADMIN LOGIN",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 30))
        
        # Form frame
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(pady=20, padx=20, fill='x')
    
        # User
        self.username_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Username",
            height=40,
            font=("Arial", 14)
        )
        self.username_entry.pack(pady=15, padx=20, fill='x')
        
        # Pas
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Password",
            show="•",
            height=40,
            font=("Arial", 14)
        )
        self.password_entry.pack(pady=15, padx=20, fill='x')
        
        # Remember Me checkbox
        ctk.CTkCheckBox(
            form_frame,
            text="Remember Me",
            variable=self.remember_me
        ).pack(pady=10, padx=20, anchor='w')
        
        # Login button
        ctk.CTkButton(
            form_frame,
            text="LOGIN",
            command=self.attempt_login,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#2E8B57",
            hover_color="#3CB371"
        ).pack(pady=20, padx=20, fill='x')
        
        # Dark mode switch
        ctk.CTkSwitch(
            main_frame,
            text="Dark Mode",
            variable=self.dark_mode,
            command=lambda: ctk.set_appearance_mode("dark" if self.dark_mode.get() else "light")
        ).pack(pady=10)
        
        # Footer
        ctk.CTkLabel(
            main_frame,
            text="© 2025 Entrepôt Brahem",
            font=("Arial", 10)
        ).pack(side='bottom', pady=10)
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda e: self.attempt_login())

    def attempt_login(self):
        """Verify credentials and proceed"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            self.save_credentials()
            self.on_login_success()
        else:
            CTkMessagebox(
                title="Login Failed",
                message="Invalid credentials",
                icon="cancel"
            )
            self.password_entry.delete(0, 'end')

    def save_credentials(self):
        """Save or clear credentials based on Remember Me"""
        if self.remember_me.get():
            with open(REMEMBER_ME_FILE, "w") as f:
                f.write(f"{self.ADMIN_USERNAME}\n{self.ADMIN_PASSWORD}")
        elif os.path.exists(REMEMBER_ME_FILE):
            os.remove(REMEMBER_ME_FILE)

    def on_login_success(self):
        """Handle successful login"""
        self.app.destroy()  # Close login window
        
        # Import and launch main application
        from main import MainApp
        main_app = MainApp()

if __name__ == "__main__":
    LoginApp()