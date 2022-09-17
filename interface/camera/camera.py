from typing import List, Tuple
from pygame import camera, image
from time import sleep
from PIL import BmpImagePlugin

def getCamera(cam: str, size: Tuple):
    camera.init()
    cam = camera.Camera(cam, size)
    cam.start()
    sleep(1)
    return cam

def split(arr: List, x: int) -> List:
    res = []
    last = 0
    for [k, i] in enumerate(arr):
        if k - last + 1 == x:
            res.append(arr[last:k+1])
            last = k + 1
    return res

def flatten(item) -> List:
    res = []
    if isinstance(item, List):
        for i in item:
            res += flatten(i)
    else:
        res.append(item)
    return res

def coordInBox(coord: Tuple[int, int], box: Tuple[int, int, int, int]) -> bool:
    x, y = coord
    l, t, r, b = box
    return y >= t and y <= b and x >= l and x <= r

def fillWithBlank(file:str, box: Tuple, dest: str,  fill: Tuple = (0, 0, 200), negative=False):
    img = BmpImagePlugin.BmpImageFile(file)
    flat = bytearray(img.tobytes())
    pixels_flat = split(list(flat), 3) # concat rgb channels (3b) into one pixel
    pixels_2d = split(pixels_flat, img.size[0]) # concat pixels into height => width

    for [k_h, h] in enumerate(pixels_2d):
        for [k_w, pixel] in enumerate(h):
            # if k_h >= t and k_h <= b and k_w >= l and k_w <= r:
            if coordInBox((k_w, k_h), box) == (not(negative)):
                pixels_2d[k_h][k_w] = list(fill)
    edited_flat = flatten(pixels_2d)
    result = img.copy()
    result.frombytes(bytes(edited_flat))
    result.save(dest)

def savePicture(cam: str, size: Tuple, saveFile: str) -> None:
    img = getCamera(cam, size).get_image()
    image.save(img, saveFile, "bmp")

if __name__ == '__main__':
    # savePicture("FHD Webcam", (512, 384), "../../real_images/25.bmp")
    # savePicture("FHD Webcam", (512, 384), saveFile="../../real_images/30.bmp")
    fillWithBlank("../../real_images/30.bmp", (60, 96, 255, 209), "../../real_images/31.bmp", (255, 255, 255), negative=True)

    # fillWithBlank("../../real_images/20.bmp", (0, 0, 50, 50),  "../../real_images/x.bmp", fill=(90, 250, 2), negative=True)
    pass
# a = [1, 2, 3, 4, 5, 6, 7, 8,9]
# b = split(a, 3)
# print(b)
