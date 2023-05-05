import os
import tkinter as tk
from tkinter import filedialog
from typing import Dict

import pdfplumber
import pyttsx3
from PyPDF3 import PdfFileReader

from file_class import FileByExtension
from helpers import is_pdf_file

WINDOW_OPENING_SIZE = "900x560"

DEFAULT_PATH = 'F:\\sandbox_python'


def process_selected_directory():
    directory = entry_choose_directory.get()
    listbox_files.delete(0, tk.END)
    files = os.walk(directory)

    for (dir_path, dirs_inside, files_inside) in files:
        if len(files_inside) > 0:
            for file in files_inside:
                file_path = os.path.join(dir_path, file)

                if is_pdf_file(file):
                    listbox_files.insert(tk.END, f"{file_path}")


def select_directory():
    directory = filedialog.askdirectory()
    entry_choose_directory.delete(0, tk.END)
    entry_choose_directory.insert(0, directory)


def activate_generate_audio_button(event):
    if os.path.splitext(listbox_files.get(listbox_files.curselection()))[1].lower() == '.pdf':
        button_generate_audio['state'] = 'normal'
    else:
        button_generate_audio['state'] = 'disabled'


def process_audio_generation():
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
    dest_filename = file + '.mp3'
    engine.save_to_file(final_text, f'{dest_filename}')
    engine.runAndWait()

    print(f"successfully generated audio file at {dest_filename}")
    label = tk.Label(window,
                     text="successfully generated audio file at " + dest_filename + "\npath copied to clipboard...")
    label.grid(row=2, column=1, columnspan=3)
    window.clipboard_clear()
    window.clipboard_append(dest_filename)

    book.close()
    engine.stop()


def destroy(msg, btn):
    msg.pack_forget()
    btn.pack_forget()
    return lambda: None


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
window.columnconfigure(0, minsize=200)
window.columnconfigure(1, minsize=400)
window.rowconfigure(1, minsize=500)

files_by_extension: Dict[str, FileByExtension] = {}

label_choose_directory = tk.Label(window, text="directory to scan :")
label_choose_directory.grid(row=0, column=0)

entry_choose_directory = tk.Entry(window, width=90)
entry_choose_directory.insert(0, DEFAULT_PATH)
entry_choose_directory.grid(row=0, column=1)

button_select_directory = tk.Button(window, text="open...", command=select_directory)
button_select_directory.grid(row=0, column=2)

button_process_selected_directory = tk.Button(window, text="scan", command=process_selected_directory)
button_process_selected_directory.grid(row=0, column=3)

frame_files = tk.Frame(window, exportselection=False)
frame_files.grid(row=1, column=0, columnspan=4, sticky="NSEW")

scrollbar_files_vertical = tk.Scrollbar(frame_files, orient=tk.VERTICAL)
scrollbar_files_vertical.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_files_horizontal = tk.Scrollbar(frame_files, orient=tk.HORIZONTAL)
scrollbar_files_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
listbox_files = tk.Listbox(frame_files, exportselection=False, yscrollcommand=scrollbar_files_vertical.set,
                           xscrollcommand=scrollbar_files_horizontal.set)
listbox_files.bind("<<ListboxSelect>>", activate_generate_audio_button)
listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
button_generate_audio = tk.Button(window, text="générer audio", command=process_audio_generation, state='disabled')
button_generate_audio.grid(row=2, column=0)

button_generate_audio = tk.Button(window, text="générer audio", command=generate_audio, state='disabled')
button_generate_audio.pack()

window.mainloop()
