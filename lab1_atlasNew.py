import cv2
import numpy as np
import os

# Параметры
columns = 4         # количество столбцов
gap = 10            # расстояние между ними
scroll_step = 50    # Шаг прокрутки

# Пути
images_folder = 'images'
images_list_path = os.path.join(images_folder, 'images.txt')

# Чтение списка изображений
with open(images_list_path, 'r') as file:
    image_filenames = [line.strip() for line in file.readlines()]

# Загрузка изображений
images = []
original_sizes = []
for filename in image_filenames:
    img_path = os.path.join(images_folder, filename)    # путь к картинке
    img = cv2.imread(img_path)                          # саму картинку
    # Если картинки нет, то просто идём дальше
    if img is None:
        continue
    images.append(img)                                   # Добавляем найденные изображения в список
    original_sizes.append((img.shape[1], img.shape[0]))  # добавляем ширину и высоту

# Рассчитываем ширину столбца
atlas_width = 1200  # Ширина атласа
column_width = (atlas_width - (columns + 1) * gap) // columns   # ширина одного столбца

# Масштабируем изображения с сохранением пропорций
# размеры картинок
scaled_images = []
scaled_heights = []
brightness_values = []  # Список для хранения яркости изображений
for img, (orig_w, orig_h) in zip(images, original_sizes):
    scale_factor = column_width / orig_w    # коэффициент масштабирования
    new_width = int(orig_w * scale_factor)  # новая ширина
    new_height = int(orig_h * scale_factor) # новая высота
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)    # уменьшение размера изображения
    # Добавляем картинки в список
    scaled_images.append(img_resized)
    scaled_heights.append(new_height)
    # Вычисляем среднюю яркость изображения
    brightness = np.mean(cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY))
    brightness_values.append(brightness)

# Функция для создания атласа
def create_atlas(sorted_images):
    # Распределяем изображения по столбцам для "водопадного" расположения
    column_heights = [0] * columns
    column_images = [[] for _ in range(columns)]

    for img in sorted_images:
        height = img.shape[0]   # Заносим высоты
        # Находим столбец с минимальной текущей высотой
        min_col_index = column_heights.index(min(column_heights))
        column_images[min_col_index].append(img)
        column_heights[min_col_index] += height + gap

    # Высота атласа определяется максимальной высотой столбца
    atlas_height = max(column_heights) + gap

    # Создаем пустой атлас
    atlas = np.full((atlas_height, atlas_width, 3), 255, dtype=np.uint8)

    # Размещение изображений на атласе
    x_positions = [gap + i * (column_width + gap) for i in range(columns)]
    y_positions = [gap] * columns


    for col_idx, images_in_col in enumerate(column_images):
        x = x_positions[col_idx]
        y = y_positions[col_idx]
        # Идём по столбцу и получаем ширину с высотой
        for img in images_in_col:
            h, w = img.shape[:2]
            # Размещение изображения
            atlas[y:y+h, x:x+w] = img
            # Обновление координаты y для следующего изображения в этом столбце
            y += h + gap

    return atlas, atlas_height

# Параметры для отображения
window_height = 800  # Высота окна для просмотра
current_scroll_position = 0  # Текущая позиция прокрутки
atlas, atlas_height = create_atlas(scaled_images)  # Создаем атлас первоначально

# Функция отображения видимой области атласа
def show_visible_atlas():
    visible_atlas = atlas[current_scroll_position:current_scroll_position + window_height, :]   # Это срез, который выбирает вертикальный диапазон строк из атласа
    cv2.imshow('Atlas', visible_atlas)

# Функция сортировки и обновления атласа
def sort_and_update(order):
    global atlas, atlas_height, current_scroll_position
    if order == 1:
        # Сортировка по яркости, яркие вверх
        sorted_images = [img for _, img in sorted(zip(brightness_values, scaled_images), reverse=True)]
    elif order == 2:
        # Сортировка по темности, темные вверх
        sorted_images = [img for _, img in sorted(zip(brightness_values, scaled_images))]
    # Создаем новый атлас на основе отсортированных изображений
    atlas, atlas_height = create_atlas(sorted_images)
    # Сбрасываем позицию прокрутки
    current_scroll_position = 0
    show_visible_atlas()

# Основной цикл отображения и обработки прокрутки
cv2.namedWindow('Atlas', cv2.WINDOW_NORMAL)
show_visible_atlas()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC для выхода
        break
    elif key == ord('w'):  # Прокрутка вверх
        current_scroll_position = max(0, current_scroll_position - scroll_step)
        show_visible_atlas()
    elif key == ord('s'):  # Прокрутка вниз
        current_scroll_position = min(atlas_height - window_height, current_scroll_position + scroll_step)
        show_visible_atlas()
    elif key == ord('1'):  # Сортировка по яркости
        sort_and_update(1)
    elif key == ord('2'):  # Сортировка по темности
        sort_and_update(2)

cv2.destroyAllWindows()
