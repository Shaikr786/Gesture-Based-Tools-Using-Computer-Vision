
import cv2
import mediapipe as mp
import threading
import math
import time
import pyautogui  # Importing pyautogui for keyboard simulation

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Keyboard layout
keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "^", "$"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "%", "*"],
        ["W", "X", "C", "V", "B", "N", ",", ";", ":", "!", ".", "?"]]

finalText = ""
clicked = False

# Button class for keyboard drawing
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

buttonList.append(Button([50, 350], "Space", [885, 85]))
buttonList.append(Button([950, 350], "Delete", [285, 85]))


# Function to detect hand landmarks
def handLandmarks(colorImg):
    landmarkList = []
    colorImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2RGB)
    landmarkPositions = hands.process(colorImg)
    if landmarkPositions.multi_hand_landmarks:
        for hand in landmarkPositions.multi_hand_landmarks:
            mp_drawing.draw_landmarks(colorImg, hand, mp_hands.HAND_CONNECTIONS)
            for index, landmark in enumerate(hand.landmark):
                landmarkList.append([index, int(landmark.x * 1280), int(landmark.y * 720)])
    return landmarkList, colorImg


# Function to draw all buttons on the image
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if button.text == "Space" or button.text == "Delete":
            cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
            text_x = x + int(w * 0.35) - 50
            text_y = y + int(h * 0.65)
            cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
            cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to simulate key press with pyautogui
def simulate_key_press(key):
    if key == "Space":
        pyautogui.press('space')  # Simulate spacebar key press
    elif key == "Delete":
        pyautogui.press('backspace')  # Simulate backspace key press
    else:
        pyautogui.write(key)  # Simulate the character as typed


# Function to run the virtual keyboard
def run_virtual_keyboard():
    global finalText, clicked
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Timestamp to manage debounce time
    last_tap_time = time.time()

    while True:  # Check if stop event is set
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        lmlist, img_with_landmarks = handLandmarks(img)
        img_with_landmarks = drawAll(img_with_landmarks, buttonList)

        if lmlist:
            # Detect Pinch (Tap Gesture)
            thumb_tip = (lmlist[4][1], lmlist[4][2])  # Thumb tip position
            index_tip = (lmlist[8][1], lmlist[8][2])  # Index finger tip position
            distance = calculate_distance(thumb_tip, index_tip)

            current_time = time.time()

            # Check if the distance is below the threshold for tap gesture
            if distance < 50:  # Threshold for tap gesture (you can adjust this threshold)
                # Check if enough time has passed since the last tap (debouncing)
                if current_time - last_tap_time > 0.3:  # Debounce time (0.3 seconds)
                    last_tap_time = current_time  # Update last tap time

                    for button in buttonList:
                        x, y = button.pos
                        w, h = button.size
                        if x < lmlist[8][1] < x + w and y < lmlist[8][2] < y + h:
                            # Trigger action when the index finger taps a button
                            if button.text == "Space":
                                finalText += " "
                                simulate_key_press("Space")  # Simulate the Space key press
                            elif button.text == "Delete":
                                finalText = finalText[:-1]
                                simulate_key_press("Delete")  # Simulate the Delete (Backspace) key press
                            else:
                                finalText += button.text
                                simulate_key_press(button.text)  # Simulate the corresponding letter key press

                            # Provide feedback by highlighting the button
                            cv2.rectangle(img_with_landmarks, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
                            cv2.putText(img_with_landmarks, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4,
                                        (255, 255, 255), 4)

        # Display the final text on the image
        cv2.rectangle(img_with_landmarks, (50, 580), (1235, 680), (64, 64, 64), cv2.FILLED)
        cv2.putText(img_with_landmarks, finalText, (60, 645), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

        # Show the image with hand landmarks
        cv2.imshow('Virtual Keyboard', img_with_landmarks)

        # Wait for key press to close the OpenCV window
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Esc key or q to exit
            break

    cap.release()
    cv2.destroyAllWindows()
run_virtual_keyboard()

