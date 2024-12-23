import os
import cv2
import easyocr
import shutil


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

    if total_files == 0:
        print("Нет изображений для обработки.")
        return

    # Обрабатываем все файлы в директории
    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(source_dir, filename)

        try:
            # Загружаем изображение в градациях серого для ускорения
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Распознаем текст на изображении, фильтруя только цифры
            results = reader.readtext(image, allowlist="0123456789", detail=0)

            # Проверяем, есть ли любой из целевых номеров в распознанных результатах
            if any(target_number in result for result in results for target_number in target_numbers):
                print(f"Один из номеров {target_numbers} найден на {filename}")
                shutil.move(file_path, os.path.join(valid_dir, filename))
            else:
                print(f"Номера {target_numbers} не найдены на {filename}")
                shutil.move(file_path, os.path.join(not_found_dir, filename))

            # Логируем прогресс
            print(f"Прогресс: {index}/{total_files} ({(index / total_files) * 100:.2f}%)")

        except Exception as e:
            print(f"Ошибка обработки файла {filename}: {e}")


if __name__ == "__main__":
    source_directory = "source_photos"  # Путь к директории с фотографиями
    marathon_numbers = ["1745", "1144", "1143"]  # Список целевых номеров

    find_numbers_on_photos(source_directory, marathon_numbers)