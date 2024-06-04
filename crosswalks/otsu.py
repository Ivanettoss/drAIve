import cv2

def otsu_thresholding(image_path, output_path):
  image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Ensure grayscale

  # Apply Otsu's thresholding
  _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  cv2.imwrite(output_path, binary_image)

  print(f"Otsu's threshold applied and image saved to: {output_path}")

# Example usage
image_path = "./crosswalks/images/a.jpg"
output_path = "./crosswalks/a.jpg"
otsu_thresholding(image_path, output_path)
