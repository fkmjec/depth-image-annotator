import argparse
import os
import cv2
import numpy as np
import time
import logging

def rescale(depth, min_range_mm, max_range_mm):
    scaled = (
        (
            (depth - min_range_mm).astype(np.float32)
            / (max_range_mm - min_range_mm)
        )
        * 255
    ).astype(np.uint8)
    return scaled


class State:
    def __init__(self, image: np.ndarray, filename, img_dir, label_dir, min_range_mm, max_range_mm):
        self.filename = filename # name with stripped suffix (no .npy)
        self.orig_img = image
        self.first_click = None
        self.last_click = None
        self.fixed = False
        self.label_dir = label_dir
        self.img_dir = img_dir
        self.min_range_mm = min_range_mm
        self.max_range_mm = max_range_mm

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
                self.fixed = True
        elif self.first_click is not None and not self.fixed:
            self.last_click = (x, y)
    
    def save(self):
        with open(self.label_dir + f"/{self.filename}.txt", "w") as f:
            if self.last_click is not None:
                first_normalized = self.to_percentage(self.first_click)
                second_normalized = self.to_percentage(self.last_click)
                center_x = (second_normalized[0] + first_normalized[0]) / 2
                center_y = (second_normalized[1] + first_normalized[1]) / 2
                assert 0 <= center_x <= 1 and 0 <= center_y <= 1 
                size_x = np.abs(second_normalized[0] - first_normalized[0])
                size_y = np.abs(second_normalized[1] - first_normalized[1])
                assert 0 <= size_x <= 1 and 0 <= size_y <= 1 
                f.write(f"0: {center_x} {center_y} {size_x} {size_y}\n")
        
        cv2.imwrite(self.img_dir + f"/{self.filename}.png", rescale(self.orig_img, self.min_range_mm, self.max_range_mm))

    def render(self) -> np.ndarray:
        depth = self.orig_img.copy()
        scaled = rescale(depth, self.min_range_mm, self.max_range_mm)
        color = cv2.cvtColor(scaled, cv2.COLOR_GRAY2BGR)
        if self.first_click is not None and self.last_click is not None:
            cv2.rectangle(color, self.first_click, self.last_click, color=(255,0,0), thickness=3)
        return color

STATE: State = None

# TODO what is the format for YOLO datasets?
def mouse_click(event, x, y,  
                flags, param):
    STATE.mouse_callback(event, x, y)

def run(in_dir: str, out_dir: str, min_range_mm: int, max_range_mm: int):
    global STATE
    if not in_dir.endswith("/"):
        in_dir += "/"
    if not out_dir.endswith("/"):
        out_dir += "/"
    image_files = os.listdir(in_dir)
    img_save_dir = out_dir + "images/"
    label_save_dir = out_dir + "labels/"

    # TODO: maybe add a warning here if the dirs exists
    os.makedirs(img_save_dir, exist_ok=True)
    os.makedirs(label_save_dir, exist_ok=True)
    
    image_files = filter(lambda x: os.path.isfile(in_dir + x), image_files)
    stopped = False
    for filename in image_files:
        if stopped:
            break
        assert filename.endswith(".npy")
        path = in_dir + filename
        stripped_fn = filename[0:-4]
        if os.path.exists(label_save_dir + stripped_fn + ".txt") and os.path.exists(img_save_dir + stripped_fn + ".png"):
            # if outputs already exist, we skip the image
            logger.info(f"label output {label_save_dir + stripped_fn + '.txt'} and image output {img_save_dir + filename} already exist, skipping.")
            continue
        img = np.load(path)
        STATE = State(img, stripped_fn, img_save_dir, label_save_dir, min_range_mm, max_range_mm)
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Depth image annotator for ASL")
    parser.add_argument("--in_dir", help="Input image directory. Contains raw .npy files (in the future, could be changed to png).", required=True)
    parser.add_argument("--out_dir", help="Output dataset directory", default="out/")
    parser.add_argument("--min_range_mm", help="The minimum range of the depth detector", default=250)
    parser.add_argument("--max_range_mm", help="The maximum range of the depth detector", default=2880)
    args = parser.parse_args()
    run(args.in_dir, args.out_dir, args.min_range_mm, args.max_range_mm)
