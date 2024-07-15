import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

# Open video capture (use 0 for webcam)
cap = cv2.VideoCapture("Resources/Videos/20240715_151426 (1).mp4")  # Replace with 0 for webcam

# Check if the capture was successful
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

detector = PoseDetector()

shirtFolderPath = "Resources/Shirts/Hasta_la-removebg-preview (1).png"
#listShirts = os.listdir(shirtFolderPath)
jacketWidth = 440
jacketHeight = 581
fixedRatio = jacketHeight / jacketWidth
jacketRatioHeightWidth = jacketHeight / jacketWidth

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    #img = cv2.flip(img, 1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        # center = bboxInfo["center"]
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt = cv2.imread(shirtFolderPath, cv2.IMREAD_UNCHANGED)
        widthOfJacket = int((lm11[0] - lm12[0]) * fixedRatio)
        currentScale = int((lm11[0] - lm12[0])) / 190
        offset = int(44 * currentScale), int(48 * currentScale)
        print(widthOfJacket)
        imgJacketResized = cv2.resize(imgShirt, (widthOfJacket, int(widthOfJacket * jacketRatioHeightWidth)))

        try:
            img = cvzone.overlayPNG(img, imgJacketResized, (lm12[0]-offset[0], lm12[1]-offset[1]))
        except:
            pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)