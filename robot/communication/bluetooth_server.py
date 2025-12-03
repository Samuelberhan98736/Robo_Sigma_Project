"""
bluetooth_server.py
Handles Bluetooth communication with a phone / laptop.

Protocol (simple text commands, one per line):
  START_AUTO       -> robot starts driving with obstacle avoidance
  STOP             -> robot stops
  PILL_SCAN        -> run pill detection behavior
  PING             -> respond with 'PONG'
"""

import json
import threading
from pathlib import Path

from navigation import NavigationController
from gopigo_controller import GoPiGoController
from sensors import SensorSuite

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

try:
    import bluetooth  # PyBluez
except ImportError:
    bluetooth = None
    print("[WARN] PyBluez not installed; BluetoothServer will not run.")


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


class BluetoothServer:
    def __init__(
        self,
        nav: NavigationController,
        controller: GoPiGoController,
        sensors: SensorSuite,
    ):
        self.nav = nav
        self.controller = controller
        self.sensors = sensors
        self.cfg = load_config()
        self.running = False

    def start(self):
        if bluetooth is None:
            print("[ERROR] Bluetooth not available on this system.")
            return

        self.running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        print("[BT] Bluetooth server thread started.")

        # Keep main thread alive
        try:
            while self.running:
                pass
        except KeyboardInterrupt:
            print("[BT] KeyboardInterrupt: stopping server.")
            self.running = False

    def _run_server(self):
        service_name = self.cfg["bluetooth"]["service_name"]
        uuid = self.cfg["bluetooth"]["uuid"]

        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        bluetooth.advertise_service(
            server_sock,
            service_name,
            service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )

        print(f"[BT] Waiting for connection on RFCOMM channel {port}...")

        while self.running:
            client_sock, client_info = server_sock.accept()
            print(f"[BT] Accepted connection from {client_info}")
            try:
                self._handle_client(client_sock)
            finally:
                client_sock.close()

        server_sock.close()
        print("[BT] Server socket closed.")

    def _handle_client(self, sock):
        sock.send(b"CONNECTED\n")
        while self.running:
            data = sock.recv(1024)
            if not data:
                break
            cmd = data.decode("utf-8").strip().upper()
            print(f"[BT] Received command: {cmd}")
            resp = self._handle_command(cmd)
            if resp is not None:
                sock.send((resp + "\n").encode("utf-8"))

    # ---------- Command handling ----------

    def _handle_command(self, cmd: str) -> str | None:
        if cmd == "PING":
            return "PONG"

        if cmd == "START_AUTO":
            threading.Thread(target=self.nav.drive_forward_safe, daemon=True).start()
            return "OK"

        if cmd == "STOP":
            self.controller.stop()
            return "OK"

        if cmd == "PILL_SCAN":
            threading.Thread(target=self.nav.search_for_pill, daemon=True).start()
            return "PILL_SCAN_STARTED"

        if cmd == "DIST":
            d = self.sensors.get_front_distance()
            return f"DIST {d:.1f}"

        return "UNKNOWN_COMMAND"
