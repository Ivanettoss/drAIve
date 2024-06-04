import cv2
import numpy as np

def second_approch_filter(image_path, output_path):
    image = cv2.resize(cv2.imread(image_path), (640, 640))

    # Convert the image to LAB color space for light intensity analysis
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    l_channel = lab_image[:, :, 0]

    # Define tolerance (percentage)
    tolerance = 0.1

    # Create an empty histogram to count intensity occurrences
    hist = np.zeros(256, dtype=np.uint8)

    # Count occurrences in the L channel with tolerance
    for i, pixel in enumerate(l_channel.flat):
      intensity = int(pixel)
      min_value = int(intensity * (1 - tolerance))
      max_value = int(intensity * (1 + tolerance))
      for value in range(max(min_value, 0), min(max_value, 255) + 1):
          hist[value] += 1

    # Find the dominant white intensity with a minimum pixel count threshold
    dominant_intensity = 0
    for i in range(255, -1, -1):
        if hist[i] > 250:
            dominant_intensity = i
            break

    # Create a mask for dominant whites with tolerance
    mask = np.ones_like(l_channel, dtype=np.uint8) * 255
    min_value = int(dominant_intensity * (1 - tolerance))
    max_value = int(dominant_intensity * (1 + tolerance))
    mask[l_channel < min_value] = 0  # Set pixels outside tolerance to black
    mask[l_channel > max_value] = 0  # Set pixels outside tolerance to black

    # Apply the mask to convert dominant whites and others to white/black
    result = cv2.bitwise_and(image, image, mask=mask)

    # Save the result image
    cv2.imwrite(output_path, result)
    return

if __name__ == "__main__":
    # Example usage
    image_path = "./crosswalks/images/a.jpg"
    output_path = "./crosswalks/a.jpg"
    first_approch_filter(image_path, output_path)
