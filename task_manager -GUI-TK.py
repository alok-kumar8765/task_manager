import psutil
import tkinter as tk
from tkinter import ttk
import time
import threading


def update_stats(label):
    while True:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        text = (
            f"CPU Usage : {cpu}%\n"
            f"Memory    : {mem.percent}%\n"
        )
        label.config(text=text)
        time.sleep(1)


def main_gui():
    root = tk.Tk()
    root.title("Python Task Manager (Tkinter)")
    root.geometry("300x200")

    label = tk.Label(root, text="Loading...", font=("Arial", 12))
    label.pack(pady=20)

    thread = threading.Thread(target=update_stats, args=(label,), daemon=True)
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main_gui()
