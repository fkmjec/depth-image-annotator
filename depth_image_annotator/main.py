import argparse
import os
import cv2
import numpy as np
import time
import logging

class State:
    def __init__(self, image: np.ndarray, filename, img_dir, label_dir):
        self.filename = filename # name with stripped suffix (no .npy)
        self.orig_img = image
        self.first_click = None
        self.last_click = None
        self.fixed = False
        self.label_dir = label_dir
        self.img_dir = img_dir

    def to_percentage(self, xy):
        max_x = self.orig_img.shape[1]
        max_y = self.orig_img.shape[0]
        per_x = xy[0] / max_x
        per_y = xy[1] / max_y
        return per_x, per_y
    
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
                print(f"rectangle: {self.first_click}, {self.last_click}")
                self.fixed = True
        elif self.first_click is not None and not self.fixed:
            self.last_click = (x, y)
    
    def save(self):
        with open(self.label_dir + f"/{self.filename}.txt", "w") as f:
            if self.fixed:
                first_normalized = self.to_percentage(self.first_click)
                second_normalized = self.to_percentage(self.last_click)
                center_x = (second_normalized[0] + first_normalized[0]) / 2
                center_y = (second_normalized[1] + first_normalized[1]) / 2
                assert 0 <= center_x <= 1 and 0 <= center_y <= 1 
                size_x = np.abs(second_normalized[0] - first_normalized[0])
                size_y = np.abs(second_normalized[1] - first_normalized[1])
                assert 0 <= size_x <= 1 and 0 <= size_y <= 1 
                f.write(f"0: {center_x} {center_y} {size_x} {size_y}\n")
        
        cv2.imwrite(self.img_dir + f"/{self.filename}.png", self.orig_img)

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

def run(folder="data/", out_dir="out/"):
    global STATE
    image_files = os.listdir(folder)
    img_save_dir = out_dir + "images"
    label_save_dir = out_dir + "labels"

    try:
        os.mkdir(out_dir)
        os.mkdir(img_save_dir)
        os.mkdir(label_save_dir)
    except FileExistsError:
        logger.error(f"Directory {out_dir} already exists, stopping!")
        return
    
    image_files = filter(lambda x: os.path.isfile(folder + x), image_files)
    stopped = False
    for filename in image_files:
        if stopped:
            break
        assert filename.endswith(".npy")
        path = folder + filename
        img = np.load(path)
        STATE = State(img, filename[0:-4], img_save_dir, label_save_dir)
        cv2.imshow("image", STATE.render())
        cv2.setMouseCallback('image', mouse_click) 
        while True:
            image = STATE.render()
            cv2.imshow("image", image)
            time.sleep(0.01)
            key = cv2.waitKey(1)
            if key == ord('q'):
                stopped = True
                break
            if key == ord('n'):
                STATE.save()
                break

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    run()