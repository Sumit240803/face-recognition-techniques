import cv2
prototxt_path = "deploy.prototxt"
model_path = "res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt_path ,model_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

f_count = 0
while True:
    ret,frame = cap.read()
    if not ret: 
        break
    f_count+=1
    if f_count%2==0:
        continue
    h,w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame,scalefactor=1.0,size=(300,300),mean=(104.0,177.0,123.0))
    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > 0.5:
            box = detections[0,0,i,3:7]*[w,h,w,h]
            (startX,startY,endX,endY) = box.astype("int")
            cv2.rectangle(frame,(startX,startY),(endX , endY),(0,255,0),3)
        cv2.imshow("Face Detection",frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cap.release()
cv2.destroyAllWindows()
