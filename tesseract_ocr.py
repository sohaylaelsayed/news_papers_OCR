import platform
from pathlib import Path
import pytesseract
from PIL import Image
from summaraization import summary 
import os

path = "ocr_output"

def tesseract_ocr(cropped_images_file_path):

  filename_text = cropped_images_file_path[ :-4] + '.docx'
  for filename in os.listdir(cropped_images_file_path):
    f = os.path.join(cropped_images_file_path,filename)
    custom_config = r'--oem 3 --psm 6'
    text  = pytesseract.image_to_string(Image.open(f),config=custom_config, lang="ara")
    summary_text = summary(text)
    with open(os.path.join(path, filename_text), 'a') as text_file:
        text_file.write(summary_text)
  return(path  + filename_text)