import numpy
import time
import math
import os
import glob
import cv2
from keras.models import Sequential
from keras.models import load_model



def teeth_detection(image):
	S_model = load_model('./vgg_lr0.001_epoch297_0.882.h5')
	result = S_model.predict(image)
	result = result[0]
	result = numpy.array(result)
	print(numpy.argmax(result))
def img_reshape(image):
	image = image[40:460,160:520,:]
	cv2.imwrite('dox.jpg',image)
	image = cv2.resize(image, (224,224))		
	return image

while 1:
	image = cv2.imread('test1.jpg')
	image = numpy.array(image)
	image = img_reshape(image)
	image = numpy.reshape(image,(1,224,224,3))
	teeth_detection(image)

#print(image.shape)
#cv2.imwrite('curr.jpg',image)
"""
while 1:
	time.sleep(2)
	image = cv2.imread('test1.jpg')
	image = numpy.array(image)
	#image = RUN.img_reshape(image)
	teeth_detection(image)
"""