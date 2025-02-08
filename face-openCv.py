import cv2
import cv2.data

face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    faces = face.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5,minSize=(30,30))

    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
    cv2.imshow("Live Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()