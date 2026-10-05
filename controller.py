import serial
import time

class Controller():
    def __init__(self, port='COM7', baud=9600):
        self.bounding_area = 70000
        self.last_command = None
        self.DEAD_ZONE = 150
        try:
            self.arduino = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print(f"Connected to Arduino on {port}")
        except Exception as e:
            self.arduino = None
            print(f"No Arduino: {e}")

    def send_command(self, cmd):
        if cmd != self.last_command:
            if self.arduino and self.arduino.is_open:
                self.arduino.write((cmd + '\n').encode())
                print(f"Sent: {cmd}")
            self.last_command = cmd

    def move(self, center_of_frame, owner_x, owner_h, owner_w):
        center_x, center_y = center_of_frame
        owner_x = float(owner_x)
        owner_h = float(owner_h)
        owner_w = float(owner_w)
        off_center = owner_x - center_x
        owner_area = owner_w * owner_h
        too_far = owner_area < self.bounding_area
        print(f"off_center: {off_center:.1f} | area: {owner_area:.0f} | too_far: {too_far}")

        if too_far:
            if off_center < -self.DEAD_ZONE:
                self.send_command("FR")
            elif off_center > self.DEAD_ZONE:
                self.send_command("FL")
            else:
                self.send_command("F")
        else:
            if off_center < -self.DEAD_ZONE:
                self.send_command("L")
            elif off_center > self.DEAD_ZONE:
                self.send_command("R")
            else:
                self.send_command("STOP")

    def stop(self):
        self.send_command("STOP")
            

        
















            



