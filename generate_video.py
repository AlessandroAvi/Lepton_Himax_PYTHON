from cv2 import cv2 
import glob
import numpy as np 

path = "C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Himax/*"
images_path = glob.glob(r"C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Himax/*.bmp")
images_path.sort()

h = 122
w = 164
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('outputVideo.mp4', fourcc,10,(w,h))



for img_path in images_path:
    print(img_path[len(path)-1:])
    img = cv2.imread(img_path)
    print(img.shape)
    video.write(img)
video.release()

print("Video out ")





