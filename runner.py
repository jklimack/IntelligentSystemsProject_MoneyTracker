
# implemented classes
import pic_to_text as p2t
import text2obj as t2o

# standard python libraries
import numpy as np
import PIL
import os


# global variables
data_path = 'images'
output_path = 'output'

# get image files
files = []
for file in sorted(list(os.listdir(data_path))):
	if file.endswith(".jpg") or file.endswith(".png"):
		files.append(file)

# select the image to extract the tex from
for i in files:
	test_file = data_path + os.sep + i

	# get the text of the image
	text = p2t.pic2text(test_file)
	# save the image text to a file
	f = open(output_path+os.sep+i+'.txt', 'w')
	f.write(text)
	# f = open(output_path+os.sep+files[i]+'.txt', 'r', encoding='utf-8')
	# text = f.read()
	f.close()
	print(text)

# extract the products/prices from the text as a dictionary of values
receipt = t2o.text2object(text)
# display the Store Name, as well as each product and the associated price
products = receipt['PRODUCTS']
prices = receipt['PRICES']
name = receipt['NAME']
total = receipt['TOTAL']
print("Store NAME: ", name)
for i in range(len(products)):
	print("PRODUCT: {} => PRICE: {}".format(products[i], prices[i]))


# verify that the products extracted are accurate (

# preprocess product names for classification algorithm

# ML model for classification of product names

# User Interface
