import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re

class PasswordStrengthAnalyzer:
    """
    A utility class to analyze password strength and provide feedback
    """
    @staticmethod
    def calculate_strength(password):
        """
        Calculate password strength based on various criteria
        
        :param password: Password string to analyze
        :return: Strength level and feedback
        """
        if not password:
            return 0, "No password provided"
        
        strength = 0
        feedback = []
        
        # Length check
        if len(password) < 8:
            feedback.append("Too short (less than 8 characters)")
        elif len(password) >= 12:
            strength += 2
            feedback.append("Good length")
        else:
            strength += 1
            feedback.append("Moderate length")
        
        # Character diversity checks
        checks = [
            (r'[A-Z]', "Contains uppercase letters"),
            (r'[a-z]', "Contains lowercase letters"),
            (r'\d', "Contains digits"),
            (r'[!@#$%^&*(),.?":{}|<>]', "Contains special characters")
        ]
        
        for pattern, msg in checks:
            if re.search(pattern, password):
                strength += 1
                feedback.append(msg)
        
        # Normalize strength
        strength = min(max(strength, 0), 5)
        
        return strength, ", ".join(feedback)

class PasswordGenerator:
    """
    Main password generation and management class
    """
    def __init__(self, master):
        """
        Initialize the password generator application
        
        :param master: Root tkinter window
        """
        self.master = master
        self.master.title("Secure Password Generator")
        self.master.geometry("600x700")
        self.master.configure(bg="#f0f0f0")
        
        self._create_widgets()
        self._setup_styles()
    
    def _create_widgets(self):
        """
        Create and layout application widgets
        """
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Password Length
        ttk.Label(main_frame, text="Password Length:").grid(row=0, column=0, sticky="w", pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(
            main_frame, 
            from_=4, 
            to=32, 
            orient=tk.HORIZONTAL, 
            variable=self.length_var, 
            length=300
        )
        self.length_scale.grid(row=0, column=1, sticky="ew", pady=5)
        self.length_display = ttk.Label(main_frame, textvariable=self.length_var)
        self.length_display.grid(row=0, column=2, padx=5)
        
        # Character Set Selections
        self.char_vars = {
            'uppercase': tk.BooleanVar(value=True),
            'lowercase': tk.BooleanVar(value=True),
            'digits': tk.BooleanVar(value=True),
            'symbols': tk.BooleanVar(value=True)
        }
        
        char_options = [
            ("Uppercase Letters", 'uppercase'),
            ("Lowercase Letters", 'lowercase'),
            ("Digits", 'digits'),
            ("Special Symbols", 'symbols')
        ]
        
        for idx, (label, key) in enumerate(char_options, 1):
            ttk.Checkbutton(
                main_frame, 
                text=label, 
                variable=self.char_vars[key]
            ).grid(row=idx, column=0, columnspan=2, sticky="w", pady=2)
        
        # Generate Button
        self.generate_btn = ttk.Button(
            main_frame, 
            text="Generate Password", 
            command=self._generate_password
        )
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Password Display
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            main_frame, 
            textvariable=self.password_var, 
            show="•", 
            font=("Courier", 14)
        )
        self.password_entry.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")
        
        # Copy and Show Buttons
        self.copy_btn = ttk.Button(
            main_frame, 
            text="Copy Password", 
            command=self._copy_password
        )
        self.copy_btn.grid(row=7, column=0, pady=5)
        
        self.show_btn = ttk.Button(
            main_frame, 
            text="Show/Hide", 
            command=self._toggle_password_visibility
        )
        self.show_btn.grid(row=7, column=1, pady=5)
        
        # Strength Indicator
        self.strength_label = ttk.Label(
            main_frame, 
            text="Strength: N/A", 
            font=("Helvetica", 10)
        )
        self.strength_label.grid(row=8, column=0, columnspan=3, pady=5)
    
    def _setup_styles(self):
        """
        Configure widget styles
        """
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10))
    
    def _generate_password(self):
        """
        Generate a password based on selected criteria
        """
        character_sets = {
            'uppercase': string.ascii_uppercase,
            'lowercase': string.ascii_lowercase,
            'digits': string.digits,
            'symbols': string.punctuation
        }
        
        # Collect selected character sets
        char_pool = ''.join(
            character_sets[key] for key, var in self.char_vars.items() 
            if var.get()
        )
        
        if not char_pool:
            messagebox.showerror("Error", "Select at least one character type")
            return
        
        # Generate password
        password = ''.join(
            random.choice(char_pool) for _ in range(self.length_var.get())
        )
        
        self.password_var.set(password)
        
        # Analyze strength
        strength, feedback = PasswordStrengthAnalyzer.calculate_strength(password)
        strength_colors = ['red', 'orange', 'yellow', 'light green', 'green']
        
        self.strength_label.config(
            text=f"Strength: {strength}/5 - {feedback}",
            foreground=strength_colors[strength]
        )
    
    def _copy_password(self):
        """
        Copy password to clipboard
        """
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def _toggle_password_visibility(self):
        """
        Toggle password visibility
        """
        current_show = self.password_entry.cget('show')
        self.password_entry.configure(show='' if current_show == '•' else '•')

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()