# TO USE INSTALL PYSERIAL
#       pip install pyserial
import cv2
import serial.tools.list_ports
import serial
import numpy as np
import copy
import random


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

mergeLineSize = 164
mergeHeightSize = 122

countFrame = 0

# contenitori dei pixel (byte) letti tramite uart
himax_frame  = np.zeros((122,164,3), np.uint8)
lepton_frame = np.zeros((60,80,3), np.uint8)

# merge operations
alpha = 0.6

w_off = 42
h_off = 31
w_end = w_off + lepton_frame.shape[1]
h_end = h_off + lepton_frame.shape[0] 


RECOGNIZE_ENABLE = False
# *********************************************************
if(RECOGNIZE_ENABLE==True):
    # Load Yolo
    net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")

    # Name custom object
    classes = ["person"]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

# *********************************************************



# big infinite while loop
while True:


    # *** read HIMAX    
    for i in range(himaxHeightSize):  # cycle over height

        pxl = serialInst.read(himaxLineSize) # read one line

        for j in range(himaxLineSize):     # cycle over width
            himax_frame[i][j][0] = pxl[j]
            himax_frame[i][j][1] = pxl[j]
            himax_frame[i][j][2] = pxl[j]


    
    # *** read LEPTON    
    for i in range(leptonHeightSize):  # cycle over height

        pxl = serialInst.read(leptonLineSize) # read one line

        for j in range(leptonLineSize):     # cycle over width

            if(j%3 == 0):
                lepton_frame[i][j//3][0] = pxl[j]     # RED

            elif(j%3 == 1):
                lepton_frame[i][j//3][1] = pxl[j]     # GREEN

            elif(j%3 == 2):
                lepton_frame[i][j//3][2] = pxl[j]     # BLUE

    
    # *** MERGE the image in a single matrix
    merge_frame  = copy.deepcopy(himax_frame)
    merge_frame[h_off:h_end, w_off:w_end,:] = cv2.addWeighted(lepton_frame, alpha, himax_frame[h_off:h_end, w_off:w_end,:], 1-alpha, 0.0)


    

    # SAVE THE IMAGE
    if(countFrame < 10):
        nameLep = "00"+str(countFrame)+"frame.bmp"
    elif(countFrame<100):
        nameLep = "0"+str(countFrame)+"frame.bmp"
    else:
        nameLep = str(countFrame)+"frame.bmp"

    
    cv2.imwrite("Capture/Lepton/"+nameLep, lepton_frame)
    cv2.imwrite("Capture/Himax/"+nameLep, himax_frame)
    cv2.imwrite("Capture/Merge/"+nameLep, merge_frame)
    countFrame = countFrame+1 


    # ************************************** RECOGNIZE HUMAN ********************************************
    if(RECOGNIZE_ENABLE == True):

        # Loading image
        img = copy.deepcopy(himax_frame)
        img = cv2.resize(img, None, fx=3, fy=3)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    #print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        #print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

        #img_scale_up = cv2.resize(img, (0, 0), fx=5, fy=5)
        #cv2.imshow("Image", img_scale_up)
        cv2.imshow("Image", img)
    # ****************************************************************************************


    
    # *** DISPLAY IMAGES
    
    himax_disp = cv2.resize(himax_frame, (0,0),fx=3, fy=3)
    cv2.imshow('HIMAX',himax_disp)
    cv2.waitKey(1) 

    

    """
    # display LETPON image
    lepton_disp = cv2.resize(lepton_frame, (0,0),fx=5, fy=5)
    cv2.imshow('LEPTON',lepton_disp)
    cv2.waitKey(1) 
    

    # display MERGE image
    merge_disp = cv2.resize(merge_frame, (0,0),fx=5, fy=5)
    cv2.imshow('MERGED', merge_disp)
    cv2.waitKey(1) 
    """



    # *** press Q to stop script
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()





  





