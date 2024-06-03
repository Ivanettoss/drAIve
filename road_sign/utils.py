import os
import shutil

# Function to read YOLO labels from a file
def read_yolo_labels(file_path):
    with open(file_path, 'r') as file:
        labels = file.readlines()
    return [label.strip().split() for label in labels]

# Function to move files to their respective directories
def move_files(file_paths, split_name, image_dir, output_dirs):
    for label_path in file_paths:
        image_filename = os.path.splitext(os.path.basename(label_path))[0] + ".png"
        image_path = os.path.join(image_dir, image_filename)

        if os.path.exists(image_path):
            shutil.move(image_path, output_dirs[split_name]['images'])
            shutil.move(label_path, output_dirs[split_name]['labels'])