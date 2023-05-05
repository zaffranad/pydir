import os
import tkinter as tk
from tkinter import filedialog
from typing import Dict

from file_class import FileByExtension
from helpers import save_stat_total_size

WINDOW_OPENING_SIZE = "900x500"

DEFAULT_PATH = 'F:\\sandbox_python'


def process_selected_directory():
    directory = directory_text.get()
    files = os.walk(directory)
    listbox_stats.delete(0, tk.END)

    stats = []
    total_size = 0
    files_by_extension.clear()

    for (dir_path, dirs_inside, files_inside) in files:
        if len(files_inside) > 0:
            for file in files_inside:
                file_path = os.path.join(dir_path, file)
                total_size += os.path.getsize(file_path)

                extension = os.path.splitext(file)[1]

                if file.startswith('.'):
                    continue

                if extension in files_by_extension:
                    files_by_extension[extension].files.append(file_path)
                else:
                    files_by_extension[extension] = FileByExtension([file_path])

    save_stat_total_size(total_size, stats)

    for extension, file_by_extension in files_by_extension.items():
        listbox_stats.insert(tk.END, f"{extension} : {file_by_extension.count()}")

    for stat in stats:
        print(stat)
        listbox_stats.insert(tk.END, stat)


def select_directory():
    directory = filedialog.askdirectory()
    directory_text.delete(0, tk.END)
    directory_text.insert(0, directory)


def display_files(event):
    listbox_files.delete(0, tk.END)
    index = listbox_stats.curselection()[0]
    for file in list(files_by_extension.values())[index].files:
        listbox_files.insert(tk.END, f"{file}")


window = tk.Tk()
window.geometry(WINDOW_OPENING_SIZE)

files_by_extension: Dict[str, FileByExtension] = {}

directory_label = tk.Label(window, text="Répertoire:")
directory_label.pack()

directory_text = tk.Entry(window, )
directory_text.insert(0, DEFAULT_PATH)
directory_text.pack()

directory_button = tk.Button(window, text="Sélectionner", command=select_directory)
directory_button.pack()

list_button = tk.Button(window, text="Analyzer", command=process_selected_directory)
list_button.pack()

listbox_stats = tk.Listbox(window)
listbox_stats.pack(fill=tk.BOTH, expand=True)
listbox_stats.bind("<<ListboxSelect>>", display_files)

listbox_files = tk.Listbox(window)
listbox_files.pack(fill=tk.BOTH, expand=True)

window.mainloop()
