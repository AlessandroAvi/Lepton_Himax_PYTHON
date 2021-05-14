from cv2 import cv2 
import numpy as np 


cap = cv2.VideoCapture('outputVideo.mp4')

while(True):
    ret, frame = cap.read()
 
    cv2.imshow('frame',frame)
    cv2.waitKey(5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()