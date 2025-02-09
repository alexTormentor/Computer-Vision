import cv2
import numpy as np
import random


def draw_canny_edges(image_path, color=(0, 255, 0), thickness=2, low_threshold=100, high_threshold=200):
    # Чтение исходного изображения
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")

    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение фильтра Кэнни для выделения границ
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)

    # Создание пустого изображения для рисования контуров
    edges_colored = np.zeros_like(image)

    # Найти контуры
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Нарисовать контуры на новом изображении с заданным цветом и толщиной
    cv2.drawContours(edges_colored, contours, -1, color, thickness)

    # Совмещение исходного изображения с изображением контуров
    result = cv2.addWeighted(image, 0.8, edges_colored, 0.5, 0)

    return result


def blur_except_edges(image_path, color=(0, 255, 0), thickness=2, low_threshold=100, high_threshold=200,
                      blur_ksize=(15, 15)):
    # Чтение исходного изображения
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")

    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение фильтра Кэнни для выделения границ
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)

    # Создание маски границ
    edges_mask = np.zeros_like(image)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(edges_mask, contours, -1, (255, 255, 255), thickness)

    # Инвертирование маски
    mask_inv = cv2.bitwise_not(edges_mask)

    # Размытие всего изображения
    blurred_image = cv2.GaussianBlur(image, blur_ksize, 0)

    # Применение размытия к не границам
    blurred_background = cv2.bitwise_and(blurred_image, mask_inv)
    edges_colored = cv2.bitwise_and(edges_mask, image)

    # Комбинирование размытых и четких областей
    result = cv2.add(blurred_background, edges_colored)

    return result


def stained_glass_effect(image_path, edge_color=(0, 0, 0), edge_thickness=2, low_threshold=1, high_threshold=10,
                         blur_ksize=(5, 5)):
    # Чтение исходного изображения
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")

    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение размытия для сглаживания мелких деталей
    blurred_gray = cv2.GaussianBlur(gray_image, blur_ksize, 0)

    # Применение фильтра Кэнни для выделения границ
    edges = cv2.Canny(blurred_gray, low_threshold, high_threshold)

    # Найти контуры с учетом внутренней структуры
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Создать пустое изображение для эффекта витража
    stained_glass = np.zeros_like(image)

    # Для каждой области (замкнутого контура) заполняем насыщенными случайными цветами
    for contour in contours:
        # Генерация насыщенного случайного цвета
        random_color = [random.randint(50, 255) for _ in range(3)]

        # Заливка области случайным цветом
        cv2.drawContours(stained_glass, [contour], -1, random_color, cv2.FILLED)

    # Наложение границ заданного цвета на изображение
    cv2.drawContours(stained_glass, contours, -1, edge_color, edge_thickness)

    return stained_glass


'''result_image = draw_canny_edges('vita.png', color=(0, 0, 255), thickness=3)
cv2.imshow('Edges', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

'''result_image = blur_except_edges('vita.png', color=(0, 0, 255), thickness=3)
cv2.imshow('Blurred Except Edges', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

result_image = stained_glass_effect('vita.png', edge_color=(0, 0, 0), edge_thickness=3)
cv2.imshow('Stained Glass Effect', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
