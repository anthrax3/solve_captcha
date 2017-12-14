import os, time, sys, logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image, ImageOps
from io import BytesIO
import urllib.request
import numpy as np

logger = logging.getLogger(__name__)

def cropImage(im, imgWidth, imgHeight):
    box1 = (0, 0, imgWidth/2, imgHeight)
    box2 = (imgWidth/2, 0, imgWidth, imgHeight)
    crop1 = im.crop(box1)
    crop2 = im.crop(box2)
    return (crop1, crop2)

def binarize_image(img, threshold=200):
   img_array = np.array(im) # convert image to np array
   img_array = np.where(img_array > threshold,255,0) 
   print(img_array.shape)
   return Image.fromarray(img_array) #TODO: Convert np.array to PIL.Image


def processImage(im): 
    # Remove large sections of white
    pr_image = ImageOps.invert(im)
    pr_image = ImageOps.autocontrast(pr_image)
    return pr_image

url="https://www.google.com/recaptcha/demo/recaptcha"
driver = webdriver.Chrome()
driver.get(url)

try:
    element = WebDriverWait(driver, 10).until(
	    EC.presence_of_element_located((By.XPATH, '//img[@id="recaptcha_challenge_image"]'))
	    )
    image_url = element.get_attribute('src')
    #im = Image.open(urllib.request.urlopen(image_url)) 
    im = Image.open('tmpxvyd2qvr.png').convert('L')
    im = binarize_image(im)
    im.show()
    imgWidth, imgHeight = im.size

    im1, im2 = cropImage(im, imgWidth, imgHeight)
	
    #im1 = processImage(im1)
    #im2 = processImage(im2)

    im1.show()
    im2.show()

    print(pytesseract.image_to_string(im1))
    print(pytesseract.image_to_string(im2))

    # split image based on white pixels in centre of image
#    captcha = pytesseract.image_to_string(inverted_image)
#    print(captcha)


finally:
    driver.quit()




#captcha_image = driver.find_element_by_xpath('//img[@id="recaptcha_challenge_image"]')
#print(captcha_image)


#driver.set_window_size(width, height)
#screen = driver.get_screenshot_as_png()
#imagefile = BytesIO()
#filehandle.write(screen)
#urllib.urlretrieve(captcha_image, filehandle)



#driver.close()

