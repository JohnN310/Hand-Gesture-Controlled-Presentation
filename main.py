import cv2
import os
from cvzone.HandTrackingModule import HandDetector

#variables 
width, height = 1280, 720
imageNumber = 0
hs, ws = 120, 213
gestureThreshold = 500
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

folderPath = "Hand-Gesture-Controlled-Presentation\Presentation"
# camera set up
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation pngs
pathImages = sorted(os.listdir(folderPath), key = len)
print(pathImages)

# Create a window for the slides
cv2.namedWindow("Slides", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Slides", 1280, 720)  # Set the desired size for the window

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands = 1)


while True:
    # import images
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imageNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False: 
        hand= hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']

        if cy <= gestureThreshold:

            #Gesture 1 - left
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                if imageNumber > 0:
                    buttonPressed = True
                    imageNumber -= 1

             #Gesture 1 - right
            if fingers == [0, 0, 0, 0, 1]:
                print("right")
                if imageNumber < len(pathImages) - 1: 
                    buttonPressed = True
                    imageNumber += 1

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed =False

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws : w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key= cv2.waitKey(1)
    if key == ord('q'):
        break