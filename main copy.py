# import cv2
# import mediapipe as mp
# import pyautogui
# import time
# import math


# # ==========================================
# # MediaPipe Setup
# # ==========================================

# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# RunningMode = mp.tasks.vision.RunningMode

# model_path = "hand_landmarker.task"

# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=RunningMode.VIDEO,
#     num_hands=1,
#     min_hand_detection_confidence=0.7,
#     min_hand_presence_confidence=0.7,
#     min_tracking_confidence=0.7
# )


# # ==========================================
# # Camera Setup
# # ==========================================

# cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FPS, 30)

# if not cap.isOpened():
#     print("Cannot Open Camera....")
#     exit()


# # ==========================================
# # Screen Setup
# # ==========================================

# screen_w, screen_h = pyautogui.size()

# print("\nHand Mouse Gesture Control....")


# # ==========================================
# # Gesture Variables
# # ==========================================

# click_times = []
# freeze_cursor = False

# prev_screen_x = 0
# prev_screen_y = 0


# # ==========================================
# # Scroll Variables
# # ==========================================

# scroll_mode = False
# last_scroll_time = 0
# scroll_delay = 0.15


# # ==========================================
# # Screenshot Variables
# # ==========================================

# screenshot_cooldown = 2
# last_screenshot_time = 0


# # ==========================================
# # Right Click Variables
# # ==========================================

# right_click_cooldown = 1
# last_right_click_time = 0


# # ==========================================
# # Drag Variables
# # ==========================================

# dragging = False
# drag_start_time = 0
# drag_threshold = 0.5


# # ==========================================
# # Zoom Variables
# # ==========================================

# previous_zoom_distance = None
# zoom_cooldown = 0.2
# last_zoom_time = 0


# # ==========================================
# # Hand Connections
# # ==========================================

# connections = [
#     (0, 1), (1, 2), (2, 3), (3, 4),
#     (0, 5), (5, 6), (6, 7), (7, 8),
#     (0, 9), (9, 10), (10, 11), (11, 12),
#     (0, 13), (13, 14), (14, 15), (15, 16),
#     (0, 17), (17, 18), (18, 19), (19, 20),
#     (5, 9), (9, 13), (13, 17)
# ]


# # ==========================================
# # Start Hand Landmarker
# # ==========================================

# with HandLandmarker.create_from_options(options) as landmarker:

#     frame_timestamp = 0

#     while True:

#         # ==================================
#         # Read Camera Frame
#         # ==================================

#         ret, frame = cap.read()

#         if not ret:
#             print("Cannot Recieve Frame....")
#             break


#         # ==================================
#         # Flip Camera
#         # ==================================

#         frame = cv2.flip(frame, 1)


#         # ==================================
#         # Convert BGR -> RGB
#         # ==================================

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


#         # ==================================
#         # Create MediaPipe Image
#         # ==================================

#         mp_image = mp.Image(
#             image_format=mp.ImageFormat.SRGB,
#             data=rgb
#         )


#         # ==================================
#         # Timestamp
#         # ==================================

#         frame_timestamp = int(time.time() * 1000)


#         # ==================================
#         # Detect Hand
#         # ==================================

#         result = landmarker.detect_for_video(
#             mp_image,
#             frame_timestamp
#         )


#         # ==================================
#         # If Hand Detected
#         # ==================================

#         if result.hand_landmarks:

#             for hand_landmarks in result.hand_landmarks:

#                 # ==================================
#                 # Draw Connections
#                 # ==================================

#                 for start, end in connections:

#                     x1 = int(
#                         hand_landmarks[start].x *
#                         frame.shape[1]
#                     )

#                     y1 = int(
#                         hand_landmarks[start].y *
#                         frame.shape[0]
#                     )

#                     x2 = int(
#                         hand_landmarks[end].x *
#                         frame.shape[1]
#                     )

#                     y2 = int(
#                         hand_landmarks[end].y *
#                         frame.shape[0]
#                     )

#                     cv2.line(
#                         frame,
#                         (x1, y1),
#                         (x2, y2),
#                         (0, 255, 0),
#                         2
#                     )


#                 # ==================================
#                 # Draw Landmarks
#                 # ==================================

#                 for landmark in hand_landmarks:

#                     x = int(
#                         landmark.x *
#                         frame.shape[1]
#                     )

#                     y = int(
#                         landmark.y *
#                         frame.shape[0]
#                     )

#                     cv2.circle(
#                         frame,
#                         (x, y),
#                         6,
#                         (0, 0, 255),
#                         -1
#                     )


#                 # ==================================
#                 # Finger Tips
#                 # ==================================

#                 thumb_tip = hand_landmarks[4]
#                 index_tip = hand_landmarks[8]
#                 middle_tip = hand_landmarks[12]
#                 ring_tip = hand_landmarks[16]
#                 pinky_tip = hand_landmarks[20]


#                 # ==================================
#                 # Finger Detection
#                 # ==================================

#                 fingers = [
#                     1 if hand_landmarks[tip].y <
#                     hand_landmarks[tip - 2].y
#                     else 0

#                     for tip in [8, 12, 16, 20]
#                 ]


#                 # ==================================
#                 # Thumb + Index Distance
#                 # ==================================

#                 pinch_distance = math.hypot(
#                     thumb_tip.x - index_tip.x,
#                     thumb_tip.y - index_tip.y
#                 )


#                 # ==================================
#                 # Scroll Mode
#                 # ==================================

#                 if sum(fingers) == 4:

#                     scroll_mode = True

#                 else:

#                     scroll_mode = False


#                 # ==================================
#                 # RIGHT CLICK
#                 # Index + Middle Fingers
#                 # ==================================

#                 if fingers[0] == 1 and fingers[1] == 1:

#                     current_time = time.time()

#                     if (
#                         current_time -
#                         last_right_click_time
#                         > right_click_cooldown
#                     ):

#                         pyautogui.rightClick()

#                         cv2.putText(
#                             frame,
#                             "Right Click....",
#                             (10, 170),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,
#                             (255, 0, 255),
#                             2
#                         )

#                         last_right_click_time = current_time


#                 # ==================================
#                 # DRAG & DROP
#                 # ==================================

#                 if pinch_distance < 0.06:

#                     current_time = time.time()

#                     # Start dragging
#                     if not dragging:

#                         if drag_start_time == 0:

#                             drag_start_time = current_time

#                         elif (
#                             current_time -
#                             drag_start_time
#                             > drag_threshold
#                         ):

#                             dragging = True

#                             pyautogui.mouseDown()

#                             cv2.putText(
#                                 frame,
#                                 "Dragging....",
#                                 (10, 210),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 255, 255),
#                                 2
#                             )

#                     # Move while dragging
#                     if dragging:

#                         screen_x = int(
#                             index_tip.x *
#                             screen_w
#                         )

#                         screen_y = int(
#                             index_tip.y *
#                             screen_h
#                         )

#                         pyautogui.moveTo(
#                             screen_x,
#                             screen_y,
#                             duration=0.02
#                         )

#                 else:

#                     # Release mouse
#                     if dragging:

#                         pyautogui.mouseUp()

#                         cv2.putText(
#                             frame,
#                             "Dropped....",
#                             (10, 210),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,
#                             (0, 255, 0),
#                             2
#                         )

#                         dragging = False

#                     drag_start_time = 0


#                 # ==================================
#                 # LEFT CLICK
#                 # ==================================

#                 if (
#                     pinch_distance < 0.06
#                     and not dragging
#                 ):

#                     if not freeze_cursor:

#                         freeze_cursor = True

#                         current_time = time.time()

#                         click_times.append(current_time)


#                         # Remove old clicks
#                         click_times = [
#                             t
#                             for t in click_times
#                             if current_time - t < 0.5
#                         ]


#                         # Double Click
#                         if (
#                             len(click_times) >= 2
#                             and
#                             click_times[-1] -
#                             click_times[-2] < 0.4
#                         ):

#                             pyautogui.doubleClick()

#                             cv2.putText(
#                                 frame,
#                                 "Double Clicked....",
#                                 (10, 50),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 255, 255),
#                                 2
#                             )

#                             click_times = []


#                         # Single Click
#                         else:

#                             pyautogui.click()

#                             cv2.putText(
#                                 frame,
#                                 "Single Clicked....",
#                                 (10, 50),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (255, 255, 0),
#                                 2
#                             )

#                 else:

#                     freeze_cursor = False


#                 # ==================================
#                 # SCROLL ACTION
#                 # ==================================

#                 if scroll_mode:

#                     current_time = time.time()

#                     if (
#                         current_time -
#                         last_scroll_time
#                         > scroll_delay
#                     ):

#                         # Scroll Up
#                         if index_tip.y < 0.4:

#                             pyautogui.scroll(5)

#                             cv2.putText(
#                                 frame,
#                                 "Scroll Up....",
#                                 (10, 90),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 255, 0),
#                                 2
#                             )

#                             last_scroll_time = current_time


#                         # Scroll Down
#                         elif index_tip.y > 0.6:

#                             pyautogui.scroll(-5)

#                             cv2.putText(
#                                 frame,
#                                 "Scroll Down....",
#                                 (10, 90),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 0, 255),
#                                 2
#                             )

#                             last_scroll_time = current_time


#                 # ==================================
#                 # SCREENSHOT
#                 # ==================================

#                 if sum(fingers) == 0:

#                     current_time = time.time()

#                     if (
#                         current_time -
#                         last_screenshot_time
#                         > screenshot_cooldown
#                     ):

#                         pyautogui.screenshot(
#                             f"ScreenShot_{int(current_time)}.png"
#                         )

#                         cv2.putText(
#                             frame,
#                             "ScreenShot Taken....",
#                             (10, 130),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,
#                             (255, 255, 0),
#                             2
#                         )

#                         last_screenshot_time = current_time


#                 # ==================================
#                 # ZOOM IN / OUT
#                 # ==================================

#                 zoom_distance = math.hypot(
#                     index_tip.x - middle_tip.x,
#                     index_tip.y - middle_tip.y
#                 )

#                 current_time = time.time()

#                 if previous_zoom_distance is not None:

#                     difference = (
#                         zoom_distance -
#                         previous_zoom_distance
#                     )

#                     if (
#                         current_time -
#                         last_zoom_time
#                         > zoom_cooldown
#                     ):

#                         # Zoom In
#                         if difference > 0.03:

#                             pyautogui.hotkey(
#                                 "ctrl",
#                                 "+"
#                             )

#                             cv2.putText(
#                                 frame,
#                                 "Zoom In....",
#                                 (10, 250),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 255, 0),
#                                 2
#                             )

#                             last_zoom_time = current_time


#                         # Zoom Out
#                         elif difference < -0.03:

#                             pyautogui.hotkey(
#                                 "ctrl",
#                                 "-"
#                             )

#                             cv2.putText(
#                                 frame,
#                                 "Zoom Out....",
#                                 (10, 250),
#                                 cv2.FONT_HERSHEY_SIMPLEX,
#                                 1,
#                                 (0, 0, 255),
#                                 2
#                             )

#                             last_zoom_time = current_time


#                 previous_zoom_distance = zoom_distance


#                 # ==================================
#                 # MOUSE CURSOR MOVEMENT
#                 # ==================================

#                 if fingers[0] == 1 and fingers[1] == 0:

#                     if (
#                         not freeze_cursor
#                         and not scroll_mode
#                         and not dragging
#                     ):

#                         screen_x = int(
#                             index_tip.x *
#                             screen_w
#                         )

#                         screen_y = int(
#                             index_tip.y *
#                             screen_h
#                         )

#                         pyautogui.moveTo(
#                             screen_x,
#                             screen_y,
#                             duration=0.05
#                         )

#                         prev_screen_x = screen_x
#                         prev_screen_y = screen_y


#         # ==================================
#         # Display Camera
#         # ==================================

#         cv2.imshow(
#             "Live Video....",
#             frame
#         )


#         # ==================================
#         # Quit With Q
#         # ==================================

#         if cv2.waitKey(1) == ord("q"):
#             break


# # ==========================================
# # Release Resources
# # ==========================================

# cap.release()
# cv2.destroyAllWindows()