from distutils.archive_util import make_archive
from pprint import pprint
import numpy as np
import json
import os

from utilities import make_dir
from read_image import ReadImages
from shapely.geometry import Polygon
from matplotlib import pyplot as plt

class rearrenge_column :  

  def __init__(self):
    self.blockes_polygon = []
    self.blockes_box = []

  def rearrange_column_box(self,box_column_list: list):

    for title_column in box_column_list : 
      if title_column["title"]=="Content Title " :
        title = title_column
        self.blockes_box.append(title)
        del  box_column_list[(box_column_list.index(title))]   
   
    for i in range(len(box_column_list)):
      max_x = box_column_list[0]["bounding-box"]["x"]  if 'bounding-box' in box_column_list[0].keys() else rearrenge_column.polygon_max_x_(box_column_list[0])
      max_y = box_column_list[0]["bounding-box"]["y"] if  'bounding-box' in box_column_list[0].keys()  else  rearrenge_column.polygon_max_y_(box_column_list[0])
      max_width =  box_column_list[0]["bounding-box"]["width"] if 'bounding-box' in box_column_list[0].keys() else  rearrenge_column.polygon_max_width_(box_column_list[0])
      block = box_column_list[0]
      
      for column in box_column_list :      
        if (column["bounding-box"]["x"]   if 'bounding-box' in column.keys() else rearrenge_column.polygon_max_x_(column)  >= max_x  ):
          block = column
          max_x = column["bounding-box"]["x"]   if 'bounding-box' in column.keys() else rearrenge_column.polygon_max_x_(column)
          max_y = column["bounding-box"]["y"]  if 'bounding-box' in column.keys() else rearrenge_column.polygon_max_y_(column)
        elif (column["bounding-box"]["x"]  if 'bounding-box' in column.keys() else  rearrenge_column.polygon_max_x_(column) < max_x and column["bounding-box"]["y"] if 'bounding-box' in column.keys() else  rearrenge_column.polygon_max_y_(column) > max_y and column["bounding-box"]["width"]  if 'bounding-box' in column.keys() else  rearrenge_column.polygon_max_width_(column) >= max_width) :
          block = column 
          max_width = column["bounding-box"]["width"] if 'bounding-box' in column.keys() else  rearrenge_column.polygon_max_width_(column)
          max_y = column["bounding-box"]["y"] if 'bounding-box' in column.keys() else  rearrenge_column.polygon_max_y_(column)
      self.blockes_box.append(block)
      del box_column_list[(box_column_list.index(block))]

    return(self.blockes_box)

  def rearrange_column_polygon(self,polygon_column_list: list): 

    for title_column in polygon_column_list : 
      if title_column["title"]== "Content Title polygon":
        title = title_column
        self.blockes_polygon.append(title)
        del  polygon_column_list[(polygon_column_list.index(title))]   
   

    for i in range(len(polygon_column_list)): 

      max_x = rearrenge_column.polygon_max_x_(polygon_column_list[0])
      max_y = rearrenge_column.polygon_max_y_(polygon_column_list[0])
      block = polygon_column_list[0]

      for column in polygon_column_list :
        if (rearrenge_column.polygon_max_x_(column)> max_x  and rearrenge_column.polygon_max_y_(column)<= max_y ):
          block = column
          max_x = rearrenge_column.polygon_max_x_(column)
          max_y = rearrenge_column.polygon_max_y_(column)
         
        elif (rearrenge_column.polygon_max_x_(column)< max_x and rearrenge_column.polygon_max_y_(column) < max_y) : 
          block = column 
      

      self.blockes_polygon.append(block)
      del polygon_column_list[(polygon_column_list.index(block))]

    return(self.blockes_polygon)

  def polygon_max_x_(box : dict):
    list = []
    for coordinate in box["polygon"] :
      list.append(coordinate[0])
    max_x = np.max(list)
    return max_x
    

  def polygon_max_y_(box : dict):
      list = []
      for coordinate in box["polygon"] :
        list.append(coordinate[1])
      max_y = np.max(list)
      return max_y

  def polygon_max_width_(box : dict):
    list = []
    for coordinate in box["polygon"] :
      list.append(coordinate[0])
    max_point = np.max(list)
    min_point = np.max(list)
    width = max_point - min_point
    return width

class mark_column_type: 

  def __init__(self):
    self.polygon_content = []
    self.box_content = []
    self.max = []
   
  def mark_column_polygon(self, content_polygon_block , image_box):
    
    for box in image_box['tasks'][0]['objects']:
      if box["title"] == "Content Title polygon" or box["title"] == "Column polygon" or box["title"] =="author polygon" or box["title"] == "image polygon" :
          self.polygon_content.append(box) if Polygon(content_polygon_block["polygon"]).contains(Polygon(box['polygon'])) == True else None
    
    # print('mark_column_polygon')
    # pprint(self.polygon_content)
    return rearrenge_column().rearrange_column_polygon(self.polygon_content)
          
  def mark_column_box(self,content_box_block :list , image_box):

    box_x = content_box_block['bounding-box']['x']
    box_y = content_box_block['bounding-box']['y']
    box_height = content_box_block['bounding-box']['height']
    box_width = content_box_block['bounding-box']['width']
    

    for box in image_box['tasks'][0]['objects']:
      if box["title"] == 'Content Title '  or box['title'] == 'Column'  or box["title"] == "Image"  or box["title"] =="author" : 
        # If top-left inner box corner is inside the bounding box  
          if box_x < box['bounding-box']['x'] and box_y < box['bounding-box']['y']:
          # If bottom-right inner box corner is inside the bounding box
            if box['bounding-box']['x'] + box['bounding-box']['width'] < box_x + box_width and box['bounding-box']['y'] + box['bounding-box']['height'] < box_y + box_height:
              self.box_content.append(box)
      
      elif box["title"] == "Column polygon" or box["title"] == "image polygon":
        box_point_x = box_x +box_width
        box_point_y = box_y + box_height
        polygon_point_x = rearrenge_column.polygon_max_x_(box)
        polygon_point_y = rearrenge_column.polygon_max_y_(box)
        if (box_x <= polygon_point_x <= box_point_x and  box_y <= polygon_point_y <= box_point_y):
          self.box_content.append(box) 

    if (len(self.box_content) == 0  )  :
      return [content_box_block]

    else :  
      return rearrenge_column().rearrange_column_box(self.box_content)
  
  def mark_ads(self,ads_block):
    return([ads_block])

  def mark_title(self,title_block):
    return([title_block])

class check_polygon_inside_rectangle :
  def __init__(self):
     self.X_list = 0
     self.Y_list = 0
     self.X_counter = 0
     self.Y_counter = 0 

  def polygon_x_point(self , box : dict):
        for coordinate in box["polygon"] :
          self.X_counter +=1
          x = self.X_list + coordinate[0]
        return x/self.X_counter
        

  def polygon_y_point(self,box : dict):
        for coordinate in box["polygon"] :
          self.Y_counter +=1
          y = self.Y_list + coordinate[1]
        return y/self.Y_counter

def readJson(train_path, annotation_path):
    read_images = ReadImages()
    print('READ JSON')
    imagePaths = []
    f = open(annotation_path)
    data = json.load(f)
    for i in range(len(data)):
        image_box = data[i]
        image_name = image_box["externalId"]
        filename, file_extension = os.path.splitext(image_name)
        print('IMGAE: ' + str(i) + ' / ' + 'IMAGE NAME: ' + image_name)
        imagePaths.append(str(train_path) + str(image_name))
        contents = []
        counter = 0

        directory_path = 'C:/Users/zeyne/Desktop/ck/data/'
        make_dir(directory_path, filename)
        path = directory_path+filename+'/'
        print(path)

        for box in image_box['tasks'][0]['objects']:
            #print(box["title"])
            if box["title"] == "Content" or  box["title"] == "Content polygon":
                contents.append(box)
            if box["title"] == "advertisement"  :
                advertisement_list = mark_column_type().mark_ads(box)  
                if "polygon" in advertisement_list[0].keys():
                    read_images.read_image(image_name, advertisement_list, filename, path)
                else:
                    read_images.read_image(image_name, advertisement_list, filename, path)
            if box["title"] == "title":
                title_list = mark_column_type().mark_title(box)
                if "polygon" in title_list[0].keys():
                    read_images.read_image(image_name, title_list, filename, path)
                else:
                    read_images.read_image(image_name, title_list, filename, path)
                
        for content in contents :  
            counter+=1
            print("content" + str(counter))
            if "polygon" in content.keys():
                polygon_column_list = mark_column_type().mark_column_polygon(content,image_box)
                read_images.read_image(image_name, polygon_column_list, filename, path)
                
            if 'bounding-box' in content.keys():
                box_column_list = mark_column_type().mark_column_box(content,image_box) 
                if(box_column_list is None):
                    print("List is empty")    
                else:
                    read_images.read_image(image_name, box_column_list, filename, path)




    