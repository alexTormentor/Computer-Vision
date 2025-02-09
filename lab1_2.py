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
for image_name in image_paths:
    image_path = os.path.join(image_folder, image_name)
    img = cv2.imread(image_path)
    if img is not None:
        images.append(img)
    else:
        print(f"Не удалось загрузить изображение: {image_path}")

# Проверяем, есть ли загруженные изображения
if not images:
    print("Нет загруженных изображений.")
    exit()

# Приводим все изображения к минимальным размерам
min_width = min(img.shape[1] for img in images)
min_height = min(img.shape[0] for img in images)

def resize_images_to_min(images, width, height):
    """Изменение размеров всех изображений до минимальных ширины и высоты."""
    resized_images = [cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA) for img in images]
    return resized_images

# Приводим все изображения к минимальным размерам
images = resize_images_to_min(images, min_width, min_height)

# Параметры по умолчанию
columns = 4  # Начальное количество столбцов
scale_percent = 100  # Масштаб изображений (в процентах)

def calculate_brightness(image):
    """Вычисление средней яркости изображения."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

def sort_images_by_brightness(images):
    """Сортировка изображений по средней яркости."""
    brightness_values = [calculate_brightness(img) for img in images]
    sorted_images = [img for _, img in sorted(zip(brightness_values, images), key=lambda pair: pair[0])]
    return sorted_images

# Сортируем изображения по яркости
images = sort_images_by_brightness(images)

def resize_images(images, scale_percent):
    """Изменение размера всех изображений в зависимости от процента масштабирования."""
    resized_images = []
    for img in images:
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        resized_images.append(resized_img)
    return resized_images

def create_atlas(images, columns):
    """Создание атласа из изображений с заданным количеством столбцов."""
    # Находим максимальные ширину и высоту среди изображений
    max_width = max(img.shape[1] for img in images)
    max_height = max(img.shape[0] for img in images)

    # Определяем размер атласа
    rows = (len(images) + columns - 1) // columns  # Вычисление необходимого количества строк
    atlas_width = columns * max_width
    atlas_height = rows * max_height

    # Создаем пустой атлас
    atlas = np.zeros((atlas_height, atlas_width, 3), dtype=np.uint8)

    # Располагаем изображения на атласе
    for idx, img in enumerate(images):
        row = idx // columns
        col = idx % columns
        x_offset = col * max_width
        y_offset = row * max_height
        atlas[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img

    return atlas

# Создаем окно
cv2.namedWindow('Atlas', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Atlas', 800, 600)

def update_atlas(x):
    """Функция для обновления атласа при изменении масштаба и количества столбцов."""
    global scale_percent, columns
    scale_percent = cv2.getTrackbarPos('Scale', 'Atlas')
    columns = cv2.getTrackbarPos('Columns', 'Atlas') or 1  # Предотвращаем деление на 0

    # Масштабируем изображения
    resized_images = resize_images(images, scale_percent)
    # Создаем атлас
    atlas = create_atlas(resized_images, columns)
    # Показываем атлас
    cv2.imshow('Atlas', atlas)

# Создаем ползунки для масштабирования и изменения количества столбцов
cv2.createTrackbar('Scale', 'Atlas', scale_percent, 200, update_atlas)
cv2.createTrackbar('Columns', 'Atlas', columns, 10, update_atlas)

# Инициализируем отображение
update_atlas(0)

# Основной цикл программы
cv2.waitKey(0)
cv2.destroyAllWindows()
