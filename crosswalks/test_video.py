import os
import cv2
from detect import process_image

# Define paths
VIDEOS_DIR = os.path.join('.', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'nightR.mp4')
video_path_out = '{}_out.mp4'.format(os.path.splitext(video_path)[0])

# Initialize VideoCapture
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

# Get frame dimensions
H, W, _ = frame.shape

# Initialize VideoWriter
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'XVID'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


# Detection threshold
threshold = 0.5
i = 0
while ret:
    i += 1
    if i%4 != 0:
        ret, frame = cap.read()
        continue
    # Perform object detection
    results = process_image(frame.copy())[1]
    for result in results:
        x_min, y_min, w, h = result
        cv2.rectangle(frame, (x_min, y_min), (x_min + w, y_min + h), (0, 255, 0), 2)
    out.write(frame)

    # Read next frame
    ret, frame = cap.read()
    print(i)
# Release VideoCapture and VideoWriter
cap.release()
out.release()
cv2.destroyAllWindows()
