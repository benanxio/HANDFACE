import cv2
import time
import numpy as np

from HandTrackingModule import HandDetector
from face_detection_video import FaceDetection

kernel = np.ones((5, 5), np.uint8)

wCam, hCam = 1280, 720
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.8, maxHands=2)

while cap.isOpened():

    success, img = cap.read()

    #img = cv2.flip(img, 1)
    
    start = time.time()

    #Deteccion del objeto
    rangomax = np.array([0, 255, 0])
    rangomin = np.array([0, 150, 0])
    mascara = cv2.inRange(img, rangomin, rangomax)
    opening = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    x, y, w, h = cv2.boundingRect(opening)
    #Dibujando rectangulo verde       
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #Dibujando circulo rojo
    cv2.circle(img, (int(x + w / 2), int(y + h / 2)), 5, (0, 0, 255), -1)

    PosAbss = ["","",""]

    #Detecion de manos
    hands, img = detector.findHands(img)
    
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["center"]
        handType1 = hand1["type"]
        fingers1 = detector.fingersUp(hand1)

        # En caso de que haya una mano
        if len(hands) == 1 and handType1 == "Right":
            #PosAbss = ["",fingers1,""]
            PosAbss = ["",handType1,""]
            
        
        else:
            #PosAbss = [fingers1,"",""]
            PosAbss = [handType1,"",""]

        # En caso de que haya dos manos
        if len(hands) == 2:

            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["center"]
            handType2 = hand2["type"]
            fingers2 = detector.fingersUp(hand2)

            if handType1 == "Right":
                #PosAbss = [fingers2,fingers1,""]
                PosAbss = [handType2,handType1,""]

            else:
                #PosAbss = [fingers1,fingers2,""]
                PosAbss = [handType1,handType2,""]


    face_pos,img = FaceDetection(img)

    PosAbss[2] = face_pos[0]

    print(PosAbss)

    end = time.time()
    totalTime = end - start
    fps = 1 / totalTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    

    cv2.imshow("Hand and Face Detection", img)
    cv2.waitKey(1)
