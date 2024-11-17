# Depth Image Annotator
This is a quick tool I threw together when needing to quickly annotate depth images for training a YOLO model at ETH's ASL. The original objective was to train a model to detect heads in a depth image. Unfortunately, there are not that many good datasets with people viewed top-down. Therefore, we had to annotate our own data.

This tool does just that, and not much more. You open a folder with many `.npy` files constituting the depth, you create the box that contains the head (in our case,
there was only ever one person in the frame, so we only allow one, although this could relatively easily be extended) and you press `n` to save the image and the label and move to the next one. If you want to quit, you press `q`.

The entire UI is created using OpenCV, as this was enough for the task.

## Install and run
* Install `python` and `poetry`
* Run `poetry install`
* Then run using `poetry run python depth_image_annotator/main.py --in_dir [folder with the .npy files] --out_dir [where you want the final dataset to be]`