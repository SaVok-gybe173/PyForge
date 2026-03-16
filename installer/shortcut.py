import os
import sys
import logging

try:
    import winshell
    from win32com.client import Dispatch
except ImportError:
    winshell = None
    logging.warning("Библиотека 'winshell' или 'pywin32' не установлена. Функции создания ярлыков будут недоступны.")

# Настройка логирования для вывода информации и ошибок
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_and_move_shortcut(
    exe_path: str,
    destination_folder: str,
    shortcut_name: str = None,
    working_directory: str = None,
    description: str = None,
    icon_path: str = None
) -> bool:
    """
    Создает ярлык (.lnk) для .exe файла и перемещает его в указанную папку на Windows.

    :param exe_path: Полный путь к исполняемому файлу (.exe), для которого создается ярлык.
    :param destination_folder: Путь к папке, куда будет перемещен созданный ярлык.
                               Если папка не существует, она будет создана.
    :param shortcut_name: Имя файла ярлыка (без расширения .lnk). Если None,
                          используется имя .exe файла.
    :param working_directory: Рабочая директория для ярлыка. Если None, используется
                              директория, где находится .exe файл.
    :param description: Описание ярлыка (отображается в свойствах).
    :param icon_path: Путь к файлу иконки (.ico, .exe, .dll). Если None,
                      используется иконка из самого .exe файла.
    :return: True, если ярлык успешно создан и перемещен, иначе False.
    """
    if sys.platform != 'win32':
        logging.error("Эта функция предназначена только для операционных систем Windows.")
        return False

    if winshell is None:
        logging.error("Не удалось импортировать 'winshell' или 'pywin32'. Убедитесь, что они установлены: pip install winshell pywin32")
        return False

    if not os.path.isfile(exe_path):
        logging.error(f"Ошибка: Исполняемый файл '{exe_path}' не найден.")
        return False

    # Убедимся, что целевая папка существует
    try:
        os.makedirs(destination_folder, exist_ok=True)
        logging.info(f"Целевая папка '{destination_folder}' проверена/создана.")
    except OSError as e:
        logging.error(f"Ошибка при создании целевой папки '{destination_folder}': {e}")
        return False

    # Определяем имя ярлыка
    if shortcut_name is None:
        shortcut_name = os.path.splitext(os.path.basename(exe_path))[0] # Имя файла без расширения
    
    # Полный путь к ярлыку (в целевой папке)
    shortcut_full_path = os.path.join(destination_folder, f"{shortcut_name}.lnk")
    
    # Рабочая директория для ярлыка
    if working_directory is None:
        working_directory = os.path.dirname(exe_path)

    try:
        # Создаем ярлык
        with winshell.shortcut(shortcut_full_path) as link:
            link.path = exe_path
            link.description = description if description else f"Ярлык для {os.path.basename(exe_path)}"
            link.working_directory = working_directory
            # Icon path can be (path, index). Index 0 means first icon in the file.
            link.icon_location = (icon_path, 0) if icon_path else (exe_path, 0)
        
        logging.info(f"Ярлык '{shortcut_full_path}' успешно создан для '{exe_path}'.")
        return True

    except Exception as e:
        logging.error(f"Произошла ошибка при создании или перемещении ярлыка: {e}")
        return False