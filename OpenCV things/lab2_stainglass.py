import cv2
import numpy as np
from sklearn.cluster import KMeans

image = cv2.imread('vita.png')
resized_image = cv2.resize(image, (800, 800))
pixels = resized_image.reshape(-1, 3)
kmeans = KMeans(n_clusters=10, random_state=42).fit(pixels)
labels = kmeans.labels_
clustered_image = kmeans.cluster_centers_[labels].reshape(resized_image.shape).astype(np.uint8)
palette = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (128, 0, 128), (255, 128, 0), (128, 128, 0),
    (0, 128, 128), (128, 0, 0), (0, 128, 0),
    (0, 0, 128), (255, 255, 255), (0, 0, 0)
]
stained_glass = np.zeros_like(clustered_image)
for i in range(len(palette)):
    stained_glass[labels.reshape(resized_image.shape[:2]) == i] = palette[i]

gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(stained_glass, contours, -1, (0, 0, 0), thickness=2)

cv2.imshow('Original Image', resized_image)
cv2.imshow('Stained Glass Effect', stained_glass)
cv2.waitKey(0)
cv2.destroyAllWindows()
