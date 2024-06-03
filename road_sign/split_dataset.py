import os
import shutil
from collections import defaultdict
from sklearn.model_selection import train_test_split

from utils import read_yolo_labels, move_files

def split_dataset(image_dir, label_dir):
    # Paths to the directories
    output_dirs = {
        'train': {
            'images': os.path.join(image_dir, 'train'),
            'labels': os.path.join(label_dir, 'train')
        },
        'test': {
            'images': os.path.join(image_dir, 'test'),
            'labels': os.path.join(label_dir, 'test')
        },
        'val': {
            'images': os.path.join(image_dir, 'val'),
            'labels': os.path.join(label_dir, 'val')
        }
    }

    # Create the output directories if they don't exist
    for split in output_dirs.values():
        os.makedirs(split['images'], exist_ok=True)
        os.makedirs(split['labels'], exist_ok=True)

    file_paths_by_class = defaultdict(list)

    # Collect all label file paths and categorize them by class
    for label_filename in os.listdir(label_dir):
        if label_filename.endswith(".txt"):
            label_path = os.path.join(label_dir, label_filename)
            labels = read_yolo_labels(label_path)
            
            for label in labels:
                class_index = int(label[0])
                file_paths_by_class[class_index].append(label_path)
                break  # Assuming each file is categorized by the first label's class

    # Split the files and move them to respective directories
    for class_index, file_paths in file_paths_by_class.items():
        train_paths, temp_paths = train_test_split(file_paths, test_size=0.2, random_state=42)
        val_paths, test_paths = train_test_split(temp_paths, test_size=0.5, random_state=42)
        
        move_files(train_paths, 'train', image_dir, output_dirs)
        move_files(test_paths, 'test', image_dir, output_dirs)
        move_files(val_paths, 'val', image_dir, output_dirs)

    print("Dataset split into train, test, and validation sets.")