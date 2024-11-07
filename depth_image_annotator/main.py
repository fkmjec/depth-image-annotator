import argparse
import os
import cv2
import numpy as np
import time

# TODO what is the format for YOLO datasets?
IMAGE = None
#define the events for the 
# mouse_click. 
def mouse_click(event, x, y,  
                flags, param): 
    global IMAGE
    if event == cv2.EVENT_LBUTTONDOWN:           
        center_coordinates = (x, y)  # Center of the image
        radius = 100  # Radius of the circle
        color = (0, 0, 255)  # Red color in BGR format
        thickness = -1  # Thickness of the circle outline (-1 to fill the circle)        # cv2.imshow('image', IMAGE) 
        cv2.circle(IMAGE, center_coordinates, radius, color, thickness)
        print("drew circle")
          
  

def run(folder="data/"):
    global IMAGE
    image_files = os.listdir(folder)
    image_files = filter(lambda x: os.path.isfile(folder + x), image_files)
    for filename in image_files:
        assert filename.endswith(".npy")
        path = folder + filename
        IMAGE = np.load(path)
        cv2.imshow("image", IMAGE)
        cv2.setMouseCallback('image', mouse_click) 
        while True:
            cv2.imshow("image", IMAGE)
            time.sleep(0.01)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    run()