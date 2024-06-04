import cv2
import numpy as np

def first_approch_filter(image_path, output_path):
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the white color range in HSV (Hue, Saturation, Value)
    lower_white = np.array([0, 0, 220], dtype="uint8")
    upper_white = np.array([255, 30, 255], dtype="uint8")

    # Create a mask for white pixels
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Apply the mask to the original image to isolate whites
    result = cv2.bitwise_and(image, image, mask=mask)

    # Save the result image
    cv2.imwrite(output_path, result)
    return

if __name__ == "__main__":
    image_path = "./crosswalks/images/a.jpg"
    output_path = "./crosswalks/2AP1.jpg"
    first_approch_filter(image_path, output_path)