import argparse
import cv2
import numpy as np
import glob
import os


store_at = 'labels_xy.npy'
parser = argparse.ArgumentParser(description='Label images')
parser.add_argument('-c', action="store", dest="c", type=int,default=10,help="Number of Images to Label")
parser.add_argument('-p', action="store", dest="folder", type=str,help="Path to images")
args = parser.parse_args()

refPt = None

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONUP:
		print "clicked at", (x,y)
		refPt = (x,y)
	if event == cv2.EVENT_RBUTTONUP:
		print "Deleted click"
		refPt = None

if args.folder:
	images = sorted(glob.glob(args.folder+"/*.jpg"))
else:
	images = sorted(glob.glob("day2/*.jpg"))


try:
	read_dictionary = np.load(store_at).item()
except:
	read_dictionary = {}
	print "No labels found"
	print "Creating new file called labels.npy"

cv2.namedWindow("winname",1)
cv2.setMouseCallback("winname", click_and_crop)
sample = np.random.choice(images,args.c)
d = read_dictionary or {}
np.save(store_at, d) 
images =[]
key = None
for   image_path in sample:
	refPt = None
	if key == ord("q"): break
	im1 = cv2.imread(image_path)
	filename = os.path.basename(image_path)
	d[filename] = [None,None]
	print  filename, "labeled as ", d.get(filename)
	while 1:
		cv2.imshow("winname", im1)
		key = None
		key = cv2.waitKey(0) & 0xFF
		if refPt:
			d[filename][0] = refPt
		if  key == ord("o"):
			print filename, "set as ","office"
			d[filename][1] = "office"
		if  key == ord("m"):
			print filename, "set as ","moving"
			d[filename][1] = "moving"
		if  key == ord("c"):
			print filename, "set as ","cabinet"
			d[filename][1] = "cabinet"
		if  key == ord("e"):
			print filename, "set as ","empty"
			d[filename][1] = "empty"
		if key == ord("n"):
			print d[filename]
			break
		if key == ord("q"):
			print d[filename]
			break
    

np.save(store_at, d) 
