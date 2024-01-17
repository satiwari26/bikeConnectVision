import cv2
import mediapipe as mp
import time
import math
import handTracking as ht

class gestureControl():

    def __init__(self, TindexPress = False, TmiddlePress = False, TringPress = False, TpinkyPress = False):
        #creating state variables for each finger approximity
        self.TindexPress = TindexPress
        self.TmiddlePress = TmiddlePress
        self.TringPress = TringPress
        self.TpinkyPress = TpinkyPress

    def identifyfingers(self,img, lmList):
        if len(lmList) != 0:
            # print(lmList[4])
            id,cx, cy = lmList[4]
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the thumb
            id,cx, cy = lmList[8]
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the index finger
            id,cx, cy = lmList[12]
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the middle finger
            id,cx, cy = lmList[16]
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the ring finger
            id,cx, cy = lmList[20]
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the pinky finger

    def identifyGesture(self,img, lmList):
        if len(lmList) != 0:
            id,cxThumb, cyThumb = lmList[4]
            id,cxIndex, cyIndex = lmList[8]
            id,cxMiddle, cyMiddle = lmList[12]
            id,cxRing, cyRing = lmList[16]
            id,cxPinky, cyPinky = lmList[20]
            Tindex = math.hypot(cxThumb-cxIndex, cyThumb-cyIndex)
            Tmiddle = math.hypot(cxThumb-cxMiddle, cyThumb-cyMiddle)
            Tring = math.hypot(cxThumb-cxRing, cyThumb-cyRing)
            Tpinky = math.hypot(cxThumb-cxPinky, cyThumb-cyPinky)

            if Tindex < 50:
                cv2.circle(img, (cxIndex,cyIndex), 10, (0,255,0), cv2.FILLED)
                self.TindexPress = True
            elif Tindex > 50 and self.TindexPress == True:
                print("Index Finger Pressed")
                self.TindexPress = False
            if Tmiddle < 50:
                cv2.circle(img, (cxMiddle,cyMiddle), 10, (0,255,0), cv2.FILLED)
                self.TmiddlePress = True
            elif Tmiddle > 50 and self.TmiddlePress == True:
                print("Middle Finger Pressed")
                self.TmiddlePress = False
            if Tring < 50:
                cv2.circle(img, (cxRing,cyRing), 10, (0,255,0), cv2.FILLED)
                self.TringPress = True
            elif Tring > 50 and self.TringPress == True:
                print("Ring Finger Pressed")
                self.TringPress = False
            if Tpinky < 50:
                cv2.circle(img, (cxPinky,cyPinky), 10, (0,255,0), cv2.FILLED)
                self.TpinkyPress = True
            elif Tpinky > 50 and self.TpinkyPress == True:
                print("Pinky Finger Pressed")
                self.TpinkyPress = False

def main():
    cap = cv2.VideoCapture(0)
    # find the frame rate
    pTime = 0
    cTime = 0
    controller = gestureControl()   #to initialize the class
    detector = ht.handDetector()   #to initialize the class
    while True:
        success, img = cap.read()
        img = detector.findHands(img)   #to find the hands
        lmList = detector.findPosition(img)   #to find the position of the hand
        controller.identifyfingers(img, lmList)
        controller.identifyGesture(img, lmList)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,'FPS: ' + str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)   #to display the frame rate

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()