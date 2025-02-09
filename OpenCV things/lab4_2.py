import cv2
import numpy as np

ref_point = []
cropped_img = None
original_image = None


def click_and_crop(event, x, y, flags, param):
    global ref_point, cropped_img, original_image

    if event == cv2.EVENT_LBUTTONDOWN:  # Клик мыши - начальная точка
        ref_point = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:  # Отпускание мыши - конечная точка
        ref_point.append((x, y))
        cv2.rectangle(param, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Road Turn Detection", param)

        x1, y1 = ref_point[0]
        x2, y2 = ref_point[1]
        cropped_img = param[y1:y2, x1:x2]

        detect_road_turn(cropped_img)


def detect_road_turn(img):
    """
    Детекция поворота дороги на основе анализа линий в выделенной области.
    """
    global original_image

    if img is None or img.size == 0:
        print("Ошибка: область не была выделена корректно.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    left_angles = []
    right_angles = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            if -45 < angle < -10:  # Линия наклонена вправо
                left_angles.append(angle)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            elif 10 < angle < 45:  # Линия наклонена влево
                right_angles.append(angle)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Определяем направление поворота
    if len(left_angles) > len(right_angles) * 1.5:
        turn = "Left Turn"
    elif len(right_angles) > len(left_angles) * 1.5:
        turn = "Right Turn"
    else:
        turn = "Straight Road"

    # Генерируем информацию об углах и расчетах
    left_mean_angle = np.mean(left_angles) if left_angles else 0
    right_mean_angle = np.mean(right_angles) if right_angles else 0
    debug_info = f"Left Mean Angle: {left_mean_angle:.2f}\nRight Mean Angle: {right_mean_angle:.2f}"

    cv2.putText(img, f"Turn: {turn}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, debug_info, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow("Detected Area", img)


def clear_image():
    global original_image
    cv2.imshow("Road Turn Detection", original_image.copy())


image_path = "road4.jpeg"
original_image = cv2.imread(image_path) 
original_image = cv2.resize(original_image, (640, 480)) 
cv2.imshow("Road Turn Detection", original_image)
cv2.setMouseCallback("Road Turn Detection", click_and_crop, param=original_image.copy()) 

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  
        clear_image()
    elif key == ord('q'):  
        break

cv2.destroyAllWindows()
