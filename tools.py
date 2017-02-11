import numpy as np
import os
import cv2
import glob

def fix_win(w, limits=(1280, 720)):
    w1 = max([w[0][0], 0])
    w2 = max([w[0][1], 0])
    w3 = min([w[1][0], limits[0]])
    w4 = min([w[1][1], limits[1]])
    return ((w1, w2), (w3, w4))


def eucl_dist(p1,p2):
    dx = np.abs(p1[0] - p2[0])
    dy = np.abs(p1[1] - p2[1])
    return np.sqrt(dx*dx + dy*dy)

def clip(img, w):
    return img[w[0][1]:w[1][1], w[0][0]:w[1][0]]


def is_in(p, area):
    return p[0] > area[0][0] and p < area[1][0] and p[1] > area[0][1] and p < area[1][1]


def sum_win_center(c, width, img):
    w = fix_win((c[1] - width, c[0] - width), (c[1] + width, c[0] + width))
    r = np.sum(img[w[0][0]:w[1][0], w[0][1]:w[1][1]])
    # This function returns the average activity in the area
    # This funciton sums up the activity white pixels in the window and divides by the total area
    w = ((c[0] - width, c[1] - width), (c[0] + width, c[1] + width))
    return r


def sum_win(w, img):
    # This function returns the summed activity in the area
    # This funciton sums up the activity white pixels in the window and divides by the total area
    return np.sum(img[w[0][0]:w[1][0], w[0][1]:w[1][1]])


def avg_win_center(c, width, img):
    # This function returns the average activity in the area
    # This funciton sums up the activity white pixels in the window and divides by the total area
    w = ((c[1] - width, c[0] - width), (c[1] + width, c[0] + width))
    s = np.sum(img[w[0][0]:w[1][0], w[0][1]:w[1][1]])
    a = (w[1][0] - w[0][0]) * (w[1][1] - w[0][1])
    w = fix_win(((c[0] - width, c[1] - width), (c[0] + width, c[1] + width)))
    return s / a, w


def avg_win(w, img):
    # print w
    # This function returns the average activity in the area
    # This funciton sums up the activity white pixels in the window and divides by the total area
    return float(np.sum(img[w[0][1]:w[1][1], w[0][0]:w[1][0]])) / ((w[1][0] - w[0][0]) * (w[1][1] - w[0][1]))


def getimages(args):
    try:
        read_dictionary = np.load('labels_xy.npy').item()
    except:
        print "No labels found"

    labels = read_dictionary or {}

    orig = sorted(glob.glob("day2/*.jpg"))
    images = sorted(glob.glob("chroma/*.jpg"))

    if args.folder:
        orig = sorted(glob.glob(args.folder+"/*.jpg"))
    works = args.c or 0
    waittime = args.w

    for x in range(len(orig) - 1):

        # skip first x frames using -fs
        if x < args.f: continue
        print "Image:", x, "of ", len(orig), orig[x + 1][32:]
        label = labels.get(os.path.basename(orig[x + 1]))
        # Pause on labeled images
        if label:
            print "LABLED IMAGE:", label
            waittime = 0
        else:
            waittime = args.w
            label = None
        # read 2 chromaticity images and computer their absolute difference
        # or do on the spot

        im3 = cv2.imread(orig[x + 1])
        im4 = cv2.imread(orig[x])
        if works == 1:
            pass
        # im1 = toChroma2(im4)
        # im2 = toChroma2(im3)
        else:
            im1 = cv2.imread(images[x])
            im2 = cv2.imread(images[x + 1])


        yield waittime, im3, im4 , label





############################################################
# Kalman filter and condensation tracking implementation

############################################################


class condensation():
    def __init__(self):
        self.samples = np.array([])
        self.numsamples = 10

    def generate_samples(self, x, p, time):
        """
        :param x: state vector
        :param p: probability
        :return:
        """
        oldselections = self.samples[np.random.randint(0,self.numsamples,self.numsamples)]
        xc = x[oldselections,time-1,:]







