#import built-in modules
from asyncio import run as run_asyncio
from threading import Thread
from tkinter import messagebox # tkinter is not built into Linux Distributions

#import external modules
from customtkinter import CTkToplevel, CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton, CTkSegmentedButton, CTkProgressBar, CTkComboBox, CTkSlider, CTkSwitch, CTkEntry, StringVar
from serial.tools.list_ports import comports as find_devices
from bleak import BleakScanner
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root, Create3

#import internal modules
from tooling.ctk_listbox import CTkListbox
from tooling.ctk_spinbox import CTkSpinbox
from tooling.theme import Theme
from tooling.__init__ import __system__

class BaseWindow(CTkToplevel, Theme):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(f"500x500+{int(self.winfo_screenwidth()/2 - 250)}+{int(self.winfo_screenheight()/2.2 - 250)}")
        self.minsize(500,500)
        self.maxsize(500,600)

        if __system__.startswith("win"):
            self.grab_set() # Windows environments only!

        self.save_window_info: bool = False

        self.parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self.parent_frame.pack(expand=True, fill="both")
        self.scrollable_frame = CTkScrollableFrame(self.parent_frame, width=400, height=300, border_width=2, border_color=self.color["green"], fg_color=self.color["bg"], corner_radius=20, label_text="CTkWindow", label_font=("Arial",20,"bold"), label_fg_color=self.color["bg"], label_text_color=self.text_color["normal"], scrollbar_button_color=self.color["bg_light"], scrollbar_button_hover_color=self.color["green"])
        self.save_button = CTkButton(self.parent_frame, cursor="hand2", text="Save", width=200, height=30, corner_radius=10, fg_color=self.color["bg_light"], hover_color=self.color["orange"], font=("Arial", 15, "bold"), text_color=self.text_color["normal"], command=self.save_info)

        self.scrollable_frame.pack(expand=True)
        self.scrollable_frame._scrollbar.grid_configure(padx=(0,5))
        self.save_button.pack(side="bottom", pady=(0,10))

        self.update()

    def change_to_listbox_type(self) -> None:
        self.scrollable_frame.pack_forget()
        
        self.scrollable_frame = CTkListbox(self.parent_frame, width=400, height=300, scrollbar_fg_color=self.color["bg_light"], scrollbar_hover_color=self.color["green"], corner_radius=20, border_color=self.color["green"], border_width=2, header_font=("Arial",20, "bold"), header_fg_color=self.color["bg"])
        self.scrollable_frame._parent_frame._scrollbar.grid_configure(padx=(0,10))

        self.scrollable_frame.pack(expand=True)

    def save_info(self) -> None:
        self.save_window_info = True
        self.destroy()

class ConnectControllerWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__()

        self.title("RC - Find A Controller")
        self.change_to_listbox_type()

        self.button_selected: int|None = None
        self.connection_type = StringVar(value="BLE")
        switch_connection_options: list = ["Serial", "BLE"]

        self.scrollable_frame.configure(header_text="Local Devices")
        self.switch_connection_button = CTkSegmentedButton(self.scrollable_frame.cget("parent_frame"), variable=self.connection_type, values=switch_connection_options, corner_radius=10, height=60, font=("Arial", 20, "bold"), fg_color=self.color["bg"], unselected_color=self.color["bg_dark"], selected_color=self.color["green"], unselected_hover_color=self.color["bg_light"], selected_hover_color=self.color["green"], command=self.switch_connection_buttons)
        self.scrollable_frame.insert_ctkobject(self.switch_connection_button, padx=20, pady=20, fill="x")
        self.scrollable_frame.delete_item_from_index(0)
        self.switch_connection_button.set("BLE")

        self.serial_devices: list[list[str,str]] = [[port_info[0],port_info[1]] for port_info in find_devices()]
        self.ble_devices: list = []
        find_ble_thread = Thread(target=self.run_async_func, daemon=True)
        find_ble_thread.start()
        self.update()
        find_ble_thread.join()
        
        self.create_window_objects()
        self.place_ble_window()

    def create_window_objects(self) -> None:
        self.serial_device_buttons: list = []
        self.ble_device_buttons: list = []

        index: int = 0
        for device in self.serial_devices:
            _button = CTkButton(self.scrollable_frame.cget("parent_frame"), cursor="hand2", font=("Arial",18,"normal"), text_color=self.text_color["normal"], width=350, height=60, fg_color=self.color["bg_light"], hover_color=self.color["orange"], text=device[0]+" || "+device[1], command=lambda button_id=index: self.button_pressed(button_id))
            self.serial_device_buttons.append(_button)
            index += 1
        
        index = 0
        for device in self.ble_devices:
            _button = CTkButton(self.scrollable_frame.cget("parent_frame"), cursor="hand2", font=("Arial",18,"normal"), text_color=self.text_color["normal"], width=350, height=60, fg_color=self.color["bg_light"], hover_color=self.color["orange"], text=device[1], command=lambda button_id=index: self.button_pressed(button_id))
            self.ble_device_buttons.append(_button)
            index += 1
    
    def button_pressed(self, button_id:int) -> None:
        if self.connection_type.get() == "Serial":
            for id in range(0,len(self.serial_device_buttons)):
                if id == button_id: 
                    self.serial_device_buttons[button_id].configure(state="active", fg_color=self.color["green"])
                    self.button_selected = button_id
                else: self.serial_device_buttons[id].configure(state="normal", fg_color=self.color["bg_light"])
        elif self.connection_type.get() == "BLE":
            for id in range(0,len(self.ble_device_buttons)):
                if id == button_id: 
                    self.ble_device_buttons[button_id].configure(state="active", fg_color=self.color["green"])
                    self.button_selected = button_id
                else: self.ble_device_buttons[id].configure(state="normal", fg_color=self.color["bg_light"])

    def place_serial_window(self) -> None:
        for button in self.serial_device_buttons:
            self.scrollable_frame.insert_ctkobject(button, padx=20, pady=10)

    def place_ble_window(self) -> None:
        for button in self.ble_device_buttons:
            self.scrollable_frame.insert_ctkobject(button, padx=20, pady=20)

    def switch_connection_buttons(self, event=None) -> None:
        self.scrollable_frame.clear()
        self.create_window_objects()
        if self.connection_type.get() == "Serial": self.place_serial_window()
        elif self.connection_type.get() == "BLE": self.place_ble_window()

    def count_char(self, string:str, char:str) -> int:
        count:int = 0
        for i in string:
            if i == char: count += 1
        
        return count

    def run_async_func(self) -> None:
        run_asyncio(self.find_ble_devices())

    async def find_ble_devices(self) -> None:
        _ble_devices = await BleakScanner.discover(timeout=3)
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

    def get_controller_info(self) -> None:
        if self.connection_type.get() == "Serial": 
            try: return ["Serial", self.serial_devices[self.button_selected][0], self.serial_devices[self.button_selected][1]]
            except: return ["None", "None", "None"]
        elif self.connection_type.get() == "BLE":
            try: return ["BLE", self.ble_devices[self.button_selected][0], self.ble_devices[self.button_selected][1]]
            except: ["None", "None", "None"]

class SettingsWindow(BaseWindow):
    def __init__(self, a_binding:str="Marker Up/Down", b_binding:str="Eraser Up/Down", x_binding:str="Honk", y_binding:str="Quick Turn", honk_pitch:int=500) -> None:
        super().__init__()

        self.title("RC - App Settings")
        self.scrollable_frame.configure(label_text="App Settings")

        self.a_value = StringVar(value=a_binding)
        self.b_value = StringVar(value=b_binding)
        self.x_value = StringVar(value=x_binding)
        self.y_value = StringVar(value=y_binding)
        self.honk_pitch_value: int = honk_pitch
        self.keyframes_value = StringVar(value=False)

        self.create_window_objects()
        self.place_window()

    def create_window_objects(self) -> None:
        mapping_option_mappings: list = ["Maker Up/Down", "Eraser Up/Down", "Honk", "Quick Turn"]
    
        self.mapping_title_label = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="Mapping Controls", font=("Arial", 20, "bold"))
        self.mapping_option_a_label = CTkLabel(self.scrollable_frame, text="A-Button", text_color=self.text_color["normal"], font=("Arial", 15, "normal"), fg_color=self.color["bg_light"], corner_radius=10)
        self.mapping_option_a_dropdown = CTkComboBox(self.scrollable_frame, values=mapping_option_mappings, variable=self.a_value, justify="center", width=250, height=30, font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_color=self.color["green"], border_width=2, corner_radius=10, button_color=self.color["green"], button_hover_color=self.color["bg_light"])
        self.mapping_option_b_label = CTkLabel(self.scrollable_frame, text="B-Button", text_color=self.text_color["normal"], font=("Arial", 15, "normal"), fg_color=self.color["bg_light"], corner_radius=10)
        self.mapping_option_b_dropdown = CTkComboBox(self.scrollable_frame, values=mapping_option_mappings, variable=self.b_value, justify="center", width=250, height=30, font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_color=self.color["green"], border_width=2, corner_radius=10, button_color=self.color["green"], button_hover_color=self.color["bg_light"])
        self.mapping_option_x_label = CTkLabel(self.scrollable_frame, text="X-Button", text_color=self.text_color["normal"], font=("Arial", 15, "normal"), fg_color=self.color["bg_light"], corner_radius=10)
        self.mapping_option_x_dropdown = CTkComboBox(self.scrollable_frame, values=mapping_option_mappings, variable=self.x_value, justify="center", width=250, height=30, font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_color=self.color["green"], border_width=2, corner_radius=10, button_color=self.color["green"], button_hover_color=self.color["bg_light"])
        self.mapping_option_y_label = CTkLabel(self.scrollable_frame, text="Y-Button", text_color=self.text_color["normal"], font=("Arial", 15, "normal"), fg_color=self.color["bg_light"], corner_radius=10)
        self.mapping_option_y_dropdown = CTkComboBox(self.scrollable_frame, values=mapping_option_mappings, variable=self.y_value, justify="center", width=250, height=30, font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_color=self.color["green"], border_width=2, corner_radius=10, button_color=self.color["green"], button_hover_color=self.color["bg_light"])
        self.mapping_option_honk_pitch_label = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text=f"Honk Pitch: {self.honk_pitch_value}Hz", fg_color=self.color["bg_light"], corner_radius=10, font=("Arial",15,"normal"))
        self.mapping_option_honk_pitch_slider = CTkSlider(self.scrollable_frame, width=100, height=20, corner_radius=10, number_of_steps=2, fg_color=self.color["bg_light"], progress_color=self.color["green"], button_color="white", button_hover_color=self.color["bg_dark"], to=2, command=self._change_honk_pitch)
        self.mapping_option_honk_pitch_slider.set(((float(self.honk_pitch_value)+100)/300)-1)

        self.keyframes_title_label = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="Keyframes", font=("Arial", 20, "bold"))
        self.keyframes_option_label = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="Keyframes On?", state="disabled", fg_color=self.color["bg_light"], corner_radius=10, font=("Arial", 15, "normal"))
        self.keyframes_option_switch = CTkSwitch(self.scrollable_frame, text="", state="disabled", variable=self.keyframes_value, switch_height=20, switch_width=60, progress_color=self.color["green"], fg_color=self.color["bg_light"], button_color="white", onvalue=True, offvalue=False)

    def place_window(self) -> None:
        self.mapping_title_label.grid(row=0, column=0, columnspan=10, sticky="w", pady=(10,0))
        self.mapping_option_a_label.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.mapping_option_a_dropdown.grid(row=1, column=1, columnspan=3, sticky="w", pady=(10,0))
        self.mapping_option_b_label.grid(row=2, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.mapping_option_b_dropdown.grid(row=2, column=1, columnspan=3, sticky="w", pady=(10,0))
        self.mapping_option_x_label.grid(row=3, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.mapping_option_x_dropdown.grid(row=3, column=1, columnspan=3, sticky="w", pady=(10,0))
        self.mapping_option_y_label.grid(row=4, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.mapping_option_y_dropdown.grid(row=4, column=1, columnspan=3, sticky="w", pady=(10,0))
        self.mapping_option_honk_pitch_label.grid(row=5, column=0, columnspan=10, sticky="w", padx=(0,10), pady=(10,0))
        self.mapping_option_honk_pitch_slider.grid(row=5, column=2, sticky="w", pady=(10,0))
        self.keyframes_title_label.grid(row=6, column=0, columnspan=10, sticky="w", pady=(30,0))
        self.keyframes_option_label.grid(row=7, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.keyframes_option_switch.grid(row=7, column=1, columnspan=10, sticky="w", pady=(10,0))

    def _change_honk_pitch(self, event=None) -> None:
        pitch_value = int(self.mapping_option_honk_pitch_slider.get())
        match pitch_value:
            case 0: self.honk_pitch_value = 300
            case 1: self.honk_pitch_value = 500
            case 2: self.honk_pitch_value = 800
        self.mapping_option_honk_pitch_label.configure(text=f"Honk Pitch: {self.honk_pitch_value}Hz")

    def get_controller_configurations(self) -> list:
        return [self.a_value.get(), self.b_value.get(), self.x_value.get(), self.y_value.get(), self.honk_pitch_value, self.keyframes_value.get()]

class RobotWindow(BaseWindow):
    def __init__(self, robot_name) -> None:
        super().__init__()

        self.title("RC - Find A Robot")
        self.scrollable_frame.configure(label_text="Robot Options")

        self.robot_name = StringVar(value=robot_name)
        self.robot_name_on = StringVar(value=0)
        self.robot_speed: int = 10
        self.robot_type = StringVar(value="Root")

        self.create_window_objects()
        self.place_window()
        self.switch_find_by_name()

    def create_window_objects(self) -> None:
        option_type_values: list = ["Root", "Create3"]

        self.robot_find_by_name_label = CTkLabel(self.scrollable_frame, text="Find Robot By Name", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], corner_radius=10)
        self.robot_find_by_name_switch = CTkSwitch(self.scrollable_frame, text="", variable=self.robot_name_on, switch_width=70, switch_height=25, progress_color=self.color["green"], command=self.switch_find_by_name)
        self.robot_option_name_label = CTkLabel(self.scrollable_frame, text="Robot Name", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], text_color_disabled=self.text_color["disabled"], corner_radius=10, fg_color=self.color["bg_light"])
        self.robot_option_name_entry = CTkEntry(self.scrollable_frame, textvariable=self.robot_name, justify="center", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_width=2, border_color=self.color["green"], corner_radius=10, width=200, height=30)
        self.robot_option_speed_label = CTkLabel(self.scrollable_frame, text="Speed of Robot", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], corner_radius=10, fg_color=self.color["bg_light"])
        self.robot_option_speed_spinbox = CTkSpinbox(self.scrollable_frame, width=195, height=30, text="", unit="cm/s", text_font=("Arial", 15, "normal"), button_font=("Arial", 15, "bold"), border_color=self.color["green"], border_width=2, button_hover_color=self.color["green"], fg_color=self.color["bg_light"], corner_radius=10, minimum=1, maximum=10, speed=200, value=10)
        self.robot_option_type_label = CTkLabel(self.scrollable_frame, text="Robot Type", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], corner_radius=10, fg_color=self.color["bg_light"])
        self.robot_option_type_dropdown = CTkComboBox(self.scrollable_frame, state="disabled", font=("Arial", 15, "normal"), justify="center", values=option_type_values, variable=self.robot_type, width=200, height=30, text_color=self.text_color["normal"], fg_color=self.color["bg_light"], button_color=self.color["green"], button_hover_color=self.color["bg_light"], border_width=2, border_color=self.color["green"], corner_radius=10)

    def place_window(self) -> None:
        self.robot_find_by_name_label.grid(row=0, column=0, pady=(10,0), padx=(0,10), sticky="w")
        self.robot_find_by_name_switch.grid(row=0, column=1, pady=(10,0), sticky="w")
        self.robot_option_name_label.grid(row=1, column=0, pady=(10,0), padx=(0,10), sticky="w")
        self.robot_option_name_entry.grid(row=1, column=1, pady=(10,0), sticky="w")
        self.robot_option_speed_label.grid(row=2, column=0, pady=(10,0), padx=(0,10), sticky="w")
        self.robot_option_speed_spinbox.grid(row=2, column=1, pady=(10,0), sticky="w")
        self.robot_option_type_label.grid(row=3, column=0, pady=(10,0), padx=(0,10), sticky="w")
        self.robot_option_type_dropdown.grid(row=3, column=1, pady=(10,0), sticky="w")
        
    def switch_find_by_name(self) -> None:
        match int(self.robot_name_on.get()):
            case 0: 
                self.robot_option_name_label.configure(state="disabled")
                self.robot_option_name_entry.configure(state="disabled", text_color=self.text_color["disabled"])
            case 1: 
                self.robot_option_name_label.configure(state="normal")
                self.robot_option_name_entry.configure(state="normal", text_color=self.text_color["normal"])

    def get_robot_info(self) -> list:
        robot_info: list = []

        if int(self.robot_name_on.get()) == 0: robot_info.append("None")
        else: robot_info.append(self.robot_name.get())

        robot_info.append(self.robot_option_speed_spinbox.get_value())
        robot_info.append(self.robot_type.get())

        return robot_info
    
class ChangeNameWindow(BaseWindow):
    def __init__(self, robot_name) -> None:
        super().__init__()
        
        self.title("RC - Change Robot Name")
        self.scrollable_frame.configure(label_text="Change Robot Name")
        self.save_button.configure(text="Change Name", command=self.start_name_change)

        self.robot: Root | Create3 = ...
        self.robot_name = StringVar(value=robot_name)
        self.robot_new_name = StringVar()
        self.robot_name_on = StringVar(value=0)
        self.robot_type = StringVar(value="Root")
        self.restart: bool = False
        self.change_successful: bool = False

        self.create_window_objects()
        self.place_main_window()
        self.switch_find_by_name()

    def create_window_objects(self) -> None:
        option_type_values: list = ["Root", "Create3"]

        self.search_by_title = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text=f"Search Robot By Name", font=("Arial", 20, "bold"))
        self.search_by_name_label = CTkLabel(self.scrollable_frame, text="Find Robot By Name", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], corner_radius=10)
        self.search_by_name_switch = CTkSwitch(self.scrollable_frame, text="", variable=self.robot_name_on, switch_width=70, switch_height=25, progress_color=self.color["green"], command=self.switch_find_by_name)
        self.search_option_name_label = CTkLabel(self.scrollable_frame, text="Robot Name", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], text_color_disabled=self.text_color["disabled"], corner_radius=10, fg_color=self.color["bg_light"])
        self.search_option_name_entry = CTkEntry(self.scrollable_frame, textvariable=self.robot_name, justify="center", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_width=2, border_color=self.color["green"], corner_radius=10, width=200, height=30)
        self.search_option_type_label = CTkLabel(self.scrollable_frame, text="Robot Type", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], corner_radius=10, fg_color=self.color["bg_light"])
        self.search_option_type_dropdown = CTkComboBox(self.scrollable_frame, state="disabled", font=("Arial", 15, "normal"), justify="center", values=option_type_values, variable=self.robot_type, width=200, height=30, text_color=self.text_color["normal"], fg_color=self.color["bg_light"], button_color=self.color["green"], button_hover_color=self.color["bg_light"], border_width=2, border_color=self.color["green"], corner_radius=10)
        self.new_name_title = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="New Name", font=("Arial", 20, "bold"))
        self.new_name_label = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="New Robot Name", fg_color=self.color["bg_light"], corner_radius=10, font=("Arial",15,"normal"))
        self.new_name_entry = CTkEntry(self.scrollable_frame, textvariable=self.robot_new_name, justify="center", font=("Arial", 15, "normal"), text_color=self.text_color["normal"], fg_color=self.color["bg_light"], border_width=2, border_color=self.color["green"], corner_radius=10, width=200, height=30)
        
        self.changing_name_title = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="Changing Name", font=("Arial",20,"bold"))
        self.changing_name_warning = CTkLabel(self.scrollable_frame, text_color=self.text_color["normal"], text="Please do not close this window!", fg_color=self.color["bg_light"], corner_radius=10, font=("Arial",12,"normal"))
        self.changing_name_progress = CTkProgressBar(self.scrollable_frame, width=300, height=15, fg_color=self.color["bg_dark"], progress_color=self.color["green"])

    def place_main_window(self) -> None:
        self.search_by_title.grid(row=0, column=0, columnspan=10, sticky="w", pady=(10,0))
        self.search_by_name_label.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.search_by_name_switch.grid(row=1, column=1, sticky="w", pady=(10,0))
        self.search_option_name_label.grid(row=2, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.search_option_name_entry.grid(row=2, column=1, sticky="w", pady=(10,0))
        self.search_option_type_label.grid(row=3, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.search_option_type_dropdown.grid(row=3, column=1, sticky="w", pady=(10,0))
        self.new_name_title.grid(row=4, column=0, columnspan=10, sticky="w", pady=(20,0))
        self.new_name_label.grid(row=5, column=0, sticky="w", padx=(0,10), pady=(10,0))
        self.new_name_entry.grid(row=5, column=1, sticky="w", pady=(10,0))

    def forget_main_window(self) -> None:
        self.search_by_title.grid_forget()
        self.search_by_name_label.grid_forget()
        self.search_by_name_switch.grid_forget()
        self.search_option_name_label.grid_forget()
        self.search_option_name_entry.grid_forget()
        self.search_option_type_label.grid_forget()
        self.search_option_type_dropdown.grid_forget()
        self.new_name_title.grid_forget()
        self.new_name_label.grid_forget()
        self.new_name_entry.grid_forget()

    def start_name_change(self) -> None:
        if messagebox.askyesno("RC - Pending Operation", "Are you sure you want to change the name?"):
            if len(self.robot_new_name.get()) == 0:
                messagebox.showerror("RC - Error", "Must enter a valid name!")
            else:
                self.restart = True
                self.forget_main_window()
                self.changing_name_title.pack()
                self.changing_name_warning.pack(pady=10)
                self.changing_name_progress.pack(pady=20)
                self.changing_name_progress.set(0)
                self.save_button.configure(state="disabled")

                match int(self.robot_name_on.get()):
                    case 0:
                        if self.robot_type.get() == "Root": self.robot = Root(Bluetooth())
                        elif self.robot_type.get() == "Create3": self.robot = Create3(Bluetooth())
                    case 1: 
                        if self.robot_type.get() == "Root": self.robot = Root(Bluetooth(self.robot_name.get()))
                        elif self.robot_type.get() == "Create3": self.robot = Create3(Bluetooth(self.robot_name.get()))

                self.changing_name_progress.set(0.333)
                Thread(target=self.change_name, daemon=True).start()

    def change_name(self) -> None:
        @event(self.robot.when_play)
        async def play(robot) -> None:
            self.changing_name_progress.set(0.667)
            await robot.set_name(self.robot_new_name.get())
            self.changing_name_progress.set(1)
            self.change_successful = True
            await robot.disconnect()
            self.destroy()    

        self.robot.play()

    def switch_find_by_name(self) -> None:
        match int(self.robot_name_on.get()):
            case 0: 
                self.search_option_name_label.configure(state="disabled")
                self.search_option_name_entry.configure(state="disabled", text_color=self.text_color["disabled"])
            case 1: 
                self.search_option_name_label.configure(state="normal")
                self.search_option_name_entry.configure(state="normal", text_color=self.text_color["normal"])

    def get_change_name_info(self) -> list[str,str]:
        return [self.robot_new_name.get(), self.robot_type.get()]
    
class AppInfoWindow(BaseWindow):
    def __init__(self, version:str) -> None:
        super().__init__()

        self.title("RC - App Information")
        self.scrollable_frame.configure(label_text="App Information")
        self.version = version
        self.save_button.configure(text="Close")
        self.create_window_objects()
        self.place_window()

    def create_window_objects(self) -> None:
        self.app_info_company_label = CTkLabel(self.scrollable_frame, text="RootConnect", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
        self.app_info_version_label = CTkLabel(self.scrollable_frame, text=f"Version: {self.version}", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
        self.app_info_date_label = CTkLabel(self.scrollable_frame, text="Build Date: 04/15/2026", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
        self.app_info_build_label = CTkLabel(self.scrollable_frame, text="UI Library: Tkinter/CustomTkinter", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
        self.app_info_license_label = CTkLabel(self.scrollable_frame, text="License: MIT Agreement", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
        self.app_info_developer_label = CTkLabel(self.scrollable_frame, text="Developer: Aaron Pohlman", text_color=self.text_color["normal"], font=("Arial",17,"normal"))
            
    def place_window(self) -> None:
        self.app_info_company_label.grid(row=0, column=0, sticky="w", padx=20, pady=(10,0))
        self.app_info_version_label.grid(row=1, column=0, sticky="w", padx=20, pady=(10,0))
        self.app_info_date_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10,0))
        self.app_info_build_label.grid(row=3, column=0, sticky="w", padx=20, pady=(10,0))
        self.app_info_license_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10,0))
        self.app_info_developer_label.grid(row=5, column=0, sticky="w", padx=20, pady=(10,0))    
