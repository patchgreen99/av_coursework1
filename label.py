import argparse
import cv2
import numpy as np
import glob
import os

parser = argparse.ArgumentParser(description='Label images')
parser.add_argument('-c', action="store", dest="c", type=int,default=10,help="Number of Images to Label")
parser.add_argument('-p', action="store", dest="folder", type=str,help="Path to images")
args = parser.parse_args()

if args.folder:
	images = sorted(glob.glob(args.folder+"/*.jpg"))
else:
	images = sorted(glob.glob("day2/*.jpg"))


try:
	read_dictionary = np.load('labels.npy').item()
except:
	print "No labels found"
	print "Creating new file called labels.npy"


sample = np.random.choice(images,args.c)
d = read_dictionary or {}
np.save('labels.npy', d) 
images =[]
key = None
for   image_path in sample:
	if key == ord("q"): break
	im1 = cv2.imread(image_path)
	filename = os.path.basename(image_path)
	print  filename, "labeled as ", d.get(filename)
	while 1:
		cv2.imshow("winname", im1)
		key = None
		key = cv2.waitKey(0) & 0xFF
		if  key == ord("o"):
			print filename, "set as ","office"
			d[filename] = "office"
		if  key == ord("m"):
			print filename, "set as ","moving"
			d[filename] = "moving"
		if  key == ord("c"):
			print filename, "set as ","cabinet"
			d[filename] = "cabinet"
		if  key == ord("e"):
			print filename, "set as ","empty"
			d[filename] = "empty"
		if key == ord("n"):
			break
		if key == ord("q"):
			break
    

np.save('labels.npy', d) 
