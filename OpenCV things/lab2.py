import cv2
import numpy as np
import random


def draw_canny_edges(image_path, color=(0, 255, 0), thickness=2, low_threshold=100, high_threshold=200):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")

    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяется алгоритм Canny для обнаружения краёв, подаем серое изображение и параметры,
    # которые задают пороги для определения сильных и слабых границ
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)
    edges_colored = np.zeros_like(image)

    # Из найденных краёв извлекаются только внешние контуры и уменьшается количество точек, описывающих контур
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(edges_colored, contours, -1, color, thickness)
    result = cv2.addWeighted(image, 0.8, edges_colored, 0.5, 0)

    return result


def blur_except_edges(image_path, color=(0, 255, 0), thickness=2, low_threshold=100, high_threshold=200,
                      blur_ksize=(15, 15)):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)

    # Создание маски границ
    edges_mask = np.zeros_like(image)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(edges_mask, contours, -1, (255, 255, 255), thickness)

    # Инвертируем маску:
    # Белые области (границы) становятся чёрными, а чёрные области (фон) становятся белыми.
    # Это необходимо, чтобы выделить области вне границ.
    mask_inv = cv2.bitwise_not(edges_mask)

    # Применяется фильтр Гаусса ко всему изображению, а blur_ksize задаёт размер ядра размытия.
    # Чем больше ядро, тем сильнее размытие.
    blurred_image = cv2.GaussianBlur(image, blur_ksize, 0)

    # Применяем размытое изображение только к областям, где фон белый, т.е. области вне границ.
    # Используем побитовое И, чтобы размытое изображение осталось только на не-границах.
    blurred_background = cv2.bitwise_and(blurred_image, mask_inv)
    edges_colored = cv2.bitwise_and(edges_mask, image)

    # Комбинирование размытых и четких областей
    result = cv2.add(blurred_background, edges_colored)

    return result



def stained_glass_effect(image_path, edge_color=(0, 0, 0), edge_thickness=2,
                         low_threshold=50, high_threshold=150, blur_ksize=(5, 5), min_contour_area=100):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение.")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_gray = cv2.GaussianBlur(gray_image, blur_ksize, 0)
    edges = cv2.Canny(blurred_gray, low_threshold, high_threshold)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    stained_glass = np.zeros_like(image)
    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue
        random_color = [random.randint(50, 255) for _ in range(3)]
        cv2.drawContours(stained_glass, [contour], -1, random_color, cv2.FILLED)
    cv2.drawContours(stained_glass, contours, -1, edge_color, edge_thickness)

    return stained_glass


'''result_image = draw_canny_edges('vita.png', color=(0, 0, 255), thickness=3)
cv2.imshow('Edges', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

result_image = blur_except_edges('vita.png', color=(0, 0, 255), thickness=3)
cv2.imshow('Blurred Except Edges', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

result_image = stained_glass_effect('vita.png')
cv2.imshow('Stained Glass Effect', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
