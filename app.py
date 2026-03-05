# Scary Theme Updates for app.py

# Import required packages for enhanced animations and spooky themes
import tkinter as tk
from tkinter import PhotoImage

# Define main application window
class ScaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Demon's Lair")
        self.master.geometry("800x600")
        self.master.config(bg='#000000')  # Black background

        # Setting up spooky icons
        self.icon = PhotoImage(file='path/to/spooky_icon.png')
        self.master.iconphoto(False, self.icon)

        # Add a spooky header
        self.header = tk.Label(self.master, text='Welcome to the Demon’s Lair', font=('Monospace', 24), fg='#00FF00', bg='#000000')
        self.header.pack(pady=20)

        # Create animated buttons
        self.start_button = tk.Button(self.master, text='Start', command=self.start_animation, bg='#00FF00', fg='#000000', font=('Arial', 16), relief='groove')
        self.start_button.pack(pady=10)

        # Enhance button animations and effects
        self.start_button.bind('<Enter>', self.on_enter)
        self.start_button.bind('<Leave>', self.on_leave)

        # Additional spooky UI elements can be added here

    # Function to handle button hover animations
    def on_enter(self, e):
        self.start_button['bg'] = '#1AFF1A'  # Light neon green
        self.start_button['fg'] = '#000000'

    def on_leave(self, e):
        self.start_button['bg'] = '#00FF00'  # Original neon green
        self.start_button['fg'] = '#000000'

    def start_animation(self):
        # Imagine this function carries out some fun animation 
        print("Spooky animation starts!")

# Run the application
if __name__ == '__main__':
    root = tk.Tk()
    app = ScaryApp(root)
    root.mainloop()