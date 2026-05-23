import cv2
import mediapipe as mp
import serial
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# COM порт Arduino
arduino = serial.Serial(
    'COM4',
    9600
)

time.sleep(2)

base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(
    options
)

cap = cv2.VideoCapture(0)

# защита от повторной отправки
gesture_sent = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(
        mp_image
    )

    text = "SHOW HAND"

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        opened = 0

        for i in [8, 12, 16, 20]:

            if hand[i].y < hand[i - 2].y:
                opened += 1

        # ладонь
        if opened >= 3:

            text = "OPEN"

            if gesture_sent == False:

                arduino.write(b'1')

                print("COMMAND SENT")

                gesture_sent = True

        # кулак
        else:

            text = "READY"

    else:

        # сброс после убирания руки
        gesture_sent = False

    cv2.putText(
        frame,
        text,
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        3
    )

    cv2.imshow(
        "Curtain Control",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()

arduino.close()

cv2.destroyAllWindows()