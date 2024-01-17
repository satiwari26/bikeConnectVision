import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):   #to initialize the class
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.mpDraw = mp.solutions.drawing_utils
        # Create a DrawingSpec for the connections, color set to red
        self.connection_drawing_spec1 = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2) #to change the color of the dots
        self.connection_drawing_spec = self.mpDraw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2) #to change the color of the lines
    
    def findHands(self, img, draw=True):   #to find the hands
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:   #to get the landmarks of the hand
                if(draw):
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, self.connection_drawing_spec1,self.connection_drawing_spec)
        return img
    
    def findPosition(self, img, handNo=0, draw=False):   #to find the position of the hand
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):   #to get the id and the landmark
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)    #to get the coordinates of the landmarks
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
        return lmList



def main():
    cap = cv2.VideoCapture(0)
    # find the frame rate
    pTime = 0
    cTime = 0
    detector = handDetector()   #to initialize the class
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


    # to get the coordinates of the index and thumb
    # x1 = 0
    # y1 = 0
    # x2 = 0
    # y2 = 0

            #         if id == 4:
            #         cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   #to draw a circle on the thumb
            #         x1 = cx
            #         y1 = cy
            #     if id == 8:
            #         cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)  #to draw a circle on the index finger
            #         x2 = cx
            #         y2 = cy
            # # cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

            # # to find the distance between the index and thumb
            # length = math.hypot(x2-x1, y2-y1)
            # print(length)
            # if length < 20:
            #     cv2.circle(img, (x1,y1), 10, (0,255,0), cv2.FILLED)