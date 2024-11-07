import argparse
import os
import cv2
import numpy as np

# TODO what is the format for YOLO datasets?
IMAGE = None
#define the events for the 
# mouse_click. 
def mouse_click(event, x, y,  
                flags, param): 
    print(x, y)
    # to check if left mouse  
    # button was clicked 
    if event == cv2.EVENT_LBUTTONDOWN: 
          
        # font for left click event 
        font = cv2.FONT_HERSHEY_TRIPLEX 
        LB = 'Left Button'
        # display that left button  
        # was clicked. 
        cv2.putText(IMAGE, LB, (x, y),  
                    font, 1,  
                    (255, 255, 0),  
                    2)  
        # cv2.imshow('image', IMAGE) 
          
          
    # to check if right mouse  
    # button was clicked 
    if event == cv2.EVENT_RBUTTONDOWN: 
           
        # font for right click event 
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX 
        RB = 'Right Button'
          
        # display that right button  
        # was clicked. 
        cv2.putText(IMAGE, RB, (x, y), 
                    font, 1,  
                    (0, 255, 255), 
                    2) 
        # cv2.imshow('image', IMAGE) 
  

def run(folder="data/"):
    image_files = os.listdir(folder)
    image_files = filter(lambda x: os.path.isfile(folder + x), image_files)
    for filename in image_files:
        assert filename.endswith(".npy")
        path = folder + filename
        image = np.load(path)
        IMAGE = image
        cv2.imshow("image", image)
        print(IMAGE)
        cv2.setMouseCallback('image', mouse_click) 
        if cv2.waitKey(-1) == ord('q'):
            break

if __name__ == "__main__":
    run()