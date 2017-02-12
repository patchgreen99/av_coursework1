# import the necessary packages
import os
# import matplotlib.pyplot as plt
import argparse
import glob
import cv2
import numpy as np
from scipy import ndimage
from math import ceil
from tools import *
from room import roomimage, binroomimage
# from tochroma import *

cv2.namedWindow("Frame", 0)
cv2.namedWindow("Final", 0)

parser = argparse.ArgumentParser(description='Basic Single Person Motion Tracker')
parser.add_argument('-c', action="store", dest="c", type=int, help="Convert To Chroma")
parser.add_argument('-f', action="store", dest="f", type=int, help="Frame to Start", default = 0)
parser.add_argument('-w', action="store", dest="w", type=int, default=1, help="Time Per frame")
parser.add_argument('-p', action="store", dest="folder", type=str, help="Path to images")
args = parser.parse_args()


errors = []
room = roomimage()
binaryroom = binroomimage()
prev_com = None
center_of_mass = None
kfmeasurements = None
previnitstate = None
filtered_state_means = None
curstate = None
miss_detections = []
state = "start"
with file("transpoints.txt","w") as f:
    x=args.f

    for waittime,im3,im4,im_label,dT in getimages(args):
        room.image = im3

        # remove noise

        th4 = cv2.absdiff(im3, im4)
        th4 = cv2.cvtColor(th4, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(th4, 80, 255, cv2.THRESH_BINARY)

        # cleanup
        thresh1 = cv2.erode(thresh1, (1, 1), iterations=1)
        thresh1 = cv2.dilate(thresh1, (1, 1), iterations=4)
        thresh1 = cv2.erode(thresh1, (1, 1), iterations=3)
        thresh1 = cv2.dilate(thresh1, (1, 1), iterations=4)

        binaryroom.image = thresh1

        office_activity = avg_win(room.office, binaryroom.image)
        cab_activity = avg_win(room.cabinet, binaryroom.image)
        door_activity = avg_win(room.door, binaryroom.image)
        total_activity = avg_win(room.total, binaryroom.image)


        #print total_activity
        CoM = None
        CoM1 = None
        CoM2 = None
        swc1, swc2,center_of_mass = None, None, None
        # pass 1
        if total_activity > 0.05:
            #try:
                CoM = ndimage.measurements.center_of_mass(binaryroom.image)
                center_of_mass = [int(CoM[1]), int(CoM[0])]
                swc, win = avg_win_center(center_of_mass, 250, binaryroom.image)

                # Pass 2[w[0][1]:w[1][1],w[0][0]:w[1][0]]
                CoM1 = ndimage.measurements.center_of_mass(binaryroom.image[win[0][1]:win[1][1], win[0][0]:win[1][0]])
                center_of_mass = [win[0][0] + int(CoM1[1]), win[0][1] + int(CoM1[0])]
                swc1, win1 = avg_win_center(center_of_mass, 150, binaryroom.image)

                # pass 3
                CoM2 = ndimage.measurements.center_of_mass(binaryroom.image[win1[0][1]:win1[1][1], win1[0][0]:win1[1][0]])
                center_of_mass = [win1[0][0] + int(CoM2[0]), win1[0][1] + int(CoM2[1])]
                swc2, win2 = avg_win_center(center_of_mass, 50, binaryroom.image)

           # except:
                #print "Error or Empty", CoM, CoM1, CoM2
                waittime = 0

                binaryroom.draw(win, win1, win2)

        else:
            center_of_mass = None
            print "No activity detected"

        # USE the state machine to decide whether the position is valid
        if state and state == "outside" and total_activity > 1:
            state = room.changestate(office_activity, cab_activity, door_activity, total_activity)
            center_of_mass = None
        elif state == "start" and total_activity < 0.08:
            # if we initialize on a frame with no activity, avoid getting locked outside
            pass
        elif state == "outside":
            pass
            center_of_mass = None
            # state = room.changestate(office_activity, cab_activity, door_activity, total_activity)
        else :
            state = room.changestate(office_activity, cab_activity, door_activity, total_activity)
        print state
        if not center_of_mass and prev_com != None:
            if state in ["desk","cabinet","room"]:
                center_of_mass = tuple(prev_com)

        room.draw(swc1, swc2, center_of_mass, dT, office_activity, cab_activity, door_activity)

        # if waittime == 0 and (im_label[0]) :
        #     print "ACTIVITY"
        #     print "DOOR", "        OFFICE", "          Cabinet" , "COM"
        #     print door_activity, office_activity, cab_activity, center_of_mass
        #     if center_of_mass and swc2:
        #         print "Total      ", " Large  ", "    Medium", "       Small"
        #         print total_activity, swc, swc1, swc2, center_of_mass
        #     if im_label[0] and center_of_mass:
        #         error_dist = eucl_dist(center_of_mass,im_label[0])
        #         errors.append(error_dist*error_dist)
        #     if  not center_of_mass and not im_label[0]:
        #         errors.append(0)
        #     waittime = 10
        #     if center_of_mass and not im_label[0]:
        #         miss_detections.append(x)
        #         waittime = 0
        #
        # else:
        #     waittime = 10




        # SHOW
        # Fast
        # im3 = clip(im3,office)
        try:
            cv2.imshow("Frame", room.image)
            cv2.imshow("Final", binaryroom.image)

        except:
            pass
        key = cv2.waitKey(waittime) & 0xFF
        if key == ord("q"):
            break
            print "RMSE (in pixels)" , np.sqrt(np.average(errors))
            print "Missdetected frames", miss_detections

        x+=1
    print "RMSE (in pixels)" , np.sqrt(np.average(errors)), "in ", len(errors), " labeled images"
    print "Missdetected frames", miss_detections
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
