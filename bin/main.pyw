#import built-in modules
from sys import exit
from time import sleep
from threading import Thread
from tkinter import messagebox # tkinter is not built into Linux Distributions
from asyncio import run as run_asyncio

#import external modules
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSegmentedButton, CTkProgressBar, StringVar
from bleak import BleakClient
from serial import Serial
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root, Create3
from time import sleep

#import internal modules
from tooling.filemanager import load_info, save_info
from tooling.theme import Theme, Icons
from tooling.windows import ConnectControllerWindow, SettingsWindow, RobotWindow, ChangeNameWindow, AppInfoWindow
from tooling.__init__ import __enable_pillow__, __version__

class Base(CTk, Theme, Icons):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(f"1200x800+{int(self.winfo_screenwidth()/2 - 550)}+{int(self.winfo_screenheight()/2.2 - 400)}")
        self.title("Root Connect")
        
        self.deiconify()

        self.parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self.parent_frame.pack(expand=True, fill="both")
        
        if __enable_pillow__ == False:
            self.create_photo_images()

class TempFrame(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_temp_frame(self) -> None:
        self.temp_logo_label = CTkLabel(self.parent_frame, text="", image=self.root_logo_image)
        self.temp_version_label = CTkLabel(self.parent_frame, text=f"Version: {__version__}", text_color="#CDCDCD", font=("Arial",15,"normal"))
        
    def place_startup_frame(self) -> None:
        self.temp_logo_label.pack(expand=True)
        self.temp_version_label.pack(expand=True)

    def forget_startup_frame(self) -> None:
        self.temp_logo_label.pack_forget()
        self.temp_version_label.pack_forget()

class ActionFrame(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_action_frame(self) -> None:
        self.action_frame_out = CTkFrame(self.parent_frame, fg_color=self.color["green"], corner_radius=0)
        self.action_frame_in = CTkFrame(self.action_frame_out, corner_radius=0, width=120, fg_color=self.color["bg_light"])
        self.robot_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.robot_image, fg_color=self.color["bg_light"], hover_color=self.color["green"], text="")
        self.controller_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.controller_image, fg_color=self.color["bg_light"], hover_color=self.color["green"], text="")
        self.app_settings_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.configure_image, fg_color=self.color["bg_light"], hover_color=self.color["green"], text="")
        self.change_name_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.text_image, fg_color=self.color["bg_light"], hover_color=self.color["green"], text="")
        self.info_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.info_image, fg_color=self.color["bg_light"], hover_color=self.color["orange"], text="")
        self.exit_button = CTkButton(self.action_frame_in, width=50, height=50, corner_radius=50, image=self.close_image, fg_color=self.color["bg_light"], hover_color=self.color["orange"], text="")

    def place_action_frame(self) -> None:
        self.action_frame_out.pack(side="left", fill="y")
        self.action_frame_in.pack(padx=(0,3), fill="y", expand=True)
        self.robot_button.pack(padx=5, pady=(10,5))
        self.controller_button.pack(padx=5, pady=5)
        self.app_settings_button.pack(padx=5, pady=5)
        self.change_name_button.pack(padx=5, pady=5)
        self.exit_button.pack(padx=5, pady=(5,10), side="bottom")
        self.info_button.pack(padx=5, pady=5, side="bottom")

    def forget_action_frame(self) -> None:
        self.action_frame_out.pack_forget()

    def configure_action_buttons(self, state:str) -> None:
        self.robot_button._state=state
        self.controller_button._state=state
        self.app_settings_button._state=state
        self.change_name_button._state=state
        self.info_button._state=state
        self.exit_button._state=state

class RobotInfoFrame(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_robot_info_frame(self) -> None:
        self.info_frame_out = CTkFrame(self.parent_frame, fg_color=self.color["green"], corner_radius=10)
        self.info_frame_in = CTkFrame(self.info_frame_out, fg_color=self.color["bg_dark"], corner_radius=0)
        self.info_label_frame = CTkFrame(self.info_frame_in, corner_radius=0, fg_color=self.color["bg_dark"])
        self.info_image_label = CTkLabel(self.info_frame_in, width=150, height=60, text="", image=self.robot_image, corner_radius=0, fg_color=self.color["bg_dark"])
        self.info_robot_label = CTkLabel(self.info_label_frame, text_color=self.text_color["normal"], height=100, text="Root - No Name", corner_radius=0, font=("Arial", 30, "bold"))
        self.info_more_button = CTkButton(self.info_label_frame, text_color=self.text_color["normal"], text="View More Info", font=("Arial", 20, "normal"), image=self.view_more_image, bg_color=self.color["green"], fg_color=self.color["bg_dark"], hover=False, corner_radius=0, command=self._view_more_info)

        self.info_more_label_frame = CTkFrame(self.info_label_frame, corner_radius=10, fg_color=self.color["bg_dark"], border_width=1, border_color=self.color["green"])
        self.info_robot_speed_label = CTkLabel(self.info_more_label_frame, text_color=self.text_color["normal"], text="Current Speed Set: ? cm/s", font=("Arial",15,"normal"))
        self.info_robot_battery_label = CTkLabel(self.info_more_label_frame, text_color=self.text_color["normal"], text="Last Read Battery %: ?%", font=("Arial",15,"normal"))

    def place_robot_info_frame(self) -> None:
        self.info_frame_out.pack(padx=150, pady=10, fill="x", expand=True)
        self.info_frame_in.pack(pady=(0,10), fill="x", expand=True)
        self.info_image_label.pack(side="left")
        self.info_label_frame.pack(side="left", fill="x", expand=True)
        self.info_robot_label.pack(side="top", fill="x",)
        self.info_more_button.pack(side="bottom", fill="x")

    def forget_robot_info_frame(self) -> None:
        self.info_frame_out.pack_forget()

    def _view_more_info(self) -> None:
        self.info_more_button.pack_forget()
        self.info_more_label_frame.pack(side="top", fill="x", padx=20, ipady=20)
        self.info_robot_speed_label.grid(row=0, column=0, sticky="w", pady=(10,0), padx=20)
        self.info_robot_battery_label.grid(row=1, column=0, sticky="w", pady=(10,0), padx=20)

        self.info_more_button.pack(side="bottom", fill="x")
        self.info_more_button.configure(text="View Less Info", image=self.view_less_image, command=self._view_less_info)

    def _view_less_info(self) -> None:
        self.info_more_label_frame.pack_forget()
        self.info_more_button.configure(text="View More Info", image=self.view_more_image, command=self._view_more_info)

    def update_info_frame_vars(self, **vars) -> None:
        if "robot_type" in vars and "robot_name" in vars: 
            robot_name = vars.pop("robot_name")
            if robot_name == "None":self.info_robot_label.configure(text=f"{vars.pop("robot_type")} - No Name")
            else: self.info_robot_label.configure(text=f"{vars.pop("robot_type")} - {robot_name}")
        if "robot_speed" in vars: self.info_robot_speed_label.configure(text=f"Current Speed: {vars.pop("robot_speed")} cm/s")
        if "robot_battery" in vars: self.info_robot_battery_label.configure(text=f"Last Read Battery %: {vars.pop("robot_battery")}%")

class ControllerFrame(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_controller_frame(self) -> None:
        self.controller_frame_out = CTkFrame(self.parent_frame, fg_color=self.color["green"], corner_radius=10)
        self.controller_frame_in = CTkFrame(self.controller_frame_out, fg_color=self.color["bg_dark"], corner_radius=0)
        self.controller_label_frame = CTkFrame(self.controller_frame_in, corner_radius=0, fg_color=self.color["bg_dark"])
        self.controller_image_label = CTkLabel(self.controller_frame_in, width=150, height=60, text="", image=self.controller_image, corner_radius=0, fg_color=self.color["bg_dark"])
        self.controller_label = CTkLabel(self.controller_label_frame, height=100, text_color=self.text_color["normal"], text="No Controller Mounted", corner_radius=0, font=("Arial", 30, "bold"))
        self.controller_more_button = CTkButton(self.controller_label_frame, text="View More Info", font=("Arial", 20, "normal"), image=self.view_more_image, bg_color=self.color["green"], fg_color=self.color["bg_dark"], hover=False, corner_radius=0, command=self._view_more_controller)

        self.controller_more_label_frame = CTkFrame(self.controller_label_frame, corner_radius=10, fg_color=self.color["bg_dark"], border_width=1, border_color=self.color["green"])
        self.controller_connection_type_label = CTkLabel(self.controller_more_label_frame, text_color=self.text_color["normal"], text="Connection Type: None", font=("Arial",15,"normal"))
        self.controller_connection_label = CTkLabel(self.controller_more_label_frame, text_color=self.text_color["normal"], text="Connection: None", font=("Arial",15,"normal"))

    def place_controller_frame(self) -> None:
        self.controller_frame_out.pack(padx=150, pady=10, fill="x", expand=True)
        self.controller_frame_in.pack(pady=(0,10), fill="x", expand=True)
        self.controller_image_label.pack(side="left")
        self.controller_label_frame.pack(side="left", fill="x", expand=True)
        self.controller_label.pack(side="top", fill="x",)
        self.controller_more_button.pack(side="bottom", fill="x")

    def forget_controller_frame(self) -> None:
        self.controller_frame_out.pack_forget()

    def _view_more_controller(self) -> None:
        self.controller_more_button.pack_forget()
        self.controller_more_label_frame.pack(side="top", fill="x", padx=20, ipady=20)
        self.controller_connection_type_label.grid(row=0, column=0, sticky="w", pady=(10,0), padx=20)
        self.controller_connection_label.grid(row=1, column=0, sticky="w", pady=(10,0), padx=20)

        self.controller_more_button.pack(side="bottom", fill="x")
        self.controller_more_button.configure(text="View Less Info", image=self.view_less_image, command=self._view_less_controller)

    def _view_less_controller(self) -> None:
        self.controller_more_label_frame.pack_forget()
        self.controller_more_button.configure(text="View More Info", image=self.view_more_image, command=self._view_more_controller)

    def update_controller_frame_vars(self, connection_type:str, connection:str, controller_name:str) -> None:
        self.controller_label.configure(text=controller_name)
        self.controller_connection_type_label.configure(text=f"Connection Type: {connection_type}")
        self.controller_connection_label.configure(text=f"Connection: {connection}")

class StartFrame(Base):
    def __init__(self) -> None:
        super().__init__()
        self.controller = StringVar(value="Touch Controls")

    def create_start_frame(self) -> None:
        switch_controllers_values: list = ["Starting Default: ", "Touch Controls", "Connected Controller"]
        
        self.start_frame_out = CTkFrame(self.parent_frame, fg_color=self.color["orange"], corner_radius=10)
        self.start_frame_in = CTkFrame(self.start_frame_out, fg_color=self.color["bg_dark"], corner_radius=0)
        self.start_button = CTkButton(self.start_frame_in,  cursor="hand2", fg_color=self.color["bg_dark"], hover_color=self.color["orange"], image=self.play_image, text="Start Connection", compound="left", font=("Arial",20,"bold"))
        
        self.start_switch_default_button = CTkSegmentedButton(self.start_frame_in, fg_color=self.color["bg_dark"], variable=self.controller, values=switch_controllers_values, border_width=2, width=200, height=50, selected_color=self.color["orange"], selected_hover_color=self.color["orange"], unselected_color=self.color["bg_dark"], unselected_hover_color=self.color["bg_light"], text_color=self.text_color["normal"], corner_radius=10)

    def place_start_frame(self) -> None:
        self.start_frame_out.pack(padx=150, pady=10, fill="x", expand=True)
        self.start_frame_in.pack(pady=(0,10), fill="x", expand=True)
        self.start_button.pack(pady=10, fill="x", padx=100)
        self.start_switch_default_button.pack(pady=(0,5))
        self.start_switch_default_button._buttons_dict["Starting Default: "].configure(state="disabled", text_color_disabled="white", fg_color=self.color["bg_dark"])

    def forget_start_frame(self) -> None:
        self.start_frame_out.pack_forget()

class ControlsFrame(Base):
    def __init__(self) -> None:
        super().__init__()

        self.is_mouse_pressed = True
        self.button_pushed = 0
        self.after_id = None
        self.controls = StringVar(value="Touch Controls")
        
    def create_controls_frame(self) -> None:
        switch_controls_values: list = ["Touch Controls", "Connected Controller"]
        self.switch_controls_button = CTkSegmentedButton(self.parent_frame, fg_color=self.color["bg"], variable=self.controls, values=switch_controls_values, border_width=2, width=200, height=50, selected_color=self.color["green"], selected_hover_color=self.color["green"], unselected_color=self.color["bg_dark"], unselected_hover_color=self.color["bg_light"], text_color=self.text_color["normal"], corner_radius=10)

        self.controls_frame = CTkFrame(self.parent_frame, border_width=2, border_color=self.color["green"], corner_radius=10, height=400, width=400, fg_color=self.color["bg_dark"])
        self.drive_frame = CTkFrame(self.controls_frame, width=400, height=400, fg_color="transparent")
        self.button_frame = CTkFrame(self.controls_frame, width=400, height=400, fg_color="transparent")

        self.up_button = CTkButton(self.drive_frame, text="", image=self.up_image, width=180, height=180, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["green"])
        self.left_button = CTkButton(self.drive_frame, text="", image=self.left_image, width=180, height=180, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["green"])
        self.right_button = CTkButton(self.drive_frame, text="", image=self.right_image, width=180, height=180, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["green"])
        self.down_button = CTkButton(self.drive_frame, text="", image=self.down_image, width=180, height=180, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["green"])

        self.a_button = CTkButton(self.button_frame, text="", image=self.a_image, width=120, height=120, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["orange"])
        self.b_button = CTkButton(self.button_frame, text="", image=self.b_image, width=120, height=120, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["orange"])
        self.x_button = CTkButton(self.button_frame, text="", image=self.x_image, width=120, height=120, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["orange"])
        self.y_button = CTkButton(self.button_frame, text="", image=self.y_image, width=120, height=120, corner_radius=20, fg_color=self.color["bg_light"], hover_color=self.color["orange"])

        self.controls_battery_frame = CTkFrame(self.parent_frame, corner_radius=0, height=80, fg_color=self.color["bg"])
        self.controls_battery_label = CTkLabel(self.controls_battery_frame, text_color=self.text_color["normal"], text="Battery Level: 0%", font=("Arial",15,"bold"))
        self.controls_battery_progressbar = CTkProgressBar(self.controls_battery_frame, height=20, corner_radius=30, fg_color=self.color["bg_dark"], progress_color=self.color["green"])    

        self.controls_hint_label = CTkLabel(self.parent_frame, text="Hint: Touch one of the top four corners to get battery level!", font=("Arial", 15, "normal"), text_color="#7C7C7C")
        self.controls_exit_button = CTkButton(self.parent_frame, height=50, text="Exit Connection", font=("Arial",17,"bold"), image=self.close_image, command="left", fg_color=self.color["bg_light"], corner_radius=50, hover_color=self.color["green"])

    def place_controls_frame(self) -> None:
        self.switch_controls_button.pack(pady=(10,10))
        self.controls_frame.pack(pady=30, expand=True, padx=20)

        self.drive_frame.pack(side="left", padx=(20,50), pady=20)
        self.button_frame.pack(side="right", padx=(50,20), pady=20)

        self.up_button.pack(side="top", pady=(0,10))
        self.left_button.pack(side="left", padx=(0,10))
        self.right_button.pack(side="right", padx=(10,0))
        self.down_button.pack(side="bottom")

        self.a_button.pack(side="top")
        self.b_button.pack(side="left", pady=(0,120))
        self.x_button.pack(side="right", pady=(0,120))
        self.y_button.pack(side="bottom", pady=(120,0))
        
        self.controls_hint_label.pack()
        self.controls_battery_frame.pack(pady=10, fill="x", expand=True, padx=300)
        self.controls_battery_label.pack(side="left", padx=10)
        self.controls_battery_progressbar.pack(side="left", fill="x", expand=True)

        self.controls_exit_button.pack(pady=20)

    def bind_controls_buttons(self) -> None:
        self.up_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(1))
        self.left_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(2))
        self.right_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(3))
        self.down_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(4))
        self.a_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(5))
        self.b_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(6))
        self.x_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(7))
        self.y_button.bind("<ButtonPress-1>", lambda event: self.on_mouse_down(8))

        self.up_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.left_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.right_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.down_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.a_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.b_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.x_button.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.y_button.bind("<ButtonRelease-1>", self.on_mouse_up)

    def on_mouse_down(self, button_id:int) -> None:
        self.is_mouse_pressed = True
        self.button_pushed = button_id
        self.move_action()
    
    def on_mouse_up(self, event=None) -> None:
        self.is_mouse_pressed = False
        self.button_pushed = 0
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def move_action(self) -> None:
        if self.is_mouse_pressed: self.after_id = self.after(10, self.move_action)

    def disable_touch_buttons(self, event=None) -> None:
        self.up_button.configure(state="disabled")
        self.left_button.configure(state="disabled")
        self.right_button.configure(state="disabled")
        self.down_button.configure(state="disabled")
        self.a_button.configure(state="disabled")
        self.b_button.configure(state="disabled")
        self.x_button.configure(state="disabled")
        self.y_button.configure(state="disabled")

    def enable_touch_buttons(self, event=None) -> None:
        self.up_button.configure(state="normal")
        self.left_button.configure(state="normal")
        self.right_button.configure(state="normal")
        self.down_button.configure(state="normal")
        self.a_button.configure(state="normal")
        self.b_button.configure(state="normal")
        self.x_button.configure(state="normal")
        self.y_button.configure(state="normal")

class App(TempFrame, ActionFrame, RobotInfoFrame, ControllerFrame, StartFrame, ControlsFrame):
    def __init__(self) -> None:
        super().__init__()

        self.robot: Root | Create3 = ...
        self.controller_thread: Thread = ...

        self.read_controller_on: bool = False
        self.restart: bool = False
        self.robot_disconnect: bool = False
        self.connection_type: str = ""
        self.connection: str = ""
        self.controller_name: str = "None"
        self.marker: str = "UP"
        self.eraser: str = "DOWN"
        
        last_info: list = load_info()

        try:
            self.robot_name: str = last_info[0]
            self.robot_speed: int = int(last_info[1])
            self.robot_type: str = last_info[2]
            self.robot_battery: int = int(last_info[3])
            self.a_binding: str = last_info[4]
            self.b_binding: str = last_info[5]
            self.x_binding: str = last_info[6]
            self.y_binding: str = last_info[7]
            self.honk_pitch: int = last_info[8]
            
            self.create_all_frames()

            if last_info[9] == "0":
                self.place_startup_frame()
                self.update()
                sleep(3)
                self.forget_startup_frame()
                self.update()
        except:
            save_info(["None", "10", "Root", "0", "Marker Up/Down", "Eraser Up/Down", "Honk", "Quick Turn", "500", "0"])
            exit(5)
        self.place_main_frames()
        self.configure_button_commands()
        self.update_info_frame_vars(robot_speed=self.robot_speed, robot_name=self.robot_name, robot_type=self.robot_type, robot_battery=self.robot_battery)
        self.update_idletasks()

    def create_all_frames(self) -> None:
        self.create_temp_frame()
        self.create_action_frame()
        self.create_robot_info_frame()
        self.create_controller_frame()
        self.create_start_frame()
        self.create_controls_frame()

    def place_main_frames(self) -> None:
        self.place_action_frame()
        self.place_robot_info_frame()
        self.place_controller_frame()
        self.place_start_frame()

    def forget_main_frame(self) -> None:
        self.forget_robot_info_frame()
        self.forget_controller_frame()
        self.forget_start_frame()
        self.forget_action_frame()

    def configure_button_commands(self) -> None:
        self.robot_button.configure(command=self.open_robot_window)
        self.controller_button.configure(command=self.open_controller_connect_window)
        self.app_settings_button.configure(command=self.open_config_window)
        self.change_name_button.configure(command=self.open_change_name_window)
        self.switch_controls_button.configure(command=self.switch_controls)
        self.start_button.configure(command=self.start_robot)
        self.exit_button.configure(command=self.ask_to_exit)
        self.info_button.configure(command=self.open_info_window)
        self.controls_exit_button.configure(command=self.restart_app)
        self.bind_controls_buttons()

    def configure_app_vars(self, **vars) -> None:
        if "restarts" in vars: self.restarts = vars.pop("restarts")
        if "robot_name" in vars: self.robot_name = vars.pop("robot_name")
        if "robot_type" in vars: self.robot_type = vars.pop("robot_type")
        if "robot_speed" in vars: self.robot_speed = vars.pop("robot_speed")
        if "robot_battery" in vars: self.robot_battery = vars.pop("robot_battery")
        if "connection" in vars: self.connection = vars.pop("connection")
        if "connection_type" in vars: self.connection_type = vars.pop("connection_type")
        if "controller_name" in vars: self.controller_name = vars.pop("controller_name")
        if "a_binding" in vars: self.a_binding = vars.pop("a_binding")
        if "b_binding" in vars: self.b_binding = vars.pop("b_binding")
        if "x_binding" in vars: self.x_binding = vars.pop("x_binding")
        if "y_binding" in vars: self.y_binding = vars.pop("y_binding")
        if "honk_pitch" in vars: self.honk_pitch = vars.pop("honk_pitch")
    
    def open_robot_window(self) -> None:
        self.configure_action_buttons("disabled")
        rw = RobotWindow(self.robot_name)
        rw.wait_window()
        self.configure_action_buttons("normal")
        if rw.save_window_info:
            rw_info = rw.get_robot_info()
            self.configure_app_vars(robot_name=rw_info[0], robot_speed=rw_info[1], robot_type=rw_info[2])
            self.update_info_frame_vars(robot_speed=self.robot_speed, robot_name=self.robot_name, robot_type=self.robot_type)

    def open_controller_connect_window(self) -> None:
        self.configure_action_buttons("disabled")
        ccw = ConnectControllerWindow()
        ccw.wait_window()
        self.configure_action_buttons("normal")
        if ccw.save_window_info:
            ccw_info = ccw.get_controller_info()
            self.configure_app_vars(connection_type=ccw_info[0], connection=ccw_info[1], controller_name=ccw_info[2])
            self.update_controller_frame_vars(connection=self.connection, connection_type=self.connection_type, controller_name=self.controller_name)

    def open_config_window(self) -> None:
        self.configure_action_buttons("disabled")
        sw = SettingsWindow(a_binding=self.a_binding, b_binding=self.b_binding, x_binding=self.x_binding, y_binding=self.y_binding, honk_pitch=self.honk_pitch)
        sw.wait_window()
        self.configure_action_buttons("normal")
        if sw.save_window_info:
            sw_info = sw.get_controller_configurations()
            self.configure_app_vars(a_binding=sw_info[0], b_binding=sw_info[1], x_binding=sw_info[2], y_binding=sw_info[3], honk_pitch=sw_info[4])

    def open_change_name_window(self) -> None:
        self.configure_action_buttons("disabled")
        cnw = ChangeNameWindow(self.robot_name)
        cnw.wait_window()
        self.configure_action_buttons("normal")
        if cnw.restart:
            if cnw.change_successful:
                cnw_info = cnw.get_change_name_info()
                self.configure_app_vars(robot_name=cnw_info[0], robot_type=cnw_info[1])
            self.absolute_restart_app()

    def open_info_window(self) -> None:
        self.configure_action_buttons("disabled")
        aiw = AppInfoWindow(__version__)
        aiw.wait_window()
        self.configure_action_buttons("normal")

    def switch_controls(self, event=None) -> None:
        if event == "Touch Controls": 
            self.enable_touch_buttons()
            self.stop_reading_controller()
        elif event == "Connected Controller": 
            self.disable_touch_buttons()
            self.start_reading_controller()

    def update_battery_level(self) -> None:
        if self.robot_battery < 30: self.controls_battery_progressbar.configure(progress_color=self.color["orange"])
        else: self.controls_battery_progressbar.configure(progress_color=self.color["green"])

        self.controls_battery_progressbar.set(self.robot_battery/100)
        self.controls_battery_label.configure(text=f"Battery Level: {self.robot_battery}%")

    def start_reading_controller(self) -> None:
        self.read_controller_on = True
        if self.controller_name == "None":
            messagebox.showerror("RC - Error", "No controller specified!")
            self.read_controller_one = False
        else:
            if self.connection_type == "Serial":
                self.controller_thread = Thread(target=self.read_serial_controller, daemon=True)
                self.controller_thread.start()
            elif self.connection_type == "BLE":
                self.controller_thread = Thread(target=self.run_async_ble_connection, daemon=True)
                self.controller_thread.start()
        
    def stop_reading_controller(self) -> None:
        self.read_controller_on = False

    def run_async_ble_connection(self) -> None:
        run_asyncio(self.read_ble_controller())

    async def read_ble_controller(self) -> None:
        ble_device = BleakClient(self.connection)
        await ble_device.connect()

        while self.read_controller_on:
            try:
                raw_controller_value = await ble_device.read_gatt_char("C0397A41-A619-445A-8AE4-B4E7B1E98A62")
                self.button_pushed = int(raw_controller_value.hex(), 16)
            except: pass
            
        await ble_device.disconnect()

    def read_serial_controller(self) -> None:
        try: serial_device = Serial(self.connection, baudrate=9600)
        except: 
            messagebox.showerror("RC - Error", "Can not find controller!")
            self.read_controller_on = False

        while self.read_controller_on: 
            try: 
                data = serial_device.readline().decode().rstrip()
                self.button_pushed = int(data)
            except: pass

    def start_robot(self) -> None:
        if self.robot_name == "None":
            if self.robot_type == "Root": self.robot = Root(Bluetooth())
            elif self.robot_type == "Create3": self.robot = Create3(Bluetooth())
        else: 
            if self.robot_type == "Root": self.robot = Root(Bluetooth(self.robot_name))
            elif self.robot_type == "Create3": self.robot = Create3(Bluetooth(self.robot_name))

        self.switch_controls_button.set(self.controller.get())
        self.update_battery_level()
        self.switch_controls(self.controller.get())
        self.forget_main_frame()
        self.place_controls_frame()  

        Thread(target=self.activate_robot, daemon=True).start()

    def activate_robot(self) -> None:
        self.restart = True

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
            self.robot_battery = _battery[1]
            self.update_battery_level()

        @event(self.robot.when_cliff_sensor, [True])
        async def cliff(robot) -> None:
            await robot.set_lights_spin_rgb(255,139,0)

        @event(self.robot.when_cliff_sensor, [False])
        async def cliff(robot) -> None:
            await robot.set_lights_on_rgb(97,167,7)

        @event(self.robot.when_play)
        async def play(robot) -> None:
            await robot.set_lights_on_rgb(97,167,7)
            while self.robot_disconnect == False:
                if self.button_pushed == 0:
                    await robot.set_wheel_speeds(0,0)
                if self.button_pushed == 1:
                    await robot.set_wheel_speeds(self.robot_speed,self.robot_speed)
                if self.button_pushed == 2:
                    await robot.set_wheel_speeds(-self.robot_speed,self.robot_speed)
                if self.button_pushed == 3:
                    await robot.set_wheel_speeds(self.robot_speed,-self.robot_speed)
                if self.button_pushed == 4:
                    await robot.set_wheel_speeds(-self.robot_speed,-self.robot_speed)
                if self.button_pushed == 5:
                    await use_binding(self.a_binding, robot)
                if self.button_pushed == 6:
                    await use_binding(self.b_binding, robot)
                if self.button_pushed == 7:
                    await use_binding(self.x_binding, robot)
                if self.button_pushed == 8:
                    await use_binding(self.y_binding, robot)

        self.robot.play()

    def absolute_restart_app(self) -> None:
        messagebox.showwarning("RC - Restarting", "A restart is required for this change to take effect!")
        self.restart = True
        self.update()
        self.destroy()

    def restart_app(self) -> None:
        if messagebox.askyesno("RC - Cutting Connection", "Are you sure you want to stop connection?"):
            self.robot_disconnect = True
            self.update()
            self.destroy()
        
    def ask_to_exit(self) -> None:
        if messagebox.askyesno("RC - Exiting", "Are you sure you want to exit?"):
            self.restart = False
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

    try:
        app.read_controller_on = False
        app.controller_thread.join()
    except: pass
    finally:
        if app.restart:
            save_info([app.robot_name, app.robot_speed, app.robot_type, app.robot_battery, app.a_binding, app.b_binding, app.x_binding, app.y_binding, app.honk_pitch,"1"]) 
            exit(5)
        else:
            save_info([app.robot_name, app.robot_speed, app.robot_type, app.robot_battery, app.a_binding, app.b_binding, app.x_binding, app.y_binding, app.honk_pitch,"0"]) 
            exit()
