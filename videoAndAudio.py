from io import BytesIO
import io
import cv2 
from gtts import gTTS
import pygame
import threading
import queue

pygame.mixer.init()
cap = cv2.VideoCapture('ionutDriving.mp4')
if not cap.isOpened():
    print("Errore nell'aprire il file video")
    exit()

class AudioPlayer:
    def __init__(self):
        self._lock = threading.Lock()
        self._is_playing = False
        self._audio_queue = queue.Queue()
        self._video_finished = False

    def play_audio(self, text):
        # Aggiungi il testo alla coda di riproduzione dell'audio
        self._audio_queue.put(text)

        # Avvia la riproduzione dell'audio se non è già in corso
        with self._lock:
            if not self._is_playing:
                self._is_playing = True
                threading.Thread(target=self._play_audio_thread).start()

    def _play_audio_thread(self):
        while not self._video_finished:
            text = self._audio_queue.get()
            
            # Converti il testo in audio con gTTS
            tts = gTTS(text=text, lang='en')

            # Salva l'audio in un buffer in memoria
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)

            # Carica l'audio dal buffer in memoria
            pygame.mixer.music.load(buf, 'mp3')

            # Riproduci l'audio
            pygame.mixer.music.play()

            # Aspetta che l'audio finisca di suonare
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Se la coda di riproduzione dell'audio è vuota, esci dal loop
            if self._audio_queue.empty():
                with self._lock:
                    self._is_playing = False
                    if self._video_finished:
                        break

# Creiamo un'istanza della classe AudioPlayer
audio_player = AudioPlayer()

def text_to_speech_thread(text):
    audio_player.play_audio(text)

i = 0
while True:
    ret, frame = cap.read()
    i += 1
    if i == 100:
        # Esegui la funzione text_to_speech in un thread separato
        text_to_speech_thread("ciao")

    if not ret:
        # Se il video è finito, impostiamo _video_finished su True per terminare la riproduzione audio
        audio_player._video_finished = True
        break

    # Mostra il frame corrente
    cv2.imshow('Frame', frame)

    # Premi 'q' sulla tastiera per uscire dal loop
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Rilascia il video capture object  Chiudi tutte le finestre
cap.release()
cv2.destroyAllWindows()
