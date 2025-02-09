import cv2

def create_panorama(image_paths):
    images = [cv2.imread(path) for path in image_paths]
    for i, img in enumerate(images):
        if img is None:
            print(f"Error: Could not load image at {image_paths[i]}")
            return

    stitcher = cv2.Stitcher_create()
    status, panorama = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        cv2.imshow("Panorama", panorama)
        cv2.imwrite("panorama_result.jpg", panorama)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Error during stitching: {status}")

image_files = ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg"]
create_panorama(image_files)
