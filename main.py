import os
import tkinter as tk
from tkinter import filedialog
from typing import Dict

import pdfplumber
import pyttsx3
from PyPDF3 import PdfFileReader

from file_class import FileByExtension
from helpers import save_stat_total_size

WINDOW_OPENING_SIZE = "900x700"

DEFAULT_PATH = 'F:\\sandbox_python'


def process_selected_directory():
    directory = entry_choose_directory.get()
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

                extension = os.path.splitext(file)[1].lower()

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
    entry_choose_directory.delete(0, tk.END)
    entry_choose_directory.insert(0, directory)


def display_files(event):
    listbox_files.delete(0, tk.END)
    button_generate_audio['state'] = 'disabled'

    if not listbox_stats.curselection():
        return

    index = listbox_stats.curselection()[0]
    for file in list(files_by_extension.values())[index].files:
        listbox_files.insert(tk.END, f"{file}")


def activate_generate_audio_button(event):
    if os.path.splitext(listbox_files.get(listbox_files.curselection()))[1].lower() == '.pdf':
        button_generate_audio['state'] = 'normal'
    else:
        button_generate_audio['state'] = 'disabled'


def generate_audio():
    file = listbox_files.get(listbox_files.curselection()[0])
    print(f"generate audio for file {file}")
    book = open(file, 'rb')

    pdf_reader = PdfFileReader(book)
    pages = pdf_reader.numPages

    final_text = ""

    with pdfplumber.open(file) as pdf:
        for i in range(0, pages):
            page = pdf.pages[i]
            text = page.extract_text()
            final_text += text

    engine = pyttsx3.init()
    engine.save_to_file(final_text, f'{file}.mp3')
    engine.runAndWait()
    book.close()
    engine.stop()


window = tk.Tk()
window.geometry(WINDOW_OPENING_SIZE)

files_by_extension: Dict[str, FileByExtension] = {}

label_choose_directory = tk.Label(window, text="Répertoire:")
label_choose_directory.pack()

entry_choose_directory = tk.Entry(window)
entry_choose_directory.insert(0, DEFAULT_PATH)
entry_choose_directory.pack()

button_select_directory = tk.Button(window, text="Sélectionner", command=select_directory)
button_select_directory.pack()

button_process_selected_directory = tk.Button(window, text="Analyzer", command=process_selected_directory)
button_process_selected_directory.pack()

listbox_stats = tk.Listbox(window, exportselection=False)
listbox_stats.pack(fill=tk.BOTH, expand=True)
listbox_stats.bind("<<ListboxSelect>>", display_files)

listbox_files = tk.Listbox(window, exportselection=False)
listbox_files.bind("<<ListboxSelect>>", activate_generate_audio_button)
listbox_files.pack(fill=tk.BOTH, expand=True)

button_generate_audio = tk.Button(window, text="générer audio", command=generate_audio, state='disabled')
button_generate_audio.pack()

window.mainloop()
