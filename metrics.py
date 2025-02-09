import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt


# Функция для добавления аддитивного нормального шума
def add_gaussian_noise(image, sigma):
    noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
    noisy_image = cv2.add(image.astype(np.float32), noise)
    noisy_image = np.clip(noisy_image, 0, 255)  # Ограничение значений на 0-255
    return noisy_image.astype(np.uint8)


# Функции для вычисления MSE и PSNR
def calculate_mse(original, noisy):
    return np.mean((original - noisy) ** 2)


def calculate_psnr(original, noisy):
    mse = calculate_mse(original, noisy)
    return 10 * np.log10((255 ** 2) / mse) if mse != 0 else float('inf')


# Загрузка изображения
image_path = 'your_image.jpg'
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Диапазон значений сигмы (степень зашумленности)
sigma_values = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Списки для хранения значений метрик
mse_values = []
psnr_values = []
ssim_values = []

# Вычисление метрик для каждого значения сигмы
for sigma in sigma_values:
    noisy_image = add_gaussian_noise(original_image, sigma)
    mse = calculate_mse(original_image, noisy_image)
    psnr = calculate_psnr(original_image, noisy_image)
    similarity = ssim(original_image, noisy_image, data_range=noisy_image.max() - noisy_image.min())

    mse_values.append(mse)
    psnr_values.append(psnr)
    ssim_values.append(similarity)

    # Отображение изображений при необходимости
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title(f"Original Image")
    plt.imshow(original_image, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.title(f"Noisy Image with sigma={sigma}")
    plt.imshow(noisy_image, cmap='gray')
    plt.show()

# Вывод значений метрик
for i, sigma in enumerate(sigma_values):
    print(f"Sigma={sigma}: MSE={mse_values[i]:.2f}, PSNR={psnr_values[i]:.2f} dB, SSIM={ssim_values[i]:.4f}")
