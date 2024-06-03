import cv2
import numpy as np
import os

from detect import process_image

def create_collage(images, output_path):
    rows = 2
    collage_height = 320 * rows
    collage_width = 960
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    for i, img in enumerate(images):
        row = i // 3
        col = i % 3
        resized_img = cv2.resize(img, (320, 320))

        if len(resized_img.shape) == 2:
            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_GRAY2BGR)

        collage[row * 320:(row + 1) * 320, col * 320:(col + 1) * 320] = resized_img

    cv2.imwrite(output_path, collage)

if __name__ == "__main__":
    input_dir = './crosswalks/images'
    output_dir = './crosswalks/outputs'

    for image_name in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f'Error: Could not open image {image_name}.')
            continue

        (a, _) = process_image(image)
        create_collage([image] + a, os.path.join(output_dir, image_name))
        print(image_name)

    print("Processing completed. Check the './outputs' folder for results.")
