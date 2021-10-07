import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def FaceDetection(img,draw=True):

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)

        #Deteccion de posicion de rostro
        pos = []

        if results.detections is not None:
            for detection in results.detections:

                bBox = detection.location_data.relative_bounding_box

                if bBox.xmin< 0.39:
                    pos = [[1,0,0],bBox.xmin,"RIGHT"]
                elif bBox.xmin> 0.42:
                    pos = [[0,0,1],bBox.xmin,"LEFT"]
                else:
                    pos = [[0,1,0],bBox.xmin,"CENTER"]

                if draw:
                    mp_drawing.draw_detection(
                    img,
                    detection,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 255)),
                    )
                    h, w, c = img.shape
                    boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                    cv2.putText(img, f'{int(detection.score[0]*100)}% {pos[2]}', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)                       

        else:
            pos = [[0,1,0],"","Centro"]
   
        return pos,img

def punto(img,posicion,i):

    h, w, c = img.shape
    x = int(posicion.location_data.relative_keypoints[i].x * w)
    y = int(posicion.location_data.relative_keypoints[i].y * h)

    return x,y

def main():
    wCam, hCam = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while cap.isOpened():

        success, img = cap.read()
        Face_Position,img = FaceDetection(img)
        #print(Face_Position)
        
        cv2.imshow("Face Detection", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()