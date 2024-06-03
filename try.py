import cv2
import pyttsx3

# Function to initialize text-to-speech engine
def init_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    return engine

# Function to speak the provided text
def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()

# Function to process the video
def process_video(video_path):
    # Initialize the text-to-speech engine
    engine = init_tts_engine()

    # Open the video capture
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        if not ret:
            break

        # Increment frame count
        frame_count += 1

        # Speak "Hello" every 300 frames
        if frame_count % 300 == 0:
            speak_text(engine, "Hello")

        # Display the frame
        cv2.imshow("Video", frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "./videos/a.mp4"
    process_video(video_path)
