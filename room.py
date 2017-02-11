from tools import *
import cv2
from math import ceil

class roomimage:
    def __init__(self, image):
        self.image = image
        # important locations
        self.office = ((400, 200), (650, 550))
        self.cabinet = ((850, 180), (1200, 700))
        self.door = ((0, 120), (300, 720))
        self.total = ((0, 0), (1280, 720))
        self.old_c = []
        
    def draw(self,swc1,swc2,center_of_mass,office_activity,cab_activity,door_activity):

        if swc2 and center_of_mass and swc2 > 0.05:
            cv2.circle(self.image, tuple(center_of_mass), 50, (0, 255, 25), thickness=-1)
            self.old_c = [center_of_mass, center_of_mass, center_of_mass, center_of_mass, center_of_mass, center_of_mass,center_of_mass]
        elif swc2 and center_of_mass and swc2 > 0.01 and swc1 > 0.005:
            cv2.circle(self.image, tuple(center_of_mass), 50, (0, 25, 255), thickness=-1)
            self.old_c = [center_of_mass, center_of_mass, center_of_mass, center_of_mass, center_of_mass, center_of_mass,center_of_mass]
        elif len(self.old_c) > 0:
            c = self.old_c.pop()
            cv2.circle(self.image, tuple(c), 50, (255, 25, 25), thickness=-1)


        cv2.rectangle(self.image, self.office[0], self.office[1], (255, 0, 0), thickness=min([int((10 * office_activity)), 30]))
        cv2.rectangle(self.image, self.cabinet[0], self.cabinet[1], (255, 255, 0), thickness=min([int(ceil(cab_activity)), 30]))
        cv2.rectangle(self.image, self.door[0], self.door[1], (0, 255, 255), thickness=min([int(ceil(door_activity)), 30]))



class binroomimage:
    def __init__(self, image):
        self.image = image 
        self.office = ((400, 200), (650, 550))
        self.cabinet = ((850, 180), (1200, 700))
        self.door = ((0, 120), (300, 720))
        self.total = ((0, 0), (1280, 720))
        
    def draw(self,win,win1,win2):
        cv2.rectangle(self.image, win[0], win[1], (255, 0, 0), thickness=1)
        cv2.rectangle(self.image, win1[0], win1[1], (255, 0, 0), thickness=1)
        cv2.rectangle(self.image, win2[0], win2[1], (255, 0, 0), thickness=1)