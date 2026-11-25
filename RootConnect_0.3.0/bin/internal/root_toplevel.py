from PySide6.QtWidgets import (QMainWindow, QFrame, QComboBox, QVBoxLayout, QFormLayout, 
                               QLabel, QScrollArea, QSizePolicy, QSlider, QWidget, QMessageBox)
from PySide6.QtCore import Qt, Signal, QSize

from threading import Thread
from asyncio import run as run_asyncio
from bleak import BleakScanner

from internal.__init__ import __bin_dir__, __cache_dir__
from internal.theme import Theme, Icons
from internal.clock import sleep
from internal.root_widgets import RootButton, ConnectionButton

class AddWindow(QMainWindow):
    device_thread = Signal()
    header_thread = Signal(str)
    header_status = Signal(int)
    
    def __init__(self, sw=0, sh=0, parent=None, window_title="RC - Window") -> None:
        super().__init__(parent)
        
        self.ble_devices: list = []
        self.selected_button: list[str|str]|None = None
        
        self.setWindowTitle(window_title)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setGeometry(int(sw/2-200),int(sh/2-300),400,600)
        
        self.central = QWidget()
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setSpacing(20)
        self.setCentralWidget(self.central)
        
        self.setStyleSheet(Theme.get_stylesheet("add_window.css"))
        self.device_thread.connect(self.add_device_buttons)
        self.header_thread.connect(self.update_header)
        self.header_status.connect(self.change_header_status)
        
        self.initWindow()
        self.central_layout.addWidget(self.header_text, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.addWidget(self.scroll_area)
        
    def initWindow(self) -> None:
        self.header_text = QLabel(text="Searching Nearby.")
        self.header_text.setObjectName("device_header")
        
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(10)
        self.container.setObjectName("device_scroll_area")
        self.connection_buttons: list = []
        
        Thread(target=self.scan_environment, daemon=True).start()
        Thread(target=self.animate_header_text, daemon=True).start()
        
        self.scroll_area = QScrollArea(self, widgetResizable=True)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setWidget(self.container)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setObjectName("device_scroll_area")
        
    def update_header(self, msg: str) -> None:
        self.header_text.setText(msg)
        
    def animate_header_text(self) -> None:
        sleep(0.5)    
        self.header_thread.emit("Searching Nearby..")
        sleep(0.5)
        self.header_thread.emit("Searching Nearby...")
        sleep(0.5)    
        self.header_thread.emit("Searching Nearby....")
        sleep(1)
        
    def change_header_status(self, status:int) -> None:
        match status:
            case 0: 
                QMessageBox.information(None, "RC - Info", "No devices found! Make sure your device is powered on and ready!")
                self.close()
            case 1: self.header_text.setText("Available Devices")
        
    def add_device_buttons(self) -> None:
        count: int = 0
        for device in self.ble_devices:
            button = ConnectionButton(Icons.connectivity)
            button.changeText(device[1], device[0])
            button.clicked.connect(lambda id=count: self.kill_window(id))
            button.setObjectNames("device_button","device_name_label","device_address_label")
            
            self.container_layout.addWidget(button, count, Qt.AlignmentFlag.AlignTop)
            self.connection_buttons.append(button)
            count += 1
        self.container_layout.addStretch(50)
    
    def kill_window(self, button_id) -> None:
        self.selected_button = self.connection_buttons[button_id].returnButtonText()
        self.close()
        
    def scan_environment(self) -> None:
        run_asyncio(self.find_devices())
        
    def count_char(self, string:str, char:str) -> int:
        count: int = 0
        for i in string:
            if i == char: count += 1
        return count
        
    async def find_devices(self) -> None:
        _ble_devices = await BleakScanner.discover(timeout=2)
        device_name: str = ""
        for device in _ble_devices:
            device_name: str = ""
            device_address: str = ""
            for iteration in range(0, len(str(device))):
                if iteration <= 17: 
                    if iteration != 17: device_address += str(device)[iteration]
                else: device_name += str(device)[iteration]

            device_address = device_address.strip()    
            device_name = device_name.strip()
            if device_name == "None" or self.count_char(device_name, "-") > 1: pass
            else: 
                self.ble_devices.append([device_address, device_name])
        self.device_thread.emit()
        
        if len(self.ble_devices) < 1: self.header_status.emit(0)
        else: self.header_status.emit(1)

class RobotWindow(QMainWindow):
    def __init__(self, parent=None, sw=0, sh=0, previous_speed:int=10) -> None:
        super().__init__(parent)
        
        self.setGeometry(int(sw/2-150),int(sh/2-150),300,300)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMaximumSize(QSize(300,300))
        self.setMinimumSize(QSize(300,300))
        self.setWindowTitle("RC - Edit Robot")
        
        self.robot_speed = previous_speed
        self.delete_robot = False
        self.change_name = False
        
        self.central = QFrame()
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setSpacing(20)
        self.setCentralWidget(self.central)
        
        self.setStyleSheet(Theme.get_stylesheet("robot_window.css"))
        
        self.initWindow()
        
        self.central_layout.addWidget(self.window_header, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.addLayout(self.option_form, 1)
        self.central_layout.addWidget(self.robot_change_name_button, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.addWidget(self.robot_delete_button, 10, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
    def initWindow(self) -> None:
        self.window_header = QLabel("Robot Options")
        self.window_header.setObjectName("window_header")
        
        self.option_form = QFormLayout()
        self.option_form.setSpacing(20)
        
        self.robot_type_text = QLabel(text="Robot Type: ")
        self.robot_type_combo = QComboBox()
        self.robot_type_combo.addItem("Root")
        
        self.robot_speed_text = QLabel(text=f"Robot Speed: {self.robot_speed} cm/s")
        self.robot_speed_slider = QSlider(Qt.Orientation.Horizontal, tickPosition=QSlider.TickPosition.TicksBelow, tickInterval=10)
        self.robot_speed_slider.setValue(self.robot_speed*10)
        self.robot_speed_slider.valueChanged.connect(self.change_speed_value_text)
        
        self.option_form.addRow(self.robot_type_text, self.robot_type_combo)
        self.option_form.addRow(self.robot_speed_text, self.robot_speed_slider)
        
        self.robot_change_name_button = RootButton(Theme.light_bg, Theme.gr, text="Change Robot Name")
        self.robot_change_name_button.setFixedSize(170,40)
        self.robot_change_name_button.clicked.connect(self.change_robot_name)
        self.robot_change_name_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.robot_delete_button = RootButton(Theme.light_bg, Theme.org, text="Delete Robot")
        self.robot_delete_button.setFixedSize(170,40)
        self.robot_delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.robot_delete_button.clicked.connect(self.kill_window)
        
    def kill_window(self, event) -> None:
        self.delete_robot = True
        self.close()
        
    def change_robot_name(self, event) -> None:
        self.change_name = True
        self.close()
    
    def change_speed_value_text(self, event) -> None:
        value = int(self.robot_speed_slider.value()/10)+1
        if value % 1 == 0:
            self.robot_speed_text.setText(f"Robot Speed: {value} cm/s")
            self.robot_speed = value
            
    def return_window_attributes(self) -> list[str,int,bool,bool]:
        return [self.robot_type_combo.currentText(),self.robot_speed,self.delete_robot,self.change_name]
        
class StartWindow(QMainWindow):
    def __init__(self, sw:int=0, sh:int=0, parent=None, known_robots:list[list[str]]=[], robots_in_action:list[str]=[]) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("RC - Start Robot")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setGeometry(int(sw/2-200),int(sh/2-300),400,600)
        self.known_robots = known_robots
        self.robots_in_action = robots_in_action
        self.connection_buttons: list = []
        self.button_id: int|None = None
        
        self.central = QWidget()
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setSpacing(20)
        self.setCentralWidget(self.central)
        self.setStyleSheet(Theme.get_stylesheet("start_window.css"))
        
        self.initWindow()
        
        self.central_layout.addWidget(self.devices_header, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.addWidget(self.scroll_area)
        
        if len(known_robots) < 1:
            QMessageBox.information(None, "RC - Info", "There are no robots to choose from! Try adding a robot first!")
            self.close()
        
    def initWindow(self) -> None:
        self.devices_header = QLabel(text="Available Robots")
        self.devices_header.setObjectName("devices_header")
        
        self.container = QWidget()
        self.container.setObjectName("device_scroll_area")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(10)
        
        count: int = 0
        for robot_info in self.known_robots:
            button = ConnectionButton(Icons.play)
            button.changeText(robot_info[0], robot_info[1])
            button.clicked.connect(lambda id=count: self.kill_window(id))
            button.setObjectNames("device_button", "device_name", "device_address")
            try:
                if self.robots_in_action[count] == robot_info[0]:
                    button.setDisabled(True)
            except: pass
            
            self.container_layout.addWidget(button, count-1, Qt.AlignmentFlag.AlignTop)
            self.connection_buttons.append(button)
            count += 1
        self.container_layout.addStretch(50)
        
        self.scroll_area = QScrollArea(self, widgetResizable=True)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setWidget(self.container)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setObjectName("device_scroll_area")
        
    def kill_window(self, button_id:int) -> None:
        self.button_id = button_id
        self.close()