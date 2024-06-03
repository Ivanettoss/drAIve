from ultralytics import YOLO

# Load the model
model = YOLO('yolov8n.pt')

# Train the model
model.train(data='./archive/data.yaml', epochs=200, imgsz=640)

# Evaluate the model
metrics = model.val(data='./archive/data.yaml', split='test')

# Print metrics
print(metrics)