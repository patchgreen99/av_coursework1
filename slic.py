# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse
import glob
import cv2
images = sorted(glob.glob("chroma/*.jpg"))
orig = sorted(glob.glob("day2/*.jpg"))


cv2.namedWindow("DIFFb",0)
cv2.namedWindow("DIFFg",0)
cv2.namedWindow("DIFFr",0)
cv2.namedWindow("NEW",0)

for x in range(len(images)-1):
	print x,images[x+1][32:], orig[x+1][32:]
	# if str(images[x+1][32:] != orig[x+1][32:]: break
	im1 = cv2.imread(images[x])
	im2 = cv2.imread(images[x+1])
	im3 = cv2.imread(orig[x+1])
	d = cv2.absdiff(im1,im2)
	
	norm_image = cv2.normalize(d, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
	norm_image_b = norm_image[:,:,0]
	norm_image_g = norm_image[:,:,1]
	norm_image_r = norm_image[:,:,2]
	# ret,thresh1 = cv2.threshold(norm_image_r,40,255,cv2.THRESH_BINARY)

	cv2.imshow("DIFFb",norm_image_b)
	cv2.imshow("DIFFg",norm_image_g)
	cv2.imshow("DIFFr",norm_image_r)
	cv2.imshow("NEW",im3)
	cv2.waitKey(0)
