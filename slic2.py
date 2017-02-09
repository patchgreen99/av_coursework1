# import the necessary packages
import os
# import matplotlib.pyplot as plt
import argparse
import glob
import cv2
import numpy as np
from scipy import ndimage
from math import ceil
# from pykalman import KalmanFilter
# from tochroma import *
orig = sorted(glob.glob("day2/*.jpg"))
images = sorted(glob.glob("chroma/*.jpg"))

try:
	read_dictionary = np.load('labels.npy').item()
except:
	print "No labels found"


# important locations
office = ((400,200),(650,550))
cabinet = ((850,180),(1200,700))
door =  ((0,120),(300,720))
total = ((0,0),(1280,720))


possitions = []
labels = read_dictionary or {}
def fix_win(w,limits = (1280,720)):
	w1 = max([w[0][0],0])
	w2 = max([w[0][1],0])
	w3 = min([w[1][0],limits[0]])
	w4 = min([w[1][1],limits[1]])
	return ((w1,w2),(w3,w4))

def clip(img,w):
	return img[w[0][1]:w[1][1],w[0][0]:w[1][0]]

def is_in(p, area):
	return p[0] > area[0][0] and p < area[1][0] and p[1] > area[0][1] and p < area[1][1]

def sum_win_center(c,width,img):
	w = fix_win((c[1] - width, c[0] - width),(c[1] + width, c[0]+width))
	r = np.sum(img[w[0][0]:w[1][0],w[0][1]:w[1][1]])
	# This function returns the average activity in the area
	# This funciton sums up the activity white pixels in the window and divides by the total area
	w = ((c[0] - width, c[1] - width),(c[0] + width, c[1]+width))
	return r
def sum_win(w,img):
	# This function returns the summed activity in the area
	# This funciton sums up the activity white pixels in the window and divides by the total area
	return np.sum(img[w[0][0]:w[1][0],w[0][1]:w[1][1]])
def avg_win_center(c,width,img):
	# This function returns the average activity in the area
	# This funciton sums up the activity white pixels in the window and divides by the total area
	w = ((c[1] - width, c[0] - width),(c[1] + width, c[0]+width))
	s = np.sum(img[w[0][0]:w[1][0],w[0][1]:w[1][1]])
	a = (w[1][0]-w[0][0]) * (w[1][1]-w[0][1])
	w = fix_win(((c[0] - width, c[1] - width),(c[0] + width, c[1]+width)))
	return s/a ,w

def avg_win(w,img):
	# print w
	# This function returns the average activity in the area
	# This funciton sums up the activity white pixels in the window and divides by the total area
	return float(np.sum(img[w[0][1]:w[1][1],w[0][0]:w[1][0]])) / ((w[1][0]-w[0][0]) * (w[1][1]-w[0][1]))



cv2.namedWindow("Frame",0)
cv2.namedWindow("Final",0)

parser = argparse.ArgumentParser(description='Basic Single Person Motion Tracker')
parser.add_argument('-c', action="store", dest="c", type=int, help="Convert To Chroma")
parser.add_argument('-f', action="store", dest="f", type=int,help="Frame to Start")
parser.add_argument('-w', action="store", dest="w", type=int,default=1,help="Time Per frame")
parser.add_argument('-p', action="store", dest="folder", type=str,help="Path to images")
args = parser.parse_args()

if args.folder:
	orig =  orig = sorted(glob.glob(args.folder+"/*.jpg"))
works = args.c or 0
waittime = args.w
old_c = []

for x in range(len(orig)-1):

	# skip first x frames using -fs
	if x < args.f: continue
	print "Image:" , x, "of ", len(orig),orig[x+1][32:]
	leabel = labels.get(os.path.basename(orig[x+1]))
	# Pause on labeled images
	if 	leabel:
		print "LABLED IMAGE:", leabel
		waittime = 0
	else:
		waittime = args.w
	# read 2 chromaticity images and computer their absolute difference
	# or do on the spot 
	try:
		im3 = cv2.imread(orig[x+1])
		im4 = cv2.imread(orig[x])
		if works ==1:
			pass
			# im1 = toChroma2(im4)
			# im2 = toChroma2(im3)
		else:
			im1 = cv2.imread(images[x])
			im2 = cv2.imread(images[x+1])
	except:
		continue

	# remove noise

	th4 = cv2.absdiff(im3, im4)
	th4 = cv2.cvtColor(th4, cv2.COLOR_BGR2GRAY)
	ret,thresh1 = cv2.threshold(th4,80,255,cv2.THRESH_BINARY)

	# cleanup
	thresh1 = cv2.erode(thresh1, (1,1),iterations=1)
	thresh1 = cv2.dilate(thresh1, (1,1),iterations=4)
	thresh1 = cv2.erode(thresh1, (1,1),iterations=3)
	thresh1 = cv2.dilate(thresh1, (1,1),iterations=4)
	
	total_activity = avg_win(total, thresh1)
	print total_activity
	CoM = None
	CoM1 = None
	CoM2 = None
	# pass 1
	if total_activity > 0.05:
		try:
			CoM= ndimage.measurements.center_of_mass(thresh1)
			center_of_mass = [int(CoM[1]),int(CoM[0])]
			swc,win = avg_win_center(center_of_mass,250,thresh1)
			print win
			# Pass 2[w[0][1]:w[1][1],w[0][0]:w[1][0]]
			CoM1 = ndimage.measurements.center_of_mass(thresh1[win[0][1]:win[1][1],win[0][0]:win[1][0]])
			center_of_mass = [win[0][0] + int(CoM1[1]),win[0][1] + int(CoM1[0])]
			swc1,win1 = avg_win_center(center_of_mass,150 ,thresh1)

			# pass 3
			CoM2 = ndimage.measurements.center_of_mass(thresh1[win1[0][1]:win1[1][1],win1[0][0]:win1[1][0]])
			center_of_mass = [win1[0][0] + int(CoM2[0]),win1[0][1] + int(CoM2[1])]
			swc2,win2 = avg_win_center(center_of_mass,50 ,thresh1)
			
			print "act:",swc,swc1
			# Green circle
			# print "average",swc

			if swc2 and center_of_mass and swc2 > 0.05: 
				cv2.circle(im3, tuple(center_of_mass), 50, (0,255,25),thickness=-1) 
				old_c = [center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass]
			elif swc2 and center_of_mass and swc2 > 0.01 and swc1 > 0.005:
				cv2.circle(im3, tuple(center_of_mass), 50, (0,25,255),thickness=-1) 
				old_c = [center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass,center_of_mass]
			elif len(old_c) > 0 :
				c = old_c.pop()
				cv2.circle(im3, tuple(c), 50, (255,25,25),thickness=-1)

			cv2.rectangle(thresh1, win[0], win[1], (255,0,0),thickness = 1)
			cv2.rectangle(thresh1, win1[0], win1[1], (255,0,0),thickness = 1)
			cv2.rectangle(thresh1, win2[0], win2[1], (255,0,0),thickness = 1)
		except:
			print "Error or Empty",CoM,CoM1,CoM2
			cv2.rectangle(thresh1, win[0], win[1], (255,0,0),thickness = 1)
			cv2.rectangle(thresh1, win1[0], win1[1], (255,0,0),thickness = 1)
			cv2.rectangle(thresh1, win2[0], win2[1], (255,0,0),thickness = 1)
			waittime = 0
	else:
		print "No activity detected"
	
	
	



	# DRAW STUFF
	# office
	office_activity = avg_win(office,thresh1)
	cv2.rectangle(im3, office[0], office[1], (255,0,0),thickness = min([int((10*office_activity)),30]))
	# cabinet
	cab_activity =  avg_win(cabinet,thresh1)
	cv2.rectangle(im3, cabinet[0], cabinet[1], (255,255,0),thickness = min([int(ceil(cab_activity)),30]))
	# door
	door_activity = avg_win(door,thresh1)
	cv2.rectangle(im3, door[0], door[1], (0,255,255),thickness = min([int(ceil(door_activity)),30]))
	
	if waittime == 0:
		print "ACTIVITY"
		print "DOOR", "        OFFICE", "          Cabinet"
		print door_activity,office_activity,cab_activity
		print "Total      ", " Large  ","    Medium", "       Small"
		print total_activity, swc, swc1, swc2

	# SHOW	
	# Fast
	# im3 = clip(im3,office)
	try:
		cv2.imshow("Frame",im3)
		cv2.imshow("Final",thresh1)
		
	except:
		pass
	key = cv2.waitKey(waittime) & 0xFF
	if  key == ord("q"):
		break

	# Cool
	# im1,im2,im3,im4 = 
	# try:
	# 	bin_frames = np.concatenate([im1,im2],axis=1)
	# 	bin_frames = np.dstack([bin_frames,bin_frames,bin_frames])
	# 	col_frames = np.concatenate([im3,im4],axis=1)
	# 	all_frames = np.concatenate([col_frames,bin_frames],axis=0)
	# 	cv2.imshow("Frame",all_frames)
	# 	cv2.waitKey(waittime)
	# except:
	# 	pass
