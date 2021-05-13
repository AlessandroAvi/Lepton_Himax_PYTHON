# TO USE INSTALL PYSERIAL
#       pip install pyserial
import cv2
import serial.tools.list_ports
import serial
import numpy as np


# create instance of serial
ports = serial.tools.list_ports.comports()
# create black serial
serialInst = serial.Serial()

# declaire some important values for the UART connection
serialInst.baudrate = 1764705   
serialInst.port = "COM3"

# open the port and see the incoming data
serialInst.open()



print(" ")
print("PRESS BLUE BUTTON TO START VIDEO")


# definition of parameters
himaxLineSize = 164
himaxHeightSize = 122

leptonLineSize = 80*3
leptonHeightSize = 60


# contenitori dei pixel (byte) letti tramite uart
himax_pxl = np.zeros((himaxHeightSize,himaxLineSize,3))
lepton_pxl = np.zeros((leptonHeightSize,leptonLineSize,3))


# big infinite while loop
while True:

    # read HIMAX    
    for i in range(himaxHeightSize):  # cycle over height

        pxl = serialInst.read(himaxLineSize) # read one line

        for j in range(himaxLineSize):     # cycle over width
            himax_pxl[i][j][0] = pxl[j]
            himax_pxl[i][j][1] = pxl[j]
            himax_pxl[i][j][2] = pxl[j]

    # display image
    himax_frame = np.array(himax_pxl ,dtype=np.uint8)
    himax_frame = cv2.resize(himax_frame, (0,0),fx=5, fy=5)
    cv2.imshow('HIMAX',himax_frame)
    cv2.waitKey(1) 
    



    # read LEPTON    
    for i in range(leptonHeightSize):  # cycle over height

        pxl = serialInst.read(leptonLineSize) # read one line

        for j in range(leptonLineSize):     # cycle over width

            if(j%3 == 0):
                lepton_pxl[i][j//3][0] = pxl[j]     # RED

            elif(j%3 == 1):
                lepton_pxl[i][j//3][1] = pxl[j]     # GREEN

            elif(j%3 == 2):
                lepton_pxl[i][j//3][2] = pxl[j]     # BLUE



    # display image
    lepton_frame = np.array(lepton_pxl ,dtype=np.uint8)

    lepton_frame = cv2.resize(lepton_frame, (0,0),fx=5, fy=5)
    cv2.imshow('LEPTON',lepton_frame)
    cv2.waitKey(1) 



    # press Q to stop script
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





  





