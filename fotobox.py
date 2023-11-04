import cv2
from cv2.data import haarcascades

import math

MAIN_WINDOW_NAME = "Fotobox"

STATE_IDLE = 0
STATE_COUNTDOWN = 1
STATE_PRESENT = 2


class Fotobox:

    running: bool
    state: int
    countdown: int

    camera: cv2.VideoCapture
    face_detector: cv2.CascadeClassifier

    frame: cv2.Mat
    take: cv2.Mat

    def __init__(self) -> None:
        self.state = STATE_IDLE
        self.running = True
        self.countdown = 0

        self.camera = cv2.VideoCapture(0)
        self.face_detector = cv2.CascadeClassifier(
            haarcascades + "haarcascade_frontalface_default.xml")

        cv2.namedWindow(MAIN_WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            MAIN_WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

    def processInput(self):
        key = cv2.pollKey()

        if key == ord('q'):
            self.running = False

        elif key == ord('m'):
            self.state = STATE_COUNTDOWN
            self.countdown = 3

    def update(self, deltaTime: int):

        # Capture frame-by-frame
        ret, img = self.camera.read()

        # if frame is read correctly ret is True
        if not ret:
            raise "Can't receive frame (stream end?)"

        if self.countdown > 0:
            self.countdown -= (deltaTime / 1e9)

        # update based on state
        if self.state == STATE_IDLE:
            self.frame = img.copy()
            cv2.putText(self.frame, f"Press M to take a picture", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        elif self.state == STATE_COUNTDOWN:
            self.frame = img.copy()
            cv2.putText(self.frame, f"{math.ceil(self.countdown)}", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if self.countdown <= 0:
                self.take = img.copy()
                self.countdown = 3
                self.state = STATE_PRESENT

        elif self.state == STATE_PRESENT:
            self.frame = cv2.cvtColor(self.take, cv2.COLOR_BGR2GRAY)

            if self.countdown <= 0:
                self.state = STATE_IDLE

    def render(self):
        # Display the resulting frame
        cv2.imshow(MAIN_WINDOW_NAME, self.frame)

    def cleanup(self):
        # When everything done, release the capture
        print("Exiting...")
        self.camera.release()
        cv2.destroyAllWindows()
