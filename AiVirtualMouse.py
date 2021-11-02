import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

##################################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 5
##################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
#print(wScr, hScr)


while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox =detector.findPosition(img)
    # 2. Get the tip of the index and middle finger
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x4, y4 = lmlist[4][1:]
        #print(x1, y1, x2, y2, x4, y4)

        # 3. Check Which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:


         # Thumb
         if fingers[0] == 0:
             pyautogui.scroll(300)
             print('up')
        else:
            if fingers[0] == 1 :
             pyautogui.scroll(-200)
            print('down')


            # 5. Convert Coordinates

            x3 = np.interp(x1, (frameR ,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR),(0,hScr))

            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening


            # 7. Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find the distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img,(lineInfo[4], lineInfo[5])
                           ,15,(0,255,0),cv2.FILLED)
                pyautogui.leftClick() and pyautogui.displayMousePosition(int=0)
            #else:
                #if length < 50:
                    #cv2.circle(img, (lineInfo[4], lineInfo[5])
                               #, 15, (0, 255, 0), cv2.FILLED)
                    #pyautogui.rightClick() and pyautogui.displayMousePosition(int=0)



    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)