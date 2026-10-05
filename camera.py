import cv2 as cv

class Camera():
    def __init__(self):
        self.capture = cv.VideoCapture(0)

    def get_frame(self):
        isTrue, frame = self.capture.read()
        height, width = frame.shape[:2]
        halfHeight = height/2
        halfWidth = width/2
        centerFrame = (halfWidth, halfHeight)
        return isTrue, frame, centerFrame

    def isRunning(self):
        return self.capture.isOpened()

    def release(self):
        self.capture.release()
    
          
          
          


      
    
      
