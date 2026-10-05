from ultralytics import YOLO
import cv2 as cv
import math

class Detector():
    def __init__(self):
        self.model = YOLO("yolo11n.pt")
        self.owner_id = None
# Owner selection: whoever is closest to the center of the frame at the press of a buttion, then tracks that id
    def selectOwner(self, results, center):
        if results[0].boxes:
            closestToCenter = None
            min_d = float("inf")
            for box in results[0].boxes:
                if box.id is None:
                    continue
                x = box.xywh[0][0].item()
                y = box.xywh[0][1].item()
                objCenter = (x, y)
                d = math.sqrt((objCenter[0] - center[0])**2 + (objCenter[1] - center[1])**2)
                if d < min_d:
                    min_d = d
                    closestToCenter = box
            if closestToCenter is None:
                print("No tracked person to select. Try again")
                return False
                
            self.owner_id = int(closestToCenter.id.item())
            print(f"Owner selected with ID: {self.owner_id}")
            return True


    def deselectOwner(self):
        self.owner_id = None
        print(f"Owner deselected. Press 'W' to Choose a New Owner")

#  Drawing detections and returning the new frame

    def getDetections(self, frame):
        results = self.model.track(frame, verbose=False, classes=[0], persist=True, tracker="botsort.yaml")
        plotted_frame = results[0].plot()
        if self.owner_id is not None:
            for box in results[0].boxes:
                if box.id is None:
                    continue
                if int(box.id.item()) == self.owner_id:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv.rectangle(plotted_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.putText(plotted_frame, "Owner", (x1, y1 - 20), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        return plotted_frame, results



        

        


