from cv2 import cv2 
import glob
import numpy as np 

path = "C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Merge/*"
images_path = glob.glob(r"C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Merge/*.bmp")

pathL = "C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Lepton/*"
images_pathL = glob.glob(r"C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Lepton/*.bmp")

pathH = "C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Himax/*"
images_pathH = glob.glob(r"C:/Users/massi/OneDrive/Documenti/STM32 projects/Termocamera_UART_py/Capture/Himax/*.bmp")


images_path.sort()
images_pathL.sort()
images_pathH.sort()

h = 122
w = 164
hL = 60
wL = 80

fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('Merge.mp4', fourcc,5,(w,h))

fourccL = cv2.VideoWriter_fourcc(*'mp4v') 
videoL = cv2.VideoWriter('Lepton.mp4', fourccL,5,(wL,hL))

fourccH = cv2.VideoWriter_fourcc(*'mp4v') 
videoH = cv2.VideoWriter('Himax.mp4', fourccH,5,(w,h))

for img_path in images_path:
    print(img_path[len(path)-1:])
    img = cv2.imread(img_path)
    print(img.shape)
    video.write(img)
video.release()

for img_pathL in images_pathL:
    print(img_pathL[len(pathL)-1:])
    imgL = cv2.imread(img_pathL)
    print(imgL.shape)
    videoL.write(imgL)
videoL.release()

for img_pathH in images_pathH:
    print(img_pathH[len(pathH)-1:])
    imgH = cv2.imread(img_pathH)
    print(imgH.shape)
    videoH.write(imgH)
videoH.release()

print("Video out ")





