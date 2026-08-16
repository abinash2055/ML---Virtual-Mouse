# import cv2
# import mediapipe as mp
# import pyautogui
# import time
# import math

# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)

# cap = cv2.VideoCapture(0)

# # Gesture Time Control
# click_start_time = None
# click_times = []
# click_cooldown = 0.5
# scroll_mode = False
# freeze_cursor = False

# screen_w, screen_h = pyautogui.size()
# print("\n Hand Mouse Gesture Control")


# prev_screen_x = 0, prev_screen_y = 0, 0


# if not cap.isOpened():
#     print("Cannot Open Camera....")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Cannot Recieve Frame....")
#         break

#     frame = cv2.flip(frame, 1)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb)

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         # Get Finger Tip
#         thumb_tip = hand_landmarks.landmark[4]
#         index_tip = hand_landmarks.landmark[8]
#         middle_tip = hand_landmarks.landmark[12]
#         ring_tip = hand_landmarks.landmark[16]
#         pinky_tip = hand_landmarks.landmark[20]

#         fingers = [
#             1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0
#             for tip in [8, 12, 16, 20]
#         ]

#         # Distance Between Thumb and Index Finger
#         dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)

#         if dist < 0.04:
#             if not freeze_cursor:
#                 freeze_cursor = True
#                 click_times.append(time.time())

#                 # Double Click
#                 if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4:
#                     pyautogui.doubleClick()
#                     cv2.putText(frame, "Double Clicked....", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#                     click_times = []
#                 else:
#                     pyautogui.click()
#                     cv2.putText(frame, "Single Clicked....", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
#         else:
#             freeze_cursor = False



#     cv2.imshow("Live Video....", frame)

#     if cv2.waitKey(1) == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()



# White = (255, 255, 255)
# Black = (0, 0, 0)
# Red   = (0, 0, 255)
# Green = (0, 255, 0)
# Blue  = (255, 0, 0)



import cv2
import mediapipe as mp
import pyautogui
import time
import math

# MediaPipe Setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

model_path = "hand_landmarker.task"

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Cannot Open Camera....")
    exit()

# Screen Setup
screen_w, screen_h = pyautogui.size()
print("\nHand Mouse Gesture Control....")

# Gesture Variables
click_times = []
freeze_cursor = False
prev_screen_x = 0
prev_screen_y = 0

# Hand Connections
connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17)
]

# Start Hand Landmarker
with HandLandmarker.create_from_options(options) as landmarker:
    frame_timestamp = 0

    while True:

        # Read Camera Frame
        ret, frame = cap.read()
        if not ret:
            print("Cannot Recieve Frame....")
            break

        # Flip Camera
        frame = cv2.flip(frame, 1)

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # Frame Timestamp
        frame_timestamp += 1

        # Detect Hand
        result = landmarker.detect_for_video(mp_image, frame_timestamp)

        # If Hand Detected
        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:

                # Draw Green Hand Connections
                for start, end in connections:
                    x1 = int(hand_landmarks[start].x * frame.shape[1])
                    y1 = int(hand_landmarks[start].y * frame.shape[0])
                    x2 = int(hand_landmarks[end].x * frame.shape[1])
                    y2 = int(hand_landmarks[end].y * frame.shape[0])

                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Draw Red Landmarks
                for landmark in hand_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])

                    cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)

                # Get Finger Tips
                thumb_tip = hand_landmarks[4]
                index_tip = hand_landmarks[8]
                middle_tip = hand_landmarks[12]
                ring_tip = hand_landmarks[16]
                pinky_tip = hand_landmarks[20]

                # Finger Detection
                fingers = [
                    1 if hand_landmarks[tip].y < hand_landmarks[tip - 2].y else 0
                    for tip in [8, 12, 16, 20]
                ]

                # Thumb + Index Distance
                distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)

                # Mouse Cursor Movement

                if fingers[0] == 1 and fingers[1] == 0:
                    screen_x = int(index_tip.x * screen_w)
                    screen_y = int(index_tip.y * screen_h)

                    pyautogui.moveTo(screen_x, screen_y, duration=0.05)

                # Click Gesture
                if distance < 0.04:
                    if not freeze_cursor:
                        freeze_cursor = True
                        current_time = time.time()
                        click_times.append(current_time)

                        # Remove old clicks
                        click_times = [ 
                            t for t in click_times
                            if current_time - t < 0.5
                        ]

                        # Double Click

                        if len(click_times) >= 2:
                            pyautogui.doubleClick()
                            cv2.putText(frame,"Double Clicked....", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                            click_times = []

                        else:
                        # Single Click
                            pyautogui.click()
                            cv2.putText(frame, "Single Clicked....", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                else:
                    freeze_cursor = False

        # Display Camera
        cv2.imshow("Live Video....", frame)

        # Quit With Q
        if cv2.waitKey(1) == ord("q"):
            break

# Release Resources
cap.release()
cv2.destroyAllWindows()