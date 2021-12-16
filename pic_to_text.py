
from PIL import Image
import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt


# If you don't have tesseract executable in your PATH, include the following:
#pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

def pic2text(image_file):
	#image_file = 'data/test-crop.jpg'
	img = cv2.imread(image_file)

	gray = get_grayscale(img)
	thresh = thresholding(gray)
	o = opening(gray)
	c = canny(gray)

	## RESIZE FIRST :
	#new_size = tuple(2*x for x in img.size)
	#img = img.resize(new_size,Image.ANTIALIAS)

	# Simple image to string
	#print(pytesseract.image_to_string(Image.open('test.png')))
	#tess.pytesseract.tesseract_cmd=r"/usr/bin/tesseract"
	# French text image to string
	#plt.imshow(thresh,cmap='gray')
	#plt.show()
	txt = pytesseract.image_to_string(thresh)
	return txt


# In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# NOTE: In this case you should provide tesseract supported images or tesseract will return error
#print(pytesseract.image_to_string('test.png'))

# Batch processing with a single file containing the list of multiple image file paths
#print(pytesseract.image_to_string('images.txt'))

# Timeout/terminate the tesseract job after a period of time
#try:
#    print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
#    print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
#except RuntimeError as timeout_error:
    # Tesseract processing is terminated
#    pass

# Get bounding box estimates
#print(pytesseract.image_to_boxes(Image.open('test.png')))

# Get verbose data including boxes, confidences, line and page numbers
#print(pytesseract.image_to_data(Image.open('test.png')))

# Get information about orientation and script detection
#print(pytesseract.image_to_osd(Image.open('test.png')))

# Get a searchable PDF
#pdf = pytesseract.image_to_pdf_or_hocr('data/test-beer.jpg', extension='pdf')
#with open('test.pdf', 'w+b') as f:
#    f.write(pdf) # pdf type is bytes by default

# Get HOCR output
#hocr = pytesseract.image_to_pdf_or_hocr('data/test-beer.jpg', extension='hocr')

# Get ALTO XML output
#xml = pytesseract.image_to_alto_xml('test.png')
