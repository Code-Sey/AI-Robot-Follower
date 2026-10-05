import cv2 as cv
from camera import Camera
from detector import Detector
from controller import Controller

cam = Camera()
detections = Detector()
controller = Controller(port='COM7', baud=9600)
selectedOwner = False
owner_lost_frames = 0
MAX_LOST_FRAMES = 10

while cam.isRunning():
#  Getting the Frame
    working, frame, center_frame = cam.get_frame()
    if not working:
        break

    key = cv.waitKey(10) & 0xff
#  gets the frame with the detectoins drawn
    new_frame, results = detections.getDetections(frame)
    cv.imshow("AI Follow Robot Vision", new_frame)

#  Selecting the owner
    if key == ord('w') and not selectedOwner:
        detections.selectOwner(results, center_frame)
        selectedOwner = True
#  Deselcting Owner
    if key == ord('z') and selectedOwner:
        detections.deselectOwner()
        selectedOwner = False

#  sends information to controller about the owenrs bounding box
    owner_found = False
    for box in results[0].boxes:
        if box.id is not None and box.id.item() == detections.owner_id:
            x = box.xywh[0][0]
            w = box.xywh[0][2]
            h = box.xywh[0][3]
            controller.move(center_frame, x, h, w)
            owner_found = True
            break
#   stops the robot when the owner isnt detected.
    if not owner_found and selectedOwner:
        owner_lost_frames += 1
        if owner_lost_frames > MAX_LOST_FRAMES:
            controller.send_command("STOP")
    else:
        owner_lost_frames = 0

    # cv.imshow("AI Follow Robot Vision", new_frame)

    if key == ord('d'):
        controller.send_command("STOP")
        cam.release()
        break

cv.destroyAllWindows()



