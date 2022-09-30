import numpy as np
import cv2
from scipy.ndimage import interpolation as inter
from PIL import Image as im
from PIL import Image, ImageChops
from matplotlib import pyplot as plt


#################ZEYNEP#####################
#remove border code
def trim(im):
  bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
  diff = ImageChops.difference(im, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)

# Rotate the image around its center
def rotateImage(img, angle: float):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def convert_grayscale(image):
    #gray_image = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return gray

def thresholding(gray_image, value):
    blurred = cv2.GaussianBlur(gray_image, (3, 3), 0)
    binary_img = cv2.threshold(blurred, value, 255, cv2.THRESH_BINARY)[1]
    return binary_img

#image preprocessing and find angle
def deskewing(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  blurred = cv2.GaussianBlur(gray, (3, 3), 0)

  thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
  dilate = cv2.dilate(thresh, kernel, iterations=5)

  # Find all contours
  contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)

  # Find largest contour and surround in min area box
  largestContour = contours[0]
  minAreaRect = cv2.minAreaRect(largestContour)

  # Determine the angle. Convert it to the value that was originally used to obtain skewed image
  angle = minAreaRect[-1]
  if angle < -45:
      angle = 90 + angle
  angle =  -1.0 * angle

  return angle

def pre_process(cropped, title):

    gray_image = convert_grayscale(cropped)
    thresh_value = 150
    binary_img = thresholding(gray_image, thresh_value)
    # kernel = np.ones((2,2),np.uint8)
    # binary_img = cv2.dilate(binary_img,kernel,iterations = 3)
    plt.imsave('D:/Cyberneticlabs/OCR_Line_Seg/new_image.jpg', binary_img)
    #binary_img = thresholding(gray_image, thresh_value)
    angle  = deskewing(cropped)

    #plt.imsave('D:/Cyberneticlabs/OCR_Line_Seg/new_image.jpg', binary_img)
    im = Image.open('D:/Cyberneticlabs/OCR_Line_Seg/new_image.jpg')

    borderless_image = trim(im)
    newFilePath = ('D:/Cyberneticlabs/OCR_Line_Seg/borderless.jpg')
    try:
        borderless_image.save(newFilePath)
    except AttributeError:
        print("Couldn't save image {}".format(borderless_image))

    borderless_img = cv2.imread('D:/Cyberneticlabs/OCR_Line_Seg/borderless.jpg')
    if angle == (-90):
        return borderless_img
    else:
        
        rotate_image = rotateImage(borderless_img, (-1.0 * angle))
        return rotate_image

###############################################################################
def preprocess(image):

    # Maybe we end up using only gray level image.
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.bitwise_not(gray_img)

    binary_img = binary_otsus(gray_img, 0)
    # plt.imshow(binary_img)
    # plt.show()
    # cv.imwrite('origin.png', gray_img)

    #borderless_img = trim(binary_img)

    # deskewed_img = deskew(binary_img)
    deskewed_img = deskew(binary_img)
    # plt.imshow(deskewed_img)
    # plt.show()
    # cv.imwrite('output.png', deskewed_img)

    # binary_img = binary_otsus(deskewed_img, 0)
    # breakpoint()

    # Visualize

    # breakpoint()
    return deskewed_img

def binary_otsus(image, filter:int=1):
    """Binarize an image 0's and 255's using Otsu's Binarization, remove noise also"""

    if len(image.shape) == 3:
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = image

    # Otsus Binarization
    if filter != 0:
        blur = cv2.GaussianBlur(gray_img, (3,3), 0)
        binary_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    else:
        binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    # Morphological Opening
    # kernel = np.ones((3,3),np.uint8)
    # clean_img = cv.morphologyEx(binary_img, cv.MORPH_OPEN, kernel)

    return binary_img

def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score

def deskew(binary_img):

    ht, wd = binary_img.shape
    # _, binary_img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

    # pix = np.array(img.convert('1').getdata(), np.uint8)
    bin_img = (binary_img // 255.0)

    delta = 0.1
    limit = 3
    angles = np.arange(-limit, limit+delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(bin_img, angle)
        scores.append(score)

    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]
    # print('Best angle: {}'.formate(best_angle))

    # correct skew
    data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
    img = im.fromarray((255 * data).astype("uint8"))

    # img.save('skew_corrected.png')
    pix = np.array(img)
    return pix
