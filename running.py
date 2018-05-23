import numpy
import time
import math
import os
import glob
import cv2
from keras.models import Sequential
from keras.models import load_model

S_model = load_model('./test_model.h5')
def teeth_detection(image):
	result = S_model.predict(image)
	result = result[0]
	result = numpy.array(result)
	print(numpy.argmax(result))
	answer = numpy.argmax(result)
	'''
	flag is in the flag.npy
	if flag != 0
		1. do labeling
			a. creeate 16 directory
			b. open text file to record the filename
			c. create file with name record in text file
		2. calculate accuracy
			a. if result != flag then print no else yes
			b. record in the text file named acc.txt
		3. statistic
			create confusion 2d-array 
	else 
		print(numpy.argmax(result))
	'''
	flag = numpy.load('flag.npy')
	#print("flag:",flag)
	if flag!=0:
		name_num = 'label_image/' + str(flag) + '/' + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + '.jpg'
		print(name_num)
		save_image = numpy.reshape(image,(224,224,3))
		print(save_image.shape)
		cv2.imwrite(name_num,save_image)
		#wait until model is real
		"""
		confusion_matric = numpy.load('con_matric.npy')
		confusion_matric[flag-1][answer]+=1
		numpy.save('con_matric.npy',confusion_matric)
		"""
	
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
