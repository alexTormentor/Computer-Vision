import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

def detect_horizon(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    horizon_text = "Линии не найдены."

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # Проверяем, является ли линия горизонтальной
            if abs(angle) < 10:  # Угол менее 10 градусов считается горизонтальным
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                if abs(angle) > 5:
                    horizon_text = f"Горизонт завален: угол {angle:.2f} градусов."
                else:
                    horizon_text = f"Горизонт горизонтален: угол {angle:.2f} градусов."
                break
        else:
            horizon_text = "Горизонтальная линия не найдена."
    return img, horizon_text

def display_horizon(image_path):
    img, horizon_text = detect_horizon(image_path)
    root = tk.Tk()
    root.title("Horizon Detector")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    label_img = tk.Label(root, image=img_tk)
    label_img.pack()

    label_text = tk.Label(root, text=horizon_text, font=("Arial", 14))
    label_text.pack()

    root.mainloop()

display_horizon("city3.jpg")