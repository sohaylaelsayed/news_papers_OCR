from types import new_class
import cv2
import numpy as np
from matplotlib import pyplot as plt
from utilities import save_image
from preprocessing import pre_process

train_path = 'D:/Cyberneticlabs/OCR_Line_Seg/data/train/'
path = "D:/Cyberneticlabs/OCR_Line_Seg/data/cropped_images/"

class ReadImages():
  def __init__(self):
    print('ReadImages start')
    self.counter = 0
        
  def read_image(self, image_name, column_list, filename, path):
    self.filename = filename
    self.image = cv2.imread(train_path + image_name)
    self.path = path
    print(self.path)

    for i in range(len(column_list)):
        self.counter+=1
        print(self.counter)
        if "polygon" in column_list[i].keys():
            #print('POLYGON')
            self.read_polygon(self.image, column_list[i], self.counter)
        else:
            #print('BOX')
            self.read_box(self.image, column_list[i], self.counter)
 
  def new_title(self, title):
    title = title.split(" ")
    print(title)
    if len(title) > 0 :
      new_title = "_".join(title)
    print(new_title)
    return new_title

  def read_box(self, image, column_list, counter):
    #print(column_list['bounding-box'])
    title = column_list['title']
    new_title = self.new_title(title)
    x = column_list['bounding-box']['x']
    y = column_list['bounding-box']['y']
    w = column_list['bounding-box']['width']
    h = column_list['bounding-box']['height']
    cropped = image[int(y):int(y)+int(h),int(x):int(x)+int(w)]#[y:y+h,x:x+w]
    preprocess_img = pre_process(cropped, title)
    save_image(preprocess_img, self.path, new_title, counter)
    return cropped

  def read_polygon(self, image, column_list, counter):
    title = column_list['title']
    new_title = self.new_title(title)
    mask = np.zeros(image.shape[0:2], dtype=np.uint8)
    points = column_list['polygon']
    points = np.array(points,  dtype=np.int32) 

    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        
    res = cv2.bitwise_and(image,image,mask = mask)
    rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    preprocess_img = pre_process(cropped, title)
    save_image(preprocess_img, self.path, new_title, counter)
    return cropped
