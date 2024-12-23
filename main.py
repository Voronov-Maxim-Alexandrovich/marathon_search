import os
import cv2
import easyocr
import shutil

def standardize_digits(text: str) -> str:
    """
    Заменяем '7' на '1' во всей строке,
    чтобы считать 7 и 1 эквивалентными.
    """
    return text.replace('7', '1')


def filter_text(text_result):
    std_result = set()
    orig_result = set()
    for orig_text in text_result:
        if 3 <= len(orig_text) <= 4:
            orig_result.add(orig_text)
            std_result.add(standardize_digits(orig_text))
    return orig_result, std_result




def find_numbers_on_photos(source_dir, target_numbers):
    # Убедимся, что папка существует
    if not os.path.exists(source_dir):
        print(f"Директория {source_dir} не существует.")
        return

    valid_dir = "valid_photos"
    not_found_dir = "not_found"

    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)
    if not os.path.exists(not_found_dir):
        os.makedirs(not_found_dir)

    # Создаем Reader с минимальными настройками для ускорения
    reader = easyocr.Reader(['en'], gpu=True)

    # Получаем список файлов
    files = [f for f in os.listdir(source_dir) if f.lower().endswith(('jpg', 'jpeg', 'png', 'bmp'))]
    total_files = len(files)

    orig_numbers = set(target_numbers)
    std_numbers_dict = {standardize_digits(n): n for n in target_numbers}
    std_numbers = set([standardize_digits(n) for n in target_numbers])

    if total_files == 0:
        print("Нет изображений для обработки.")
        return

    # Обрабатываем все файлы в директории
    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(source_dir, filename)

        try:
            # Загружаем изображение в градациях серого для ускорения
            # image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Распознаем текст на изображении, фильтруя только цифры
            orig_result, std_result = filter_text(reader.readtext(file_path, allowlist="0123456789", detail=0))
            found_numbers = [std_numbers_dict[n] for n in std_numbers.intersection(std_result)]

            # Проверяем, есть ли любой из целевых номеров в распознанных результатах
            if found_numbers:
                print(f"Файл '{filename}': Найдены номера {found_numbers}")
                print(f"Прогресс: {index}/{total_files} ({(index / total_files) * 100:.2f}%)")
                shutil.move(file_path, os.path.join(valid_dir, filename))
            else:
                shutil.move(file_path, os.path.join(not_found_dir, filename))


        except Exception as e:
            print(f"Ошибка обработки файла {filename}: {e}")


if __name__ == "__main__":
    source_directory = "source_photos"  # Путь к директории с фотографиями
    marathon_numbers = ['3028', '1473', '3531', '4017', '1217', '1138', '1340', '1131', '1745', '2620', '2550', '1213',
                        '3365', '1222', '2145', '1508', '1317', '2151', '1262', '252', '1908', '1617', '2297', '3166',
                        '1108', '1143', '1144', '1960']

    find_numbers_on_photos(source_directory, marathon_numbers)
