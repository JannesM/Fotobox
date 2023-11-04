import time
from fotobox import Fotobox

# def process_image(img):
#     # convert to gray scale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # detect faces
#     faces = face_detector.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)

#     cv2.imshow("Faces", img)

if __name__ == "__main__":

    fb = Fotobox()

    frame_counter = 0
    previous = time.time_ns()

    while fb.running:
        elapsed = time.time_ns() - previous
        previous = time.time_ns()
        frame_counter += 1

        fb.processInput()

        fb.update(elapsed)

        fb.render()

    fb.cleanup()