class FakeController:
    """
    A Fake Controller that helps us test without the robot present
    """
    
    def __init__(self, port=None, baud=None):
        print("Fake controller, no hardware")
    def move(self, center_frame, x, h, w):
        print(f"move: x={x:.0f} w={w:.0f} h={h:.0f}")
    def send_command(self, cmd):
        print(f"command: {cmd}")