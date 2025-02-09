import cv2
import numpy as np
import os

# Указываем путь к папке с изображениями и файлом списка
image_folder = 'images'  # Папка с изображениями и текстовым файлом
image_list_path = os.path.join(image_folder, 'images.txt')

# Чтение списка файлов из текстового файла
with open(image_list_path, 'r') as file:
    image_paths = [line.strip() for line in file.readlines()]

# Загружаем изображения, добавляя путь к каждому из них
images = []
image_info = []  # Для хранения информации о каждом изображении (путь и само изображение)
for image_name in image_paths:
    image_path = os.path.join(image_folder, image_name)
    img = cv2.imread(image_path)
    if img is not None:
        images.append(img)
        image_info.append((image_path, img))  # Сохраняем путь и изображение
    else:
        print(f"Не удалось загрузить изображение: {image_path}")

# Проверяем, есть ли загруженные изображения
if not images:
    print("Нет загруженных изображений.")
    exit()

# Функции для сортировки
def sort_by_brightness(imgs_info):
    # Рассчитываем среднюю яркость для каждого изображения
    return sorted(imgs_info, key=lambda x: np.mean(cv2.cvtColor(x[1], cv2.COLOR_BGR2GRAY)), reverse=True)

def sort_by_red(imgs_info):
    # Рассчитываем среднее значение красного канала
    return sorted(imgs_info, key=lambda x: np.mean(x[1][:, :, 2]), reverse=True)

def sort_by_blue(imgs_info):
    # Рассчитываем среднее значение синего канала
    return sorted(imgs_info, key=lambda x: np.mean(x[1][:, :, 0]), reverse=True)

# Параметры окна и количество столбцов
window_width = 800
window_height = 600
columns = 4  # Количество столбцов
padding = 10  # Отступ между картинками

# Определение размера каждого изображения в зависимости от количества столбцов
image_width = (window_width - (columns + 1) * padding) // columns

# Расчет количества строк для размещения всех изображений
rows = (len(images) + columns - 1) // columns

# Функция для отображения атласа
def display_atlas(sorted_images):
    aspect_ratios = [img.shape[1] / img.shape[0] for _, img in sorted_images]  # Соотношение сторон

    # Создаем пустой атлас с размерами окна 800х600
    atlas = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255  # белый фон

    # Располагаем изображения на атласе с учетом их пропорций
    x_offset = padding
    y_offset = padding
    current_row = 0

    for idx, (path, img) in enumerate(sorted_images):
        aspect_ratio = aspect_ratios[idx]
        image_height = int(image_width / aspect_ratio)

        # Масштабируем изображение
        resized_img = cv2.resize(img, (image_width, image_height))

        # Если изображение не помещается по высоте, переходим на новую строку
        if y_offset + image_height + padding > window_height:
            current_row += 1
            y_offset = padding
            x_offset = padding + current_row * (image_width + padding)

        if x_offset + image_width > window_width:
            break  # Заканчиваем, если вышли за пределы окна

        # Размещаем изображение на атласе
        atlas[y_offset:y_offset + image_height, x_offset:x_offset + image_width] = resized_img

        # Смещаемся на следующую позицию
        y_offset += image_height + padding

    # Отображаем атлас в окне фиксированного размера
    cv2.imshow('Atlas', atlas)

# Изначальное отображение атласа без сортировки
display_atlas(image_info)

# Основной цикл программы для обработки клавиш
while True:
    key = cv2.waitKey(0)
    if key == ord('t'):
        # Сортировка по яркости
        sorted_images = sort_by_brightness(image_info)
        display_atlas(sorted_images)
    elif key == ord('y'):
        # Сортировка по красному каналу
        sorted_images = sort_by_red(image_info)
        display_atlas(sorted_images)
    elif key == ord('u'):
        # Сортировка по синему каналу
        sorted_images = sort_by_blue(image_info)
        display_atlas(sorted_images)
    elif key == 27:  # Клавиша Esc для выхода
        break

cv2.destroyAllWindows()
