# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse
import glob
import cv2,os
images = sorted(glob.glob("day2/*.jpg"))
done_images = sorted(glob.glob("chroma/*.jpg"))


def mynorm(image):
	image = cv2.normalize(image,image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F) 
	return image

def toChroma(image):
	for x in xrange(image.shape[0]):
		for y in xrange(image.shape[1]):
			try:
				p = image[x,y]
				sump = sum(p)
				image[x,y] = [255*p[0]/sump,255*p[1]/sump,255*p[2]/sump]
			except KeyboardInterrupt:
				break
	return image

for i,x in enumerate(images):
	done_images = sorted(glob.glob("chroma/*.jpg"))
	done_images = [os.path.basename(x)==os.path.basename(y) for y in done_images]
	done = any(done_images)
	print str(i) +  " / " + str(len(images)) + " Done   ( ", 100*i / len(images), "%  )"
	if done: continue
	im1 = cv2.imread(x)
	im2 = toChroma(im1)
	cv2.imshow("NEW",im2)
	xs = str(i)
	while len(xs) < len(str(len(images))): xs = "0" + xs
	filename = "chroma/"+ x[5:]
	print "saved: ", filename
	cv2.imwrite(filename, im2)
	# cv2.waitKey(2)
