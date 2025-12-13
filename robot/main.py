from communication.bluetooth_server import BluetoothServer
from robot.drive.gopigo_drive import GoPiGoController
from sensors import SensorSuite
from navigation import NavigationController
from robot.preception.object_detection import ObjectDetector

def main():
    controller = GoPiGoController()
    sensors = SensorSuite()
    detector = ObjectDetector()
    nav = NavigationController(controller, sensors, detector)

    server = BluetoothServer(nav, controller, sensors)
    server.start()

if __name__ == "__main__":
    main()
