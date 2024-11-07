import argparse
import os
import cv2
import numpy as np
import time

class State:
    def __init__(self, image: np.ndarray):
        self.orig_img = image
        self.first_click = None
        self.last_click = None
        self.fixed = False
    
    def mouse_callback(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.fixed:
                self.first_click = None
                self.last_click = None
                self.fixed = False
                return
            if self.first_click is None:
                self.first_click = (x, y)
            else:
                self.last_click = (x, y)
                self.fixed = True
        elif self.first_click is not None and not self.fixed:
            self.last_click = (x, y)

    def render(self) -> np.ndarray:
        displayed = self.orig_img.copy()
        if self.first_click is not None and self.last_click is not None:
            cv2.rectangle(displayed, self.first_click, self.last_click, color=(255,0,0), thickness=3)
        return displayed

STATE: State = None

# TODO what is the format for YOLO datasets?
def mouse_click(event, x, y,  
                flags, param):
    STATE.mouse_callback(event, x, y)

def run(folder="data/"):
    global STATE
    image_files = os.listdir(folder)
    image_files = filter(lambda x: os.path.isfile(folder + x), image_files)
    for filename in image_files:
        assert filename.endswith(".npy")
        path = folder + filename
        img = np.load(path)
        STATE = State(img)
        cv2.imshow("image", STATE.render())
        cv2.setMouseCallback('image', mouse_click) 
        while True:
            image = STATE.render()
            cv2.imshow("image", image)
            time.sleep(0.01)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    run()