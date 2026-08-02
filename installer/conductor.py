import tkinter as tk
from tkinter import filedialog

def select_single_file():
    """Открыть проводник для выбора одного файла"""
    root = tk.Tk()
    root.withdraw()  # Прячем пустое окно tkinter
    # askopenfilename возвращает путь к файлу или пустую строку, если выбор отменен
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=[("Все файлы", "*.*"), ("Изображения", "*.png;*.jpg;*.jpeg"), ("Тексты", "*.txt")]
    )
    root.destroy()
    return file_path if file_path else None

def select_files_possible():
    """Открыть проводник для выбора нескольких файлов"""
    root = tk.Tk()
    root.withdraw()
    # askopenfilenames возвращает кортеж с путями
    files = filedialog.askopenfilenames(
        title="Выберите один или несколько файлов",
        filetypes=[("Все файлы", "*.*")]
    )
    root.destroy()
    return list(files) if files else None  # Преобразуем кортеж в список для удобства

def select_folder():
    """Открыть проводник для выбора папки"""
    root = tk.Tk()
    root.withdraw()
    # askdirectory возвращает путь к папке
    folder_path = filedialog.askdirectory(
        title="Выберите папку"
    )
    root.destroy()
    return folder_path if folder_path else None