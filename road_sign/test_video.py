import os
import cv2
from ultralytics import YOLO

# Define paths
VIDEOS_DIR = os.path.join('.', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'a.mp4')
video_path_out = '{}_out.mp4'.format(os.path.splitext(video_path)[0])

# Initialize VideoCapture
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

# Get frame dimensions
H, W, _ = frame.shape

# Initialize VideoWriter
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'XVID'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

# Load YOLO model
model_path = os.path.join('.', 'road_sign', 'model', 'model.pt')
model = YOLO(model_path)

# Detection threshold
threshold = 0.5
i = 0
while ret:
    i += 1
    if i % 2 == 0:
        continue
    # Perform object detection
    results = model(frame)[0]

    # Process detection results
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Write frame to output video
    out.write(frame)

    # Read next frame
    ret, frame = cap.read()
    if i >= 801:
        break

# Release VideoCapture and VideoWriter
cap.release()
out.release()
cv2.destroyAllWindows()
