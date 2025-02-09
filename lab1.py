import cv2
import numpy as np

# Глобальные переменные
drawing = False  # True, если мышка зажата
x_start, y_start, x_end, y_end = -1, -1, -1, -1  # Координаты области

# Функция обновления изображения в зависимости от положения трекбара
def update(val):
    if x_start == -1 or y_start == -1 or x_end == -1 or y_end == -1:
        return

    alpha = val / 100.0  # Преобразуем значение трекбара (от 0 до 100) в коэффициент (от 0.0 до 1.0)

    # Преобразование области в монохром
    gray_half = cv2.cvtColor(image[y_start:y_end, x_start:x_end], cv2.COLOR_BGR2GRAY)
    gray_half_bgr = cv2.cvtColor(gray_half, cv2.COLOR_GRAY2BGR)

    # Создание нового изображения, где часть области - это комбинация цветного и монохромного
    blended_half = cv2.addWeighted(image[y_start:y_end, x_start:x_end], 1 - alpha, gray_half_bgr, alpha, 0)

    # Замена части изображения на изменённую область
    modified_image = image.copy()
    modified_image[y_start:y_end, x_start:x_end] = blended_half

    # Показ изменённого изображения
    cv2.imshow('Modified Image', modified_image)

# Функция для обработки событий мыши
def draw_rectangle(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, drawing

    # Начало рисования прямоугольника
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y

    # Обновление координат по мере перемещения мыши
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x_end, y_end = x, y
            # Показываем область выделения на изображении в реальном времени
            temp_image = image.copy()
            cv2.rectangle(temp_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.imshow('Modified Image', temp_image)

    # Завершение рисования
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y
        # Обновляем изображение с изменениями
        update(cv2.getTrackbarPos('Strength', 'Modified Image'))

# Загрузка изображения
image = cv2.imread('vita1.png')

# Создание окна для отображения изображения и трекбара
cv2.namedWindow('Modified Image')
cv2.setMouseCallback('Modified Image', draw_rectangle)

# Добавление трекбара для управления силой преобразования
cv2.createTrackbar('Strength', 'Modified Image', 0, 100, update)

# Отображение исходного изображения
cv2.imshow('Modified Image', image)

# Ожидание завершения работы
cv2.waitKey(0)
cv2.destroyAllWindows()
