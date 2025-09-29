import tkinter as tk
from src.gui.main_window import JobApplicationApp

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationApp(root)
    root.mainloop()