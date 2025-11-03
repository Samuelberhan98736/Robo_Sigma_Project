#sampe pusdo code until we get our parts

from gopigo_controller import GoPiGoContoller
from sensors import DistanceSensor
from communication.bluetooth_server import BluetoothSrver

robot = GoPiGoController()
sensor = DistanceSensor()
bt_server = BluetoothServer(robot)

while True:
    distance = sensor.get_distance()
    if distance < 20:
        robot.stop()
        robot.turn_right()
    bt_server.listen()