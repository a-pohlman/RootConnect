from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSizePolicy, QWidget, QStackedWidget, QSpacerItem)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QSize

from threading import Thread
from asyncio import run as run_asyncio
from bleak import BleakClient
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root, Create3

from internal.__init__ import sys, __bin_dir__, __cache_dir__
from internal.theme import Theme, Icons
from internal.filemanager import read_file, save_data_to_csv
from internal.root_widgets import RootFrame, RootButton
from internal.root_toplevel import AddWindow

class TouchControlsFrame(RootFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.initFrame()
        
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.addLayout(self.motion_layout)
        self.frame_layout.addSpacerItem(QSpacerItem(60,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed))
        self.frame_layout.addLayout(self.function_layout)
        
    def initFrame(self) -> None:
        self.motion_layout = QVBoxLayout()
        
        self.touch_up = RootButton(Theme.bg, Theme.gr, text="")
        self.touch_up.setIcon(Icons.up)
        self.touch_up.setObjectName("touch_up")
        self.touch_left = RootButton(Theme.bg, Theme.gr, text="")
        self.touch_left.setIcon(Icons.left)
        self.touch_left.setObjectName("touch_left")
        self.touch_right = RootButton(Theme.bg, Theme.gr, text="")
        self.touch_right.setIcon(Icons.right)
        self.touch_right.setObjectName("touch_right")
        self.touch_down = RootButton(Theme.bg, Theme.gr, text="")
        self.touch_down.setIcon(Icons.down)
        self.touch_down.setObjectName("touch_down")
        self.horizontal_lr_layout = QHBoxLayout()
        self.horizontal_lr_layout.addWidget(self.touch_left)
        self.horizontal_lr_layout.addWidget(self.touch_down)
        self.horizontal_lr_layout.addWidget(self.touch_right)
        self.motion_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding))
        self.motion_layout.addWidget(self.touch_up, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.motion_layout.addLayout(self.horizontal_lr_layout)
        self.motion_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding))
        
        self.function_layout = QVBoxLayout()
        self.touch_a = RootButton(Theme.bg, Theme.org, text="")
        self.touch_a.setIcon(Icons.a)
        self.touch_a.setObjectName("touch_a")
        self.touch_b = RootButton(Theme.bg, Theme.org, text="")
        self.touch_b.setIcon(Icons.b)
        self.touch_b.setObjectName("touch_b")
        self.touch_x = RootButton(Theme.bg, Theme.org, text="")
        self.touch_x.setIcon(Icons.x)
        self.touch_x.setObjectName("touch_x")
        self.touch_y = RootButton(Theme.bg, Theme.org, text="")
        self.touch_y.setIcon(Icons.y)
        self.touch_y.setObjectName("touch_y")
        self.horizontal_bx_layout = QHBoxLayout()
        self.horizontal_bx_layout.addWidget(self.touch_b)
        self.horizontal_bx_spacer: QSpacerItem = QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        self.horizontal_bx_layout.addSpacerItem(self.horizontal_bx_spacer)
        self.horizontal_bx_layout.addWidget(self.touch_x)
        self.function_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding))
        self.function_layout.addWidget(self.touch_a, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.function_layout.addLayout(self.horizontal_bx_layout)
        self.function_layout.addWidget(self.touch_y, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.function_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding))
        
        self.resize_buttons()
        
    def resize_buttons(self, size: tuple[int,int] = (120,120)) -> None:
        self.touch_up.setFixedSize(size[0],size[1])
        self.touch_down.setFixedSize(size[0],size[1])
        self.touch_left.setFixedSize(size[0],size[1])
        self.touch_right.setFixedSize(size[0],size[1])
        self.touch_a.setFixedSize(size[0],size[1])
        self.touch_b.setFixedSize(size[0],size[1])
        self.touch_x.setFixedSize(size[0],size[1])
        self.touch_y.setFixedSize(size[0],size[1])
        
        self.horizontal_bx_spacer.changeSize(size[0],size[1])
        
        self.touch_up.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_down.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_left.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_right.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_a.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_b.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_x.setIconSize(QSize(size[0]*0.6,size[1]*0.6))
        self.touch_y.setIconSize(QSize(size[0]*0.6,size[1]*0.6))

class MainWindow(QMainWindow):
    def __init__(self, sw:int, sh:int) -> None:
        super().__init__()
        
        self.robot_info: list[str] = read_file(__cache_dir__+"start_robot.csv")[0]
        self.robot_info[3] = int(self.robot_info[3])
        self.sw = sw
        self.sh = sh
        self.virtual_button: int = 0
        self.read_ble_on: bool = True
        self.read_touch_on: bool = True
        self.controller_bindings: list[str] = ["Marker Up/Down", "Eraser Up/Down", "Honk", "Quick Turn"]
        self.honk_pitch: int = 500
        self.marker: str = "DOWN"
        self.eraser: str = "DOWN"
        self.controller_address: str|None = None
        self.controller_name: str|None = None
        
        if sys.argv[1] != self.robot_info[0]:
            self.close()
        
        self.setWindowTitle(f"RC: {self.robot_info[0]} (Connecting)")
        self.setGeometry(int(sw/2 - 400),int(sh/2 - 300),800,600)
        self.initWindow()
        
        self.center = QWidget()
        self.center_layout = QVBoxLayout(self.center)
        self.center_layout.addWidget(self.nav_frame)
        self.center_layout.addLayout(self.switch_layout)
        self.center_layout.addWidget(self.stacked_frame)
        
        self.setStyleSheet(Theme.get_stylesheet("controller_window.css"))        
        self.setCentralWidget(self.center)
        
    def initWindow(self) -> None:
        self.nav_frame = QFrame()
        self.nav_frame.setObjectName("nav_frame")
        self.nav_frame_layout = QHBoxLayout(self.nav_frame)
        self.battery_icon = QLabel(pixmap=Icons.battery)
        self.battery_icon.setToolTip("To refresh the battery level, touch one of the top four corners of the robot!")
        self.battery_label = QLabel(text=f"{self.robot_info[4]}%")
        self.battery_label.setObjectName("battery_label")
        self.battery_label.setToolTip("To refresh the battery level, touch one of the top four corners of the robot!")
        self.robot_name = QLabel(text=self.robot_info[0])
        self.robot_name.setObjectName("robot_name")
        self.exit_btn = RootButton(Theme.light_bg, Theme.org)
        self.exit_btn.setIcon(Icons.exit)
        self.exit_btn.setIconSize(QSize(70,30))
        self.exit_btn.setFixedSize(70,40)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn.setStyleSheet("border: none; border-radius: 15px;")
        self.exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nav_frame_layout.addWidget(self.battery_icon,0,Qt.AlignmentFlag.AlignLeft)
        self.nav_frame_layout.addWidget(self.battery_label,1,Qt.AlignmentFlag.AlignLeft)
        self.nav_frame_layout.addWidget(self.robot_name,20,Qt.AlignmentFlag.AlignHCenter)
        self.nav_frame_layout.addWidget(self.exit_btn,0,Qt.AlignmentFlag.AlignRight)
        
        self.switch_layout = QHBoxLayout()
        self.touch_controls_button = RootButton(Theme.light_bg, Theme.gr, text="Touch Controls")
        self.touch_controls_button.setObjectName("touch_controls_button")
        self.touch_controls_button.setFixedSize(180,40)
        self.touch_controls_button.clicked.connect(lambda *args: self.switch_controls(0))
        self.touch_controls_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.external_controls_button = RootButton(Theme.light_bg, Theme.gr, text="Root Controller")
        self.external_controls_button.setObjectName("external_controls_button")
        self.external_controls_button.setFixedSize(180,40)
        self.external_controls_button.clicked.connect(lambda *args: self.switch_controls(1))
        self.external_controls_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_layout.addSpacerItem(QSpacerItem(20,1,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed))
        self.switch_layout.addWidget(self.touch_controls_button)
        self.switch_layout.addWidget(self.external_controls_button)
        self.switch_layout.addSpacerItem(QSpacerItem(20,1,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed))
        
        self.stacked_frame = QStackedWidget()

        self.touch_controls_frame = TouchControlsFrame()
        self.touch_controls_frame.setObjectName("touch_controls_frame")
        
        self.controller_frame = RootFrame()
        self.controller_frame.setObjectName("controller_frame")
        self.controller_frame_layout = QVBoxLayout(self.controller_frame)
        self.controller_frame_layout.setSpacing(30)
        self.controller_message = QLabel("No Active Controller!")
        self.controller_message.setObjectName("controller_message")
        self.controller_connect_btn = RootButton(Theme.bg, Theme.org, text="Connect Controller")
        self.controller_connect_btn.setObjectName("controller_connect_btn")
        self.controller_connect_btn.setFixedSize(250,50)
        self.controller_connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.controller_connect_btn.clicked.connect(self.open_add_window)
        self.controller_frame_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding))
        self.controller_frame_layout.addWidget(self.controller_message, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.controller_frame_layout.addWidget(self.controller_connect_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.controller_frame_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding))
        
        self.stacked_frame.addWidget(self.touch_controls_frame)
        self.stacked_frame.addWidget(self.controller_frame)
        
        self.start_robot()
        self.switch_controls(0)
        
    def resizeEvent(self, event) -> None:
        if event.size().width() > 1260:
            self.touch_controls_frame.resize_buttons((160,160))
        
        if event.size().width() <= 1260:
            self.touch_controls_frame.resize_buttons((120,120))
            
        if event.size().width() <= 1020:
            self.touch_controls_frame.resize_buttons((90,90))
        
        QMainWindow.resizeEvent(self,event)
        
    def open_add_window(self, event) -> None:
        self.add_window = AddWindow(self.sw, self.sh, self, "RC - Add Controller")
        self.add_window.destroyed.connect(self.add_window_destroyed)
        self.controller_connect_btn.setDisabled(True)
        self.add_window.show()
        
    def add_window_destroyed(self, event) -> None:
        self.controller_connect_btn.setDisabled(False)
        if self.add_window.selected_button is not None:
            self.controller_name = self.add_window.selected_button[0]
            self.controller_address = self.add_window.selected_button[1]
            self.controller_message.setText(f"{self.controller_name} (Connecting)")
            Thread(target=self.start_ble_controller, daemon=True).start()
        self.add_window.ble_devices.clear()
        self.add_window.connection_buttons.clear()
    
    def switch_controls(self, frame_id:int) -> None:
        match frame_id:
            case 0: 
                self.read_ble_on = False
                self.read_touch_on = True
                Thread(target=self.read_touch_controls, daemon=True).start()
                self.stacked_frame.setCurrentIndex(0)
                self.touch_controls_button.color_effect.setColor(Theme.gr)
                self.touch_controls_button.hover_animation.setStartValue(Theme.gr)
                self.touch_controls_button.setDisabled(True)
                self.external_controls_button.color_effect.setColor(Theme.light_bg)
                self.external_controls_button.hover_animation.setStartValue(Theme.light_bg)
                self.external_controls_button.setDisabled(False)
            case 1: 
                self.read_touch_on = False
                self.read_ble_on = True
                self.stacked_frame.setCurrentIndex(1)
                self.touch_controls_button.color_effect.setColor(Theme.light_bg)
                self.touch_controls_button.hover_animation.setStartValue(Theme.light_bg)
                self.touch_controls_button.setDisabled(False)
                self.external_controls_button.color_effect.setColor(Theme.gr)
                self.external_controls_button.hover_animation.setStartValue(Theme.gr)
                self.external_controls_button.setDisabled(True)
        
    def start_ble_controller(self) -> None:
        run_asyncio(self.read_ble_controller())
        
    def read_touch_controls(self) -> None:
        try:
            while self.read_touch_on:
                if self.touch_controls_frame.touch_up.isDown() == True: self.virtual_button = 1
                elif self.touch_controls_frame.touch_left.isDown() == True: self.virtual_button = 2
                elif self.touch_controls_frame.touch_right.isDown() == True: self.virtual_button = 3
                elif self.touch_controls_frame.touch_down.isDown() == True: self.virtual_button = 4
                elif self.touch_controls_frame.touch_a.isDown() == True: self.virtual_button = 5
                elif self.touch_controls_frame.touch_b.isDown() == True: self.virtual_button = 6
                elif self.touch_controls_frame.touch_x.isDown() == True: self.virtual_button = 7
                elif self.touch_controls_frame.touch_y.isDown() == True: self.virtual_button = 8
                else: self.virtual_button = 0
        except: pass
            
    async def read_ble_controller(self) -> None:
        try: 
            ble_device = BleakClient(self.controller_address)
            await ble_device.connect()
            self.controller_message.setText(f"{self.controller_name} (Active)")
            while self.read_ble_on:
                raw_controller_value = await ble_device.read_gatt_char("C0397A41-A619-445A-8AE4-B4E7B1E98A62")
                self.virtual_button = int(raw_controller_value.hex(), 16)
            await ble_device.disconnect()
            self.controller_message.setText("No Active Controller!")
        except: pass
        
    def start_robot(self) -> None:
        if self.robot_info[2] == "Root": self.robot = Root(Bluetooth(self.robot_info[0], self.robot_info[1]))
        elif self.robot_info[2] == "Create3": self.robot = Create3(Bluetooth(self.robot_info[0], self.robot_info[1]))
            
        Thread(target=self.activate_robot, daemon=True).start()
    
    def activate_robot(self) -> None:
        async def quick_turn(robot) -> None:
            await robot.turn_right(180)

        async def switch_marker_position(robot, position:str) -> None:
            match position:
                case "UP": await robot.set_marker_up()
                case "DOWN": await robot.set_marker_down()

        async def switch_eraser_position(robot, position:str) -> None:
            match position:
                case "UP": await robot.set_eraser_up()
                case "DOWN": await robot.set_eraser_down()

        async def honk(robot) -> None:
            await self.robot.play_tone(self.honk_pitch, 1)

        async def use_binding(binding:str, robot:Root|Create3) -> None:
            match binding:
                case "Marker Up/Down":
                    await switch_marker_position(robot, self.marker)
                    if self.marker == "UP": self.marker = "DOWN"
                    else: self.marker = "UP"
                case "Eraser Up/Down":
                    await switch_eraser_position(robot, self.eraser)
                    if self.eraser == "UP": self.eraser = "DOWN"
                    else: self.eraser = "UP"
                case "Honk": await honk(robot)
                case "Quick Turn": await quick_turn(robot)

        @event(self.robot.when_touched, [True, True, True, True])
        async def touched(robot) -> None:
            _battery: tuple = await robot.get_battery_level()
            self.robot_info[4] = _battery[1]
            self.battery_label.setText(f"{self.robot_info[4]}%")

        @event(self.robot.when_cliff_sensor, [True])
        async def cliff(robot) -> None:
            await robot.set_lights_spin_rgb(255,139,0)

        @event(self.robot.when_cliff_sensor, [False])
        async def cliff(robot) -> None:
            await robot.set_lights_on_rgb(97,167,7)

        @event(self.robot.when_play)
        async def play(robot) -> None:
            await robot.set_lights_on_rgb(97,167,7)
            _battery: tuple = await robot.get_battery_level()
            self.robot_info[4] = _battery[1]
            self.battery_label.setText(f"{self.robot_info[4]}%")
            self.setWindowTitle(f"RC: {self.robot_info[0]} (Active)")
            while True:
                if self.virtual_button == 0:
                    await robot.set_wheel_speeds(0,0)
                if self.virtual_button == 1:
                    await robot.set_wheel_speeds(self.robot_info[3],self.robot_info[3])
                if self.virtual_button == 2:
                    await robot.set_wheel_speeds(-self.robot_info[3],self.robot_info[3])
                if self.virtual_button == 3:
                    await robot.set_wheel_speeds(self.robot_info[3],-self.robot_info[3])
                if self.virtual_button == 4:
                    await robot.set_wheel_speeds(-self.robot_info[3],-self.robot_info[3])
                if self.virtual_button == 5:
                    await use_binding(self.controller_bindings[0], robot)
                if self.virtual_button == 6:
                    await use_binding(self.controller_bindings[1], robot)
                if self.virtual_button == 7:
                    await use_binding(self.controller_bindings[2], robot)
                if self.virtual_button == 8:
                    await use_binding(self.controller_bindings[3], robot)

        self.robot.play()

if __name__ == "__main__":
    name_token = sys.argv[1]
    
    controller_app = QApplication([])

    screen = QGuiApplication.primaryScreen()
    Icons.initIcons()
    
    main_window = MainWindow(screen.size().width(), screen.size().height())
    main_window.show()
    
    controller_app.exec()
    
    main_window.read_ble_on = False
    main_window.read_touch_on = False
    save_data_to_csv(__cache_dir__+"battery.csv", [[main_window.robot_info[4]]])
    
    sys.exit(0)