import argparse
import os
import cv2
import numpy as np

# TODO what is the format for YOLO datasets?

def run(folder="data/"):
    image_files = os.listdir(folder)
    image_files = filter(lambda x: os.path.isfile(folder + x), image_files)
    for filename in image_files:
        assert filename.endswith(".npy")
        path = folder + filename
        image = np.load(path)
        cv2.imshow("lel", image)
        if cv2.waitKey(-1) == ord('q'):
            break

if __name__ == "__main__":
    run()