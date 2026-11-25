from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout, QLineEdit,
                               QLabel, QSizePolicy)
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import (Qt, Signal, QSize)

from threading import Thread
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root, Create3

from internal.__init__ import sys, __bin_dir__, __cache_dir__
from internal.theme import Theme, Icons
from internal.filemanager import read_file, save_data_to_csv
from internal.root_widgets import RootButton

class MainWindow(QMainWindow):
    name_changed = Signal()
    
    def __init__(self, sw:int=0, sh:int=0) -> None:
        super().__init__()
        
        self.setGeometry(int(sw/2-150),int(sh/2-150),300,300)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMaximumSize(QSize(300,300))
        self.setMinimumSize(QSize(300,300))
        self.setWindowTitle("RC - Change Name")
        self.name_changed.connect(self.kill_window)
        
        self.central = QFrame()
        self.central_layout = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)
        
        self.robot_info = read_file(__cache_dir__+"start_robot.csv")[0]
        if sys.argv[1] != self.robot_info[0]:
            self.close()
            
        self.initWindow()
        
        self.central_layout.addWidget(self.window_header, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.central_layout.addWidget(self.field)
        
        self.setStyleSheet(Theme.get_stylesheet("change_window.css"))
        
    def initWindow(self) -> None:
        self.window_header = QLabel("Change Name")
        self.window_header.setObjectName("window_header")
        
        self.field = QFrame()
        self.field.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.field.setObjectName("field")
        self.field_layout = QVBoxLayout(self.field)
        self.field_layout.setSpacing(15)
        
        self.name_textbox = QLineEdit(placeholderText="Enter new name here")
        self.name_textbox.setFixedSize(200,40)
        self.name_textbox.textChanged.connect(self.on_text_changed)
        self.name_submit_btn = RootButton(Theme.bg, Theme.org, text="Start Change")
        self.name_submit_btn.setFixedSize(200, 30)
        self.name_submit_btn.setObjectName("name_submit_btn")
        self.name_submit_btn.clicked.connect(self.start_change)
        self.name_submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.name_submit_btn.setDisabled(True)
        self.warning_label = QLabel(text="Warning: DO NOT CLOSE WINDOW!")
        self.warning_label.setObjectName("warning_label")
        
        self.field_layout.addWidget(self.name_textbox,10,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.field_layout.addWidget(self.name_submit_btn,0,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
    
    def on_text_changed(self, event) -> None:
        if len(self.name_textbox.text()) > 0: self.name_submit_btn.setDisabled(False)
        else: self.name_submit_btn.setDisabled(True)
        
    def start_change(self, event) -> None:
        self.field_layout.removeWidget(self.name_textbox)
        self.field_layout.removeWidget(self.name_submit_btn)
        self.name_textbox.hide()
        self.name_submit_btn.hide()
        self.field_layout.addWidget(self.warning_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.window_header.setText("Changing Name.")
        if self.robot_info[2] == "Root": self.robot = Root(Bluetooth(self.robot_info[0], self.robot_info[1]))
        elif self.robot_info[2] == "Create3": self.robot = Create3(Bluetooth(self.robot_info[0], self.robot_info[1]))
        self.robot_info[0] = self.name_textbox.text()
        Thread(target=self.activate_change, daemon=True).start()        
    
    def activate_change(self) -> None:
        @event(self.robot.when_play)
        async def play(robot) -> None:
            self.window_header.setText("Changing Name..")
            await robot.set_name(self.robot_info[0])
            self.window_header.setText("Changing Name...")
            await robot.disconnect()
            self.name_changed.emit()

        self.robot.play()
        
    def kill_window(self) -> None:
        self.close()
        
if __name__ == "__main__":
    name_token = sys.argv[1]
    
    change_window_app = QApplication([])

    screen = QGuiApplication.primaryScreen()
    Icons.initIcons()
    
    main_window = MainWindow(screen.size().width(), screen.size().height())
    main_window.show()
    
    change_window_app.exec()
    
    save_data_to_csv(__cache_dir__+"name.csv", [[main_window.robot_info[0]]])
    
    sys.exit(0)