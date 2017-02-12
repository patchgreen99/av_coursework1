import argparse
import cv2
import numpy as np
import glob
import os


store_at = 'labels_xy.npy'
help_text = "Label Images \n " + \
 "Annotate a random sample if images by clicking" + \
 "Delete coordinates by right click \n" + \
 "press n to go to next \n" + \
 "press q to go to quit and save \n" + \
 "run with -m 1 to manage the dictionary \n"


parser = argparse.ArgumentParser(description=help_text)
parser.add_argument('-c', action="store", dest="c", type=int,default=10,help="Number of Images to Label")
parser.add_argument('-p', action="store", dest="folder", type=str,help="Path to images")
parser.add_argument('-m', action="store", dest="m", type=int,help="Manage images",default = None)
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
	dirpath = args.folder + "/"
	images = sorted(glob.glob(args.folder+"/*.jpg"))
else:
	images = sorted(glob.glob("images_folder/*.jpg"))
	dirpath = "day2/"

try:
	read_dictionary = np.load(store_at).item()
	print "DICTIONARY CONTAINS:", len(read_dictionary), "Labels"
except:
	read_dictionary = {}
	print "No labels found"
	print "Creating new file called labels.npy"

cv2.namedWindow("winname",1)
cv2.setMouseCallback("winname", click_and_crop)

if not args.m:
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
elif args.m == 1:
	d = read_dictionary or {}
	key = None
	for_deletion = []
	for filename, label in d.iteritems():
		if key == ord("q"): break
		im1 = cv2.imread(dirpath+filename)
		# if d[filename][0]: cv2.circle(im1,d[filename][0], 50, (0, 0, 255), thickness=-1)
		print  filename, "labeled as ", label
		refPt = d[filename][0]
		while 1:
			try:
				if d[filename][0]:
					print d[filename][0]
					cv2.circle(im1,d[filename][0], 50, (255, 0, 255), thickness=-1)
			except:
				print filename, "label deleted"
				for_deletion.append(filename)
				break
			cv2.imshow("winname", im1)
			key = None
			key = cv2.waitKey(0) & 0xFF
			d[filename][0] = refPt
			refPt = None
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
			if  key == ord("d"):
				print filename, "label deleted"
				for_deletion.append(filename)
				break
			if key == ord("n"):
				print d[filename]
				break
			if key == ord("q"):
				print d[filename]
				break
	for filename in for_deletion:
		del d[filename]
		print filename, "deleted"

    

np.save(store_at, d)
print "DICTIONARY CONTAINS:", len(d), "Labels"
