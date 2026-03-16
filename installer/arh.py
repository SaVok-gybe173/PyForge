import zipfile
import os
import logging

# Настройка логирования для вывода информации и ошибок
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def unzip_archive(
    zip_file_path: str,
    extract_to_dir: str,
    password: str = None,
    members_to_extract: list[str] = None
) -> bool:
    """
    Распаковывает ZIP-архив в указанную директорию.

    :param zip_file_path: Путь к ZIP-файлу, который нужно распаковать.
    :param extract_to_dir: Путь к директории, куда будет распаковано содержимое.
                           Если директория не существует, она будет создана.
    :param password: Пароль для защищенного архива (необязательно).
                     Должен быть строкой.
    :param members_to_extract: Список строк с именами файлов/папок внутри архива,
                               которые нужно извлечь. Если None или пустой список,
                               будет распаковано всё содержимое архива (необязательно).
    :return: True, если распаковка прошла успешно, иначе False.
    """
    if not os.path.exists(zip_file_path):
        logging.error(f"Ошибка: ZIP-файл '{zip_file_path}' не найден.")
        return False

    # Создаем целевую директорию, если она не существует
    try:
        os.makedirs(extract_to_dir, exist_ok=True)
        logging.info(f"Целевая директория '{extract_to_dir}' проверена/создана.")
    except OSError as e:
        logging.error(f"Ошибка при создании директории '{extract_to_dir}': {e}")
        return False

    pwd_bytes = None
    if password:
        pwd_bytes = password.encode('utf-8')
        logging.info("Используется пароль для распаковки архива.")

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Проверяем, есть ли что-то в архиве
            if not zip_ref.namelist():
                logging.warning(f"Архив '{zip_file_path}' пуст.")
                return True # Считаем, что распаковка "успешна", так как ничего не надо распаковывать

            if members_to_extract:
                # Распаковка только указанных членов
                extracted_count = 0
                for member_name in members_to_extract:
                    if member_name in zip_ref.namelist():
                        try:
                            zip_ref.extract(member_name, extract_to_dir, pwd=pwd_bytes)
                            logging.info(f"Извлечен файл/папка: '{member_name}'")
                            extracted_count += 1
                        except RuntimeError as e:
                            if "Bad password" in str(e):
                                logging.error(f"Ошибка: Неверный пароль для '{member_name}' в архиве '{zip_file_path}'.")
                                return False
                            else:
                                logging.error(f"Ошибка при извлечении '{member_name}': {e}")
                                return False
                        except Exception as e:
                            logging.error(f"Неизвестная ошибка при извлечении '{member_name}': {e}")
                            return False
                    else:
                        logging.warning(f"Файл/папка '{member_name}' не найден(а) в архиве '{zip_file_path}'.")
                
                if extracted_count > 0:
                    logging.info(f"Успешно извлечено {extracted_count} из {len(members_to_extract)} запрошенных элементов из '{zip_file_path}' в '{extract_to_dir}'.")
                    return True
                else:
                    logging.warning(f"Не удалось извлечь ни один из запрошенных элементов из '{zip_file_path}'.")
                    return False
            else:
                # Распаковка всего содержимого
                zip_ref.extractall(extract_to_dir, pwd=pwd_bytes)
                logging.info(f"Архив '{zip_file_path}' успешно распакован полностью в '{extract_to_dir}'.")
                return True

    except FileNotFoundError:
        logging.error(f"Ошибка: Файл '{zip_file_path}' не найден (несмотря на начальную проверку).")
        return False
    except zipfile.BadZipFile:
        logging.error(f"Ошибка: Файл '{zip_file_path}' не является действительным ZIP-архивом или поврежден.")
        return False
    except RuntimeError as e:
        if "Bad password" in str(e):
            logging.error(f"Ошибка: Неверный пароль для архива '{zip_file_path}'.")
        else:
            logging.error(f"Произошла ошибка при распаковке архива: {e}")
        return False
    except Exception as e:
        logging.error(f"Произошла неизвестная ошибка при распаковке '{zip_file_path}': {e}")
        return False