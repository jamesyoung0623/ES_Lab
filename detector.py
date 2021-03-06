import numpy  as np
import cv2

def read_clip_mono(path):
    cap = cv2.VideoCapture(path)
    clip_buf = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break 
        mono = frame[:,:,1]
        clip_buf.append(mono)
    return clip_buf

class BlobDetector(object):
    def __init__(self, frame, hist=500, thres=16, kr=3):
        #maybe for use to detect only RoI in future
        self.roi = self.cut_roi(frame)
        #self.H, self.W = self.roi.shape 
        #background subtractor
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=hist, varThreshold=thres, detectShadows=False) 
        #define kernel
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kr,kr))  
        #set blob detector params
        blob_params = self.set_blob_params()
        self.blob_detector = cv2.SimpleBlobDetector_create(blob_params)

    def cut_roi(self, img):
        return img[0:480,0:640]

    def get_foreground(self, frame):
        fgmask = self.fgbg.apply(frame)  
        morph = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel) 
        return morph
            
    def set_blob_params(self):
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds 
        params.minThreshold = 0;
        params.maxThreshold = 200;
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 110    
        params.maxArea = 1000
        
        params.filterByConvexity = False
        params.filterByColor = False
        params.filterByInertia = False
        return params

    def draw_keypoint(self, img):
        inv_img = cv2.bitwise_not(img)
        keypoints = self.blob_detector.detect(inv_img)
        img = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('test', img)
        if keypoints:
            cv2.waitKey(0)
        else:
            CV2.waitKey(1)
    
    def detect_keypoint(self, frame):
        inv_img = cv2.bitwise_not(frame)
        keypoints = self.blob_detector.detect(inv_img)
        frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('hello', frame)
        cv2.waitKey(1)
        return keypoints

    def demo_video(self, clip):
        for i in range(len(clip)):
            fgmask = self.get_foreground(clip[i])
            self.draw_keypoint(fgmask)                


