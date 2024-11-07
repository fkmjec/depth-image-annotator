import numpy as np
from time import time, sleep

def generate_data(count: int, dimx: int, dimy: int, folder="data/"):
    for _ in range(count):
        array = (np.random.rand(dimx, dimy) * 255).astype(np.uint8)
        np.save(folder + str(time()), array)
        print("saved")
        sleep(0.5)
        

if __name__ == "__main__":
    generate_data(20, 512, 512)