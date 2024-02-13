# Path: cameras/init.py
import numpy as np
from scipy import linalg, optimize, signal
from scipy.spatial.transform import Rotation

from pseyepy import Camera, Display
import cv2 as cv

import os
import json

class Camera_Wrapper:
    CAMERAIDS = [0, 1, 2, 3] # TODO: currently hard-coded, but should be read from a config file
    def __init__(self):
        dirname = os.path.dirname(__file__) #
        filename = os.path.join(dirname, "jyjblrds_cam_param.json") #TODO: a) why does he need 4 identical camara param json objects? b) tweak params
        f = open(filename)
        self.camera_params = json.load(f)
        
        #c = Camera([0,1], fps=[30, 60], resolution=[Camera.RES_LARGE, Camera.RES_SMALL], colour=[True, False])
        self.cams = Camera(ids=CAMERAIDS, fps=90, auto_gain=true) #  TODO: tweak: gain (0-63), exposure (0-1023), auto_gain (True/False), auto_exposure (True/False), auto_white_balance (True/False), white_balance (0-63)
        self.disp = Display(c) # begin the display
        
    def test(self):
        print("Testing")
        self.cams.checkfps()
        
        
    def edit_cams(self, exposure, gain, white_balance): # TODO: maybe individual camera control and seperate exposure, gain, white_balance
        self.cams.exposure = [exposure]*len(self.CAMERAIDS)
        self.cams.gain = [gain]*len(self.CAMERAIDS)
        self.cams.white_balance = [white_balance]*len(self.CAMERAIDS)
        
    def get_frames(self):
        #  camera.read() returns a list of frames, one per camera controlled by the object
        frames = self.cams.read(timestamp=False, squeeze=True)
        
        for i in range(len(self.CAMERAIDS)): #THIS IS DIRECTLY FROM jyjblrd's CODE, I'm assuming he calibrated the cameras correctly FIXME: check calibration
            frames[i] = cv.cvtColor(frames[i], cv.COLOR_BGR2RGB)
            frames[i] = np.rot90(frames[i], k=self.camera_params[i]["rotation"])
            frames[i] = make_square(frames[i])
            frames[i] = cv.undistort(frames[i], self.get_camera_params(i)["intrinsic_matrix"], self.get_camera_params(i)["distortion_coef"])
            frames[i] = cv.GaussianBlur(frames[i],(9,9),0)
            kernel = np.array([[-2,-1,-1,-1,-2],
                               [-1,1,3,1,-1],
                               [-1,3,4,3,-1],
                               [-1,1,3,1,-1],
                               [-2,-1,-1,-1,-2]])
            frames[i] = cv.filter2D(frames[i], -1, kernel)
        
        return np.hstack(frames)
    
    def get_points(self):
        #TODO: implement
    
    
    
    def get_camera_params(self, cam_id): # In case i decide to have individual camera params
        return self.camera_params[cam_id]
    
    def close(self):
        self.cams.close()
        self.disp.close()
        
    def __del__(self):
        self.close()
    