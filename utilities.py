import numpy as np
import cv2 as cv
import os
from matplotlib import pyplot as plt

def save_gray_img(img, path, title):
    print(path+title)
    plt.imsave(path + f'{title}.jpg', img)

def save_image(img, path, title, counter):
    print(path)
    plt.imsave(path + f'{title}_{counter}.jpg', img)

def save_preprocess_image(path, filename, img):
    plt.imsave(path + f'{filename}.jpg', img)

def make_dir(directory, name):
    # Path
    path = os.path.join(directory, name)
    if os.path.isdir(path):
        name = name+'2'
        path = os.path.join(directory, name)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
    else:
        os.mkdir(path)
        print("Directory '% s' created" % directory)
    new_path = directory+name
    print(new_path)
    return new_path