import cv2
import mediapipe as mp
import time
import math
import handTracking as ht


def main():
    cap = cv2.VideoCapture(0)
    # find the frame rate
    pTime = 0
    cTime = 0
    detector = ht.handDetector()   #to initialize the class
    while True:
        success, img = cap.read()
        img = detector.findHands(img)   #to find the hands
        lmList = detector.findPosition(img)   #to find the position of the hand
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,'FPS: ' + str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)   #to display the frame rate

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()