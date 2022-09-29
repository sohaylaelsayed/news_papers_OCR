import cv2 
import os
from matplotlib import pyplot as plt
from PIL import Image
from pdf2image import convert_from_path

from read_json import readJson
from preprocessing import pre_process, preprocess, convert_grayscale
from utilities import save_preprocess_image, save_gray_img
from semantic_relation import string_match
from tesseract_ocr import tesseract_ocr



# path of where the file is
threshold = 0.85  # 0-1
output_format = "word"  # excel / word


#you should give your local path
train_path = 'C:/Users/zeyne/Desktop/ck/data/train/'
annotation_path = 'C:/Users/zeyne/Desktop/ck/news_paper_segmentation_-export-2022-09-13T13_11_27.050Z.json'

pdr_to_jpg_path = 'C:/Users/zeyne/Desktop/ck/data/pdf_to_jpg/'
gray_images_path = "C:/Users/zeyne/Desktop/ck/data/gray_images/"


def main():

    print("Processing Images")

    #convert pdf to jpg

    for filename in os.listdir(train_path):
        f = os.path.join(train_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if str(f).find("pdf") != -1:
                # Store Pdf with convert_from_path function
                images = convert_from_path(f)
                for i in range(len(images)):
                    # Save pages as images in the pdf
                    images[i].save(pdr_to_jpg_path+ filename[ :-4]+'.jpg', 'JPEG')
            else :
                Image.open(f).save(pdr_to_jpg_path+filename )

    #convert gray image

    for filename in os.listdir(pdr_to_jpg_path):
        f = os.path.join(pdr_to_jpg_path, filename)
        title, file_extension = os.path.splitext(filename)
        
        cropped_img = cv2.imread(f)
        preprocess_img = convert_grayscale(cropped_img)
        cropped_path = save_gray_img(preprocess_img, gray_images_path, title)
        text_file_path = tesseract_ocr (cropped_path)
        string_match(text_file_path, threshold, output_format)



    
    #create cropped images

    readJson(gray_images_path, annotation_path)

    print('\nDone')

if __name__ == "__main__":
    main()