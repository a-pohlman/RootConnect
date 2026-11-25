from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QLabel, QScrollArea, QSizePolicy, QWidget)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, Signal, QSize

from threading import Thread
from subprocess import run as run_external_script

from internal.__init__ import sys, __bin_dir__, __cache_dir__
from internal.theme import Theme, Icons
from internal.clock import get_computer_time as gct
from internal.clock import sleep
from internal.filemanager import read_file, save_data_to_csv
from internal.root_widgets import RootFrame, RobotFrame, RootButton
from internal.root_toplevel import RobotWindow, StartWindow, AddWindow
        
class NavFrame(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__()
        
        self.parent = parent
        
        self.nav_layout = QHBoxLayout(self)
        self.nav_layout.setSpacing(10)
        self.setFixedHeight(100)
        self.setObjectName("nav")
        
        self.initNavFrame()
        
        self.nav_layout.addWidget(self.add_btn, 0, Qt.AlignmentFlag.AlignLeft)
        self.nav_layout.addWidget(self.start_btn, 1, Qt.AlignmentFlag.AlignLeft)
        self.nav_layout.addWidget(self.help_btn, 1, Qt.AlignmentFlag.AlignRight)
        self.nav_layout.addWidget(self.settings_btn, 0, Qt.AlignmentFlag.AlignRight)
    
    def initNavFrame(self) -> None:
        self.add_btn = RootButton(Theme.bg, Theme.gr, text="Add Robot")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setFixedSize(160,60)
        self.add_btn.setIcon(Icons.add)
        self.add_btn.setIconSize(QSize(40,40))
        self.add_btn.setObjectName("nav_add_button")
        
        self.start_btn = RootButton(Theme.bg, Theme.org, text="Run Robot")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setFixedSize(160,60)
        self.start_btn.setIcon(Icons.play)
        self.start_btn.setIconSize(QSize(40,40))
        self.start_btn.setObjectName("nav_start_button")
        
        self.help_btn = RootButton(Theme.bg, Theme.gr, text="")
        self.help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.help_btn.setFixedSize(60,60)
        self.help_btn.setIcon(Icons.help)
        self.help_btn.setIconSize(QSize(40,40))
        self.help_btn.setObjectName("nav_help_button")
        self.help_btn.setDisabled(True)
        self.help_btn.setToolTip("Help window is currently not a feature! Please go to the Github Repository for help and information!")
        
        self.settings_btn = RootButton(Theme.bg, Theme.gr, text="")
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setFixedSize(60,60)
        self.settings_btn.setIcon(Icons.settings)
        self.settings_btn.setIconSize(QSize(40,40))
        self.settings_btn.setObjectName("nav_settings_button")
        self.settings_btn.setDisabled(True)
        self.settings_btn.setToolTip("Settings window is currently not a feature!")
     
class MainFrame(QFrame):
    time_signal = Signal(str)
    
    def __init__(self, sw:int, sh:int, parent=None) -> None:
        super().__init__()

        self.parent_window = parent
        self.sw = sw
        self.sh = sh
        self.time_signal.connect(self.update_time)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40,30,40,0)
        self.main_layout.setSpacing(40)
        self.setObjectName("main")
        
        self.robot_frames: list[RobotFrame] = []
        self.frame_id: int = 0
        self.robot_name_address: list[list[str,str]] = []
        self.robot_attributes: list[list[str,str,str,bool]] = []
        self.robots_in_action: dict = {}
        self.row: int = 0
        self.column: int = 0
        
        self.initMainFrame()
        
        self.main_layout.addWidget(self.msg_frame, 0, Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.scroll_area)
        
        Thread(target=self.start_clock, daemon=True).start()
    
    def initMainFrame(self) -> None:
        self.msg_frame = RootFrame()
        self.msg_frame.setObjectName("main_message_frame")
        self.msg_frame_layout = QHBoxLayout(self.msg_frame)
        self.msg_frame_layout.setContentsMargins(20,20,20,20)
        self.msg_frame_layout.setSpacing(10)
        
        self.msg_image_con = QLabel(pixmap=Icons.connectivity)
        self.msg_label_con = QLabel(text="Robots Connected: 0")
        self.msg_image_time = QLabel(pixmap=Icons.clock)
        self.msg_label_time = QLabel(text="12:00 PM")
        
        self.msg_frame_layout.addWidget(self.msg_image_con, 0, Qt.AlignmentFlag.AlignLeft)
        self.msg_frame_layout.addWidget(self.msg_label_con, 1, Qt.AlignmentFlag.AlignLeft)
        self.msg_frame_layout.addWidget(self.msg_image_time, 1, Qt.AlignmentFlag.AlignRight)
        self.msg_frame_layout.addWidget(self.msg_label_time, 0, Qt.AlignmentFlag.AlignRight)

        self.scroll_container = QWidget()
        self.scroll_container.setObjectName("main_scroll_container")
        self.scroll_container_layout = QGridLayout(self.scroll_container)
        self.scroll_container_layout.setContentsMargins(10,10,10,10)
        self.scroll_container_layout.setSpacing(15)
        
        self.scroll_area = QScrollArea(parent=self, widgetResizable=True)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setWidget(self.scroll_container)
        self.scroll_area.setObjectName("main_scroll_area")
        
        try:
            robots = read_file(__cache_dir__+"saved_robots.csv")
            for info in robots:
                self.add_robot_to_grid([info[0],info[1]],[info[2],int(info[3]),int(info[4]),False])   
        except: pass
           
    def add_robot_to_grid(self, name_of_robot: list[str|str], settings:list=["Root",10,0,False]) -> None:
        if name_of_robot not in self.robot_name_address:
            robot_frame = RobotFrame()
            robot_frame.changeRobotName(name_of_robot[0])
            robot_frame.changeBatteryPercent(settings[2])
            robot_frame.header_menu_button.clicked.connect(lambda *args, frame_id=self.frame_id: self.open_robot_window(frame_id))
            self.robot_attributes.append(settings)
            self.robot_name_address.append([name_of_robot[0],name_of_robot[1]])
            self.robot_frames.append(robot_frame)
            self.scroll_container_layout.addWidget(robot_frame,self.row,self.column,Qt.AlignmentFlag.AlignTop)
            self.scroll_container_layout.setRowStretch(self.scroll_container_layout.rowCount(), 1)
            
            if self.column > 0:
                self.row += 1
                self.column = 0
            else:
                self.column += 1
                
            self.frame_id += 1
            
        self.update_saved_robots()
    
    def destroy_robot_from_grid(self, frame_id:int=0) -> None:
        robot_name_address: list = []
        robot_attributes: list = []
        
        for frame in self.robot_frames:
            self.scroll_container_layout.removeWidget(frame)
            frame.deleteLater()
        garbage = self.robot_name_address.pop(frame_id)
        garbage = self.robot_attributes.pop(frame_id)
        
        self.frame_id = 0
        self.row = 0
        self.column = 0
        
        for name_address in self.robot_name_address:
            robot_name_address.append(name_address)
            
        for attributes in self.robot_attributes:
            robot_attributes.append(attributes)
        
        self.robot_frames.clear()
        self.robot_name_address.clear()
        self.robot_attributes.clear()
        
        for index in range(len(robot_name_address)):
            self.add_robot_to_grid(robot_name_address[index], robot_attributes[index])
        
        self.update_saved_robots()
            
    def open_robot_window(self, frame_id:int=0) -> None:
        self.robot_window = RobotWindow(self.parent_window, self.sw, self.sh, self.robot_attributes[frame_id][1])
        self.robot_window.destroyed.connect(lambda *args: self.robot_window_destroyed(frame_id))
        self.robot_window.show()

    def robot_window_destroyed(self, frame_id:int=0) -> None:
        window_attributes = self.robot_window.return_window_attributes()
        self.robot_attributes[frame_id] = [window_attributes[0],window_attributes[1],self.robot_attributes[frame_id][2],window_attributes[2]]
        if self.robot_attributes[frame_id][3] == True:
            self.destroy_robot_from_grid(frame_id)
        if window_attributes[3] == True:
            self.create_temp_data(frame_id)
            while True:
                """Use below code for Windows 11 Version"""
                if run_external_script(args=f"root_change_name.exe {self.robot_name_address[frame_id][0]}", cwd=__bin_dir__, shell=True).returncode != 5:
                    break
                
    
                """Use below code for Python Version
                if run_external_script(args=sys.executable+f" root_change_name.pyw {self.robot_name_address[frame_id][0]}", cwd=__bin_dir__).returncode != 5:
                    break
                """    
            self.robot_name_address[frame_id][0] = read_file(__cache_dir__+"name.csv")[0][0]
            self.robot_frames[frame_id].changeRobotName(self.robot_name_address[frame_id][0])
    
    def update_saved_robots(self) -> None:
        saved_robots: list[list[str]] = []
        for index in range(len(self.robot_name_address)):
            saved_robots.append([self.robot_name_address[index][0],self.robot_name_address[index][1],self.robot_attributes[index][0],self.robot_attributes[index][1],self.robot_attributes[index][2]])
        save_data_to_csv(dir=__cache_dir__+"saved_robots.csv", robot_data=saved_robots)        
        
    def create_temp_data(self, index:int) -> None:
        save_data_to_csv(dir=__cache_dir__+"start_robot.csv", robot_data=[[self.robot_name_address[index][0],self.robot_name_address[index][1],self.robot_attributes[index][0],self.robot_attributes[index][1],self.robot_attributes[index][2]]])
        
    def start_clock(self) -> None:
        while True:
            self.time_signal.emit(gct())
            sleep(1)
    
    def update_time(self, msg:str) -> None:
        self.msg_label_time.setText(msg)
        
class MainWindow(QMainWindow):
    def __init__(self, sw, sh) -> None:
        super().__init__()
        
        self.sw = sw
        self.sh = sh
        
        self.setWindowTitle("RootConnect")
        self.setGeometry(int(sw/2 - 400),int(sh/2 - 300),800,600)
        
        self.initUI()
        self.setStyleSheet(Theme.get_stylesheet("home.css"))
        
    def initUI(self) -> None:
        self.central = QFrame()
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.central)
        
        self.nav = NavFrame(self)
        self.main = MainFrame(self.sw, self.sh, self)
        
        self.central_layout.addWidget(self.nav)
        self.central_layout.addWidget(self.main)
        
        self.nav.add_btn.clicked.connect(self.open_add_window)
        self.nav.start_btn.clicked.connect(self.open_start_window)
    
    def open_add_window(self) -> None:
        self.add_window = AddWindow(self.sw, self.sh, self, "RC - Add Robot")
        self.add_window.destroyed.connect(self.add_window_destroyed)
        self.nav.add_btn.setDisabled(True)
        self.add_window.show()
        
    def open_start_window(self) -> None:
        self.start_window = StartWindow(self.sw, self.sh, self, self.main.robot_name_address, self.main.robots_in_action)
        self.start_window.destroyed.connect(self.start_window_destroyed)
        self.nav.start_btn.setDisabled(True)
        self.start_window.show()
        
    def add_window_destroyed(self, event) -> None:
        self.nav.add_btn.setDisabled(False)
        if self.add_window.selected_button is not None:
            self.main.add_robot_to_grid(self.add_window.selected_button)
        self.add_window.ble_devices.clear()
        self.add_window.connection_buttons.clear()
        
    def start_window_destroyed(self) -> None:
        self.nav.start_btn.setDisabled(False)
        if self.start_window.button_id != None:
            Thread(target=self.start_connection, args=([self.start_window.button_id]), daemon=True).start()
            
    def start_connection(self, robot_id:int) -> None:
        self.main.robots_in_action[robot_id] = self.main.robot_name_address[robot_id][0]
        self.main.create_temp_data(robot_id)
        self.main.msg_label_con.setText(f"Robots Connected: {len(self.main.robots_in_action)}")
        while True:
            """Use below code for Windows 11 Version"""
            if run_external_script(args=f"root_controller.exe {self.main.robot_name_address[robot_id][0]}", cwd=__bin_dir__, shell=True).returncode != 5:
                break
            

            """Use below code for Python Version
            if run_external_script(args=sys.executable+f" root_controller.pyw {self.main.robot_name_address[robot_id][0]}", cwd=__bin_dir__).returncode != 5:
                break
            """
        self.main.robots_in_action.pop(robot_id)
        _battery_level: int = int(read_file(__cache_dir__+"battery.csv")[0][0])
        self.main.robot_frames[robot_id].changeBatteryPercent(_battery_level)
        self.main.robot_attributes[robot_id][2] = _battery_level
        self.main.msg_label_con.setText(f"Robots Connected: {len(self.main.robots_in_action)}")
        
if __name__ == "__main__":
    root_connect = QApplication([])
    
    screen = QGuiApplication.primaryScreen()
    Icons.initIcons()
    
    main_window = MainWindow(screen.size().width(), screen.size().height())
    main_window.show()
    
    root_connect.exec()
    main_window.main.update_saved_robots()
    sys.exit(0)