import xml.etree.ElementTree as ET
import os

def normalize_annotation(input_dir, output_dir):
    class_mapping = {
        "trafficlight": 0,
        "stop": 1,
        "speedlimit": 2,
        "crosswalk": 3
    }
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            # Parse XML file
            tree = ET.parse(os.path.join(input_dir, filename))
            root = tree.getroot()

            # Get image size
            size = root.find("size")
            width = int(size.find("width").text)
            height = int(size.find("height").text)

            yolo_annotation = ""

            # Process each object
            for obj in root.findall("object"):
                class_name = obj.find("name").text
                class_index = class_mapping.get(class_name)

                if class_index is not None:
                    bbox = obj.find("bndbox")
                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)

                    # Convert coordinates to YOLO format
                    x_center = (xmin + xmax) / 2 / width
                    y_center = (ymin + ymax) / 2 / height
                    box_width = (xmax - xmin) / width
                    box_height = (ymax - ymin) / height

                    # Append YOLO annotation to the string
                    yolo_annotation += f"{class_index} {x_center} {y_center} {box_width} {box_height}\n"

            # Write YOLO annotation to file
            output_filename = os.path.splitext(filename)[0] + ".txt"
            with open(os.path.join(output_dir, output_filename), "w") as f:
                f.write(yolo_annotation)