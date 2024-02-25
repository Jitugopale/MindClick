from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import time
import random
import pyttsx3
import os
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import pygame
import numpy as np

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Initialize pygame
pygame.init()

# Initialize mixer
mixer = pygame.mixer
mixer.init()

# Initialize screen
screen = pygame.display.set_mode((640, 480))

# Initialize detection variables
thresh = 0.25
frame_check = 20
drowsy_start_time = None
drowsy_alert_interval = 10

# Initialize dlib face detector and shape predictor
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define facial landmarks indices
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Initialize OpenCV camera capture
cap = cv2.VideoCapture(0)

# Initialize global variables
flag = 0

class DrowsyDetectionApp(App):
    def build(self):
        self.alert_system_running = False
        self.detection_running = False

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        heading_label = Label(text='Detection and Alert System', font_size=20, bold=True)
        start_detection_button = Button(text='Start Detection', on_press=self.start_detection)
        stop_detection_button = Button(text='Stop Detection', on_press=self.stop_detection)
        start_alert_button = Button(text='Start Alert System', on_press=self.start_alert_system)
        stop_alert_button = Button(text='Stop Alert System', on_press=self.stop_alert_system)

        layout.add_widget(heading_label)
        layout.add_widget(start_detection_button)
        layout.add_widget(stop_detection_button)
        layout.add_widget(start_alert_button)
        layout.add_widget(stop_alert_button)

        return layout

    def start_detection(self, instance):
        if not self.detection_running:
            self.detection_running = True
            Clock.schedule_interval(self.detect_drowsiness, 1)

    def stop_detection(self, instance):
        if self.detection_running:
            self.detection_running = False
            Clock.unschedule(self.detect_drowsiness)

    def start_alert_system(self, instance):
        if not self.alert_system_running:
            self.alert_system_running = True
            self.start_time_music = time.time()
            self.start_time_speech = time.time()
            self.elapsed_time_music = 0
            self.elapsed_time_speech = 0
            self.music_folder = "sounds"
            self.alert_interval_music_seconds = 180
            self.alert_interval_speech_seconds = 120
            Clock.schedule_interval(self.random_alert, 1)

    def stop_alert_system(self, instance):
        if self.alert_system_running:
            self.alert_system_running = False
            Clock.unschedule(self.random_alert)

    def detect_drowsiness(self, dt):
        global drowsy_start_time, flag
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < thresh:
                flag += 1
                print(flag)
                if flag >= frame_check:
                    if drowsy_start_time is None:
                        drowsy_start_time = time.time()
                    elif time.time() - drowsy_start_time >= drowsy_alert_interval:
                        cv2.putText(frame, "****************ALERT!****************", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "****************ALERT!****************", (10, 325),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        mixer.music.load("alert.mp3")  # Load the alert sound here
                        mixer.music.play()
                        drowsy_start_time = None
            else:
                flag = 0

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()

    def random_alert(self, dt):
        elapsed_time_music = time.time() - self.start_time_music
        if elapsed_time_music >= self.alert_interval_music_seconds and elapsed_time_music % self.alert_interval_music_seconds < 1:
            self.play_random_music(self.music_folder)

        elapsed_time_speech = time.time() - self.start_time_speech
        if elapsed_time_speech >= self.alert_interval_speech_seconds and elapsed_time_speech % self.alert_interval_speech_seconds < 1:
            self.display_and_speak_time(elapsed_time_speech)

    def play_random_music(self, music_folder):
        music_files = [file for file in os.listdir(music_folder) if file.endswith(('.mp4', '.wav'))]
        if music_files:
            random_music = random.choice(music_files)
            music_path = os.path.join(music_folder, random_music)
            mixer.music.load(music_path)
            mixer.music.play()
        else:
            print("No music files found in the specified folder.")

    def display_and_speak_time(self, elapsed_time):
        minutes, seconds = divmod(elapsed_time, 60)
        time_str = "{:02}:{:02}".format(int(minutes), int(seconds))
        speak_message = f"You have traveled since {int(minutes)} minute{'s' if int(minutes) > 1 else ''} ago. Take some rest."
        print("Time Elapsed: {}".format(time_str))
        engine.say(speak_message)
        engine.runAndWait()

if __name__ == '__main__':
    DrowsyDetectionApp().run()
