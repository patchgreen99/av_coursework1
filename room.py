from tools import *
import cv2
from pykalman import KalmanFilter
from math import ceil

class roomimage:
    def __init__(self):
        self.image = None
        # important locations
        self.office = ((360, 120), (700, 620))
        self.cabinet = ((850, 180), (1200, 700))
        self.door = ((0, 120), (300, 720))
        self.total = ((0, 0), (1280, 720))
        self.measurements = []
        self.states = ["working_at_desk","at_cabinets","just_in_the_room","at_the_door","outside_the_room","start"]
        self.statemarkings = [self.office[0],self.cabinet[0],self.total[0],self.door[0]]
        self.tag = ["desk","cabinet","room","room","outside"]
        self.curstate = 5

        
    def changestate(self,office_activity,cab_activity,door_activity,total_activity):
        prev_state = self.curstate
        room_activity = (total_activity * area(self.total) - office_activity * area(self.office) - cab_activity * area(
            self.cabinet) - door_activity * area(self.door)) \
                        / (area(self.total) * area(self.office) * area(self.cabinet) * area(self.door))
        no_activity = 0
        if total_activity == 0:
            no_activity =1
        transitions =  {"working_at_desk" :[office_activity+no_activity,cab_activity,room_activity,door_activity,0,0],
                        "at_cabinets"     :[office_activity,cab_activity+no_activity,room_activity,door_activity,0,0],
                        "just_in_the_room":[office_activity,cab_activity,room_activity+no_activity,door_activity,0,0],
                        "at_the_door"     :[office_activity,cab_activity,room_activity,door_activity,no_activity,0],
                        "outside_the_room":[0,0,0,door_activity,no_activity,0],
                        "start"           :[office_activity,cab_activity,room_activity,door_activity,no_activity,0]}
        decision = np.array(transitions[self.states[self.curstate]])
        # THIS SOMETIMES fails and defaults to 0 so when we are outside we just straight to the desl
        self.curstate = np.argmax(decision/np.sum(decision))
        if prev_state == 4 and (self.curstate in [0,1]):
            self.curstate = 4
        return self.tag[self.curstate]

        
    def draw(self,swc1,swc2,center_of_mass,dT,office_activity,cab_activity,door_activity):
        if center_of_mass is not None:
            self.measurements.append(center_of_mass)


            # Kalman filter

            curstate = np.array([self.measurements[-2,0], self.measurements[-2,1], (self.measurements[-1,0] - self.measurements[-2,0]) / dT,
                                 (self.measurements[-1,1] - self.measurements[-2,1]) / dT])

            if previnitstate is not None:
                transition_matrices = np.array([[1, 0, dT, 0], [0, 1, 0, dT], [0, 0, 1, 0], [0, 0, 0, 1]])
                observation_matrices = [[1, 0, 0, 0], [0, 1, 0, 0]]

                initcovariance = 1.0e-3 * np.eye(4)
                transistionCov = 1.0e-4 * np.eye(4)
                observationCov = 1.0e-1 * np.eye(2)
                kf = KalmanFilter(transition_matrices=transition_matrices,
                                  observation_matrices=observation_matrices,
                                  initial_state_mean=previnitstate,
                                  initial_state_covariance=initcovariance,
                                  transition_covariance=transistionCov,
                                  observation_covariance=observationCov)

                print previnitstate
                print curstate
                (filtered_state_means, filtered_state_covariances) = kf.filter([previnitstate, curstate])

                previnitstate = curstate



            if swc2 and center_of_mass is not None and swc2 > 0.05:
                cv2.circle(self.image, tuple(center_of_mass), 50, (0, 255, 25), thickness=-1)
            elif swc2 and center_of_mass is not None and swc2 > 0.01 and swc1 > 0.005:
                cv2.circle(self.image, tuple(center_of_mass), 50, (0, 25, 255), thickness=-1)
            else:
                cv2.circle(self.image, tuple(center_of_mass), 50, (182, 24, 255), thickness=-1)

            for idx in range(len(self.measurements)-1):
                cv2.line(self.image, tuple(self.measurements[idx]), tuple(self.measurements[idx+1]), (0, 25, 255),
                         thickness=1)

            if len(self.measurements) > 6:
                del self.measurements[0]



        cv2.rectangle(self.image, self.office[0], self.office[1], (255, 0, 0), thickness=min([int((10 * office_activity)), 30]))
        cv2.rectangle(self.image, self.cabinet[0], self.cabinet[1], (255, 255, 0), thickness=min([int(ceil(cab_activity)), 30]))
        cv2.rectangle(self.image, self.door[0], self.door[1], (0, 255, 255), thickness=min([int(ceil(door_activity)), 30]))

        if self.curstate < 4:
            cv2.circle(self.image, self.statemarkings[self.curstate], 30, (25,255,255), thickness=-1)



class binroomimage:
    def __init__(self):
        self.image = None
        self.office = ((400, 200), (650, 550))
        self.cabinet = ((850, 180), (1200, 700))
        self.door = ((0, 120), (300, 720))
        self.total = ((0, 0), (1280, 720))
        
    def draw(self,win,win1,win2):
        cv2.rectangle(self.image, win[0], win[1], (255, 0, 0), thickness=1)
        cv2.rectangle(self.image, win1[0], win1[1], (255, 0, 0), thickness=1)
        cv2.rectangle(self.image, win2[0], win2[1], (255, 0, 0), thickness=1)