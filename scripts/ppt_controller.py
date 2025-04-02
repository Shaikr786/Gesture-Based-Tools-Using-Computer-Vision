import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Cooldown time for actions
last_action_time = 0
cooldown_time = 1.0  # 1 second

def count_fingers(hand_landmarks):
    """ Detect which fingers are up based on landmark positions. """
    finger_states = [0, 0, 0, 0, 0]  # Thumb to pinky
    finger_tips = [4, 8, 12, 16, 20]  # Index of tip landmarks

    # Check if fingers are up
    for i in range(1, 5):  # 1-4 for fingers (not thumb)
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_tips[i] - 2].y:
            finger_states[i] = 1

    # Thumb detection (adjust based on left/right hand)
    if hand_landmarks.landmark[finger_tips[0]].x > hand_landmarks.landmark[finger_tips[0] - 1].x:
        finger_states[0] = 1

    return finger_states

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Error accessing webcam.")
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(hand_landmarks)

            current_time = time.time()

            if fingers == [1, 1, 1, 1, 1]:
                cv2.putText(img, "Next Slide", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press("right")
                    last_action_time = current_time

            elif fingers == [1, 0, 0, 0, 0]:
                cv2.putText(img, "Previous Slide", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press("left")
                    last_action_time = current_time

            elif fingers == [0, 1, 1, 0, 0]:
                cv2.putText(img, "Zoom In", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.hotkey("ctrl", "+")
                    last_action_time = current_time

            elif fingers == [0, 1, 0, 0, 0]:
                cv2.putText(img, "Zoom Out", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.hotkey("ctrl", "-")
                    last_action_time = current_time

            elif fingers == [1, 1, 0, 0, 0]:
                cv2.putText(img, "Start Presentation", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press("f5")
                    last_action_time = current_time

            elif fingers == [0, 1, 1, 1, 0]:
                cv2.putText(img, "Stop Presentation", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press("esc")
                    last_action_time = current_time

            else:
                cv2.putText(img, "Gesture Not Recognized", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("PPT Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
