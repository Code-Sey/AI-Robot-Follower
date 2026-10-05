import cv2 as cv

class Camera():
    def __init__(self):
        self.capture = cv.VideoCapture(0)

    def get_frame(self):
        isTrue, frame = self.capture.read()
        if not isTrue:
            return False,None, None
        height, width = frame.shape[:2]
        centerFrame = (width/2, height/2)
        return isTrue, frame, centerFrame

    def isRunning(self):
        return self.capture.isOpened()

    def release(self):
        self.capture.release()
    
          
          
          


      
    
      
