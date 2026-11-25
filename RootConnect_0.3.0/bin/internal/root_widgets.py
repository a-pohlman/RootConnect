from PySide6.QtWidgets import (QFrame, QPushButton, QVBoxLayout, QHBoxLayout, 
                               QLabel, QGraphicsColorizeEffect, QGraphicsDropShadowEffect)
from PySide6.QtGui import QColor, QCursor, QPixmap
from PySide6.QtCore import Qt, Signal, QSize, QPropertyAnimation, QVariantAnimation, QEasingCurve

from internal.theme import Theme, Icons

class RootButton(QPushButton):
    def __init__(self, background_color: QColor, hover_color: QColor, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.background_color: QColor = background_color
        self.hover_color: QColor = hover_color
        
        self.initButton()

    def initButton(self) -> None:
        self.color_effect = QGraphicsColorizeEffect(self)
        self.color_effect.setColor(self.background_color)
        self.setGraphicsEffect(self.color_effect)
        self.hover_animation = QPropertyAnimation(self.color_effect, b'color')
        self.hover_animation.setDuration(250)
        self.hover_animation.setEasingCurve(QEasingCurve.InSine)
        self.hover_animation.setStartValue(self.background_color)
        self.hover_animation.setEndValue(self.hover_color)
        
    def enterEvent(self, event) -> None:
        if self.hover_animation.State.Stopped:
            self.hover_animation.setDirection(self.hover_animation.Direction.Forward)
            self.hover_animation.start()
        
        QPushButton.enterEvent(self, event)
        
    def leaveEvent(self, event) -> None:
        if self.hover_animation.State.Stopped:
            self.hover_animation.setDirection(self.hover_animation.Direction.Backward)
            self.hover_animation.start()
        
        QPushButton.leaveEvent(self, event)

class RootFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.body_shadow = QGraphicsDropShadowEffect(self, xOffset=0, yOffset=0, blurRadius=10, color=Theme.dark_shadow)
        self.setGraphicsEffect(self.body_shadow)
        
        self.blur_animation = QVariantAnimation(self)
        self.blur_animation.setStartValue(10)
        self.blur_animation.setEndValue(30)
        self.blur_animation.setDuration(100)
        self.blur_animation.setEasingCurve(QEasingCurve.InSine)
        self.blur_animation.valueChanged.connect(self.updateBlurRadius)
        
    def enterEvent(self, event) -> None:
        if self.blur_animation.State.Stopped:
            self.blur_animation.setDirection(self.blur_animation.Direction.Forward)
            self.blur_animation.start()
            
    def leaveEvent(self, event) -> None:
        if self.blur_animation.State.Stopped:
            self.blur_animation.setDirection(self.blur_animation.Direction.Backward)
            self.blur_animation.start()
        
    def updateBlurRadius(self, value) -> None:
        self.body_shadow.setBlurRadius(value)

class RobotFrame(RootFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.setObjectName("robot_frame")
        self.setFixedHeight(230)
        self.robot_frame_layout = QVBoxLayout(self)
        self.robot_frame_layout.setSpacing(20)
        self.robot_frame_layout.setContentsMargins(30,10,30,10)
        
        self.initFrame()
        
        self.robot_frame_layout.addLayout(self.header_layout)
        self.robot_frame_layout.addWidget(self.robot_image, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.robot_frame_layout.addWidget(self.robot_name, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
    def initFrame(self) -> None:
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(10)
        
        self.header_label_batt = QLabel(text="0%")
        self.header_image_batt = QLabel(pixmap=Icons.battery)
        self.header_menu_button = RootButton(Theme.light_bg, Theme.gr, text="")
        self.header_menu_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.header_menu_button.setFixedSize(50,30)
        self.header_menu_button.setObjectName("robot_frame_header_menu_button")
        self.header_menu_button.setIcon(Icons.menu)
        self.header_menu_button.setIconSize(QSize(40,40))
        
        self.header_layout.addWidget(self.header_image_batt, 0, Qt.AlignmentFlag.AlignLeft)
        self.header_layout.addWidget(self.header_label_batt, 1, Qt.AlignmentFlag.AlignLeft)
        self.header_layout.addWidget(self.header_menu_button, 0, Qt.AlignmentFlag.AlignRight)
        
        self.robot_image = QLabel(pixmap=Icons.robot.scaled(QSize(160,160), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.robot_name = QLabel(text="Robot has no name")
        self.robot_name.setStyleSheet("font-weight: bold;")
        
    def changeRobotName(self, name: str) -> None:
        self.robot_name.setText(name)
        
    def changeBatteryPercent(self, percent: int) -> None:
        self.header_label_batt.setText(f"{percent}%")
        
class ConnectionButton(QFrame):
    clicked = Signal()
    
    def __init__(self, icon:QPixmap) -> None:
        super().__init__()
        
        self.color_effect = QGraphicsColorizeEffect(self)
        self.color_effect.setColor(Theme.bg)
        self.setGraphicsEffect(self.color_effect)
        self.hover_animation = QPropertyAnimation(self.color_effect, b'color')
        self.hover_animation.setDuration(250)
        self.hover_animation.setEasingCurve(QEasingCurve.InSine)
        self.hover_animation.setStartValue(Theme.bg)
        self.hover_animation.setEndValue(Theme.gr)
        self.icon = icon
        
        self.connection_button_layout = QHBoxLayout(self)
        self.connection_button_layout.setSpacing(20)
        
        self.initConnectionButton()
        
        self.connection_button_layout.addWidget(self.device_image, 0, Qt.AlignmentFlag.AlignLeft)
        self.connection_button_layout.addLayout(self.vlabel_layout, 1)
        
    def initConnectionButton(self) -> None:
        self.device_image = QLabel(pixmap=self.icon)
        
        self.vlabel_layout = QVBoxLayout()
        self.vlabel_layout.setSpacing(15)
        
        self.device_name = QLabel(text="BLE Device Name")
        self.device_address = QLabel(text="BLE Device Address")
        
        self.vlabel_layout.addWidget(self.device_name)
        self.vlabel_layout.addWidget(self.device_address)
    
    # Click functionality found on stack forum exchange adapted to PySide6 / PyQt6      
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.pressPos = event.position()

    def mouseReleaseEvent(self, event) -> None:
        if (self.pressPos is not None and event.button() == Qt.LeftButton and self.rect().contains(event.position().toPoint())):
            self.clicked.emit()
        self.pressPos = None
        
    def enterEvent(self, event) -> None:
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if self.hover_animation.State.Stopped:
            self.hover_animation.setDirection(self.hover_animation.Direction.Forward)
            self.hover_animation.start()
        
        QFrame.enterEvent(self,event)
        
    def leaveEvent(self, event) -> None:
        if self.hover_animation.State.Stopped:
            self.hover_animation.setDirection(self.hover_animation.Direction.Backward)
            self.hover_animation.start()
            
        QFrame.leaveEvent(self,event)
        
    def changeText(self, new_name: str, new_address: str) -> None:
        self.device_name.setText(new_name)
        self.device_address.setText(new_address)
        
    def returnButtonText(self) -> str:
        return [self.device_name.text(),self.device_address.text()]
    
    def setObjectNames(self, button_name:str, device_name:str, device_address:str) -> None:
        self.setObjectName(button_name)
        self.device_name.setObjectName(device_name)
        self.device_address.setObjectName(device_address)