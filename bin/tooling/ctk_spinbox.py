from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage
from PIL import Image

__version__ = "0.1.5"

class CTkSpinbox:
    def __init__(self,
                 master,
                 width:int=140,
                 height:int=50,
                 corner_radius:int=5,
                 border_width:int=2,
                 value:int=0,
                 step:int|float=1,
                 speed: int = 10,
                 maximum:int|None=None,
                 minimum:int|None=None,
                 border_color:str="red",
                 fg_color:str="#202020",
                 text_color:str="white",
                 text:str="CTkSpinbox",
                 text_placement:str="left",
                 button_up_image:str|None=None,
                 button_down_image:str|None=None,
                 button_hover_color:str="#404040",
                 unit:str="u",
                 state:str="normal",
                 button_image_size:tuple[int|int]|None=None,
                 text_font:tuple[str|int|str]=("Arial",13,"bold"),
                 button_font:tuple[str|int|str]=("Arial",15,"bold")) -> None:
        """Creates a CTkSpinbox with custom units and maximums and minimum values"""
        self.master = master
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.value = value
        self.step = step
        self.speed = speed
        self.maximum = maximum
        self.minimum = minimum
        self.border_color = border_color
        self.fg_color = fg_color
        self.text_color = text_color
        self.text = text
        self.text_placement = text_placement

        if button_up_image is not None:
            self.button_up_image = CTkImage(Image.open(button_up_image), size=button_image_size)
        else:
            self.button_up_image = None

        if button_down_image is not None:
            self.button_down_image = CTkImage(Image.open(button_down_image), size=button_image_size)
        else:
            self.button_down_image = None
        
        self.unit = unit
        self.state = state
        self.button_hover_color = button_hover_color
        self.button_font = button_font
        self.text_font = text_font

        self._after_id: None = None
        self._mouse_id: bool = False
        self._pressed_id: int = 0

        self.create_spinbox()
        self._map_spinbox()
        self.update_spinbox()
        
        self.up_button.bind("<ButtonPress-1>", lambda event: self._on_mouse_down(0))
        self.down_button.bind("<ButtonPress-1>", lambda event: self._on_mouse_down(1))
        self.up_button.bind("<ButtonRelease-1>", lambda event: self._on_mouse_up())
        self.down_button.bind("<ButtonRelease-1>", lambda event: self._on_mouse_up())

    def create_spinbox(self) -> None:
        self.spinbox = CTkFrame(self.master, 
                                width=self.width, 
                                height=self.height, 
                                border_width=self.border_width, 
                                corner_radius=self.corner_radius, 
                                border_color=self.border_color,
                                fg_color=self.fg_color)
        
        self.label = CTkLabel(self.spinbox, 
                              width=(self.width-(self.border_width*2))*0.8,
                              height=self.height-(self.border_width*2)-5,
                              corner_radius=self.corner_radius,
                              text_color=self.text_color,
                              font=self.text_font,
                              text="",
                              fg_color=self.fg_color,
                              bg_color=self.fg_color)
        
        self.button_frame = CTkFrame(self.spinbox, fg_color=self.fg_color, corner_radius=self.corner_radius)
        
        self.up_button = CTkButton(self.button_frame, 
                                   width=self.width-(self.width-(self.border_width*2))*0.8-self.border_width*2,
                                   height=self.height/2-self.border_width,
                                   text="+",
                                   image=self.button_up_image,
                                   corner_radius=self.corner_radius,
                                   border_width=0,
                                   font=self.button_font,
                                   fg_color=self.fg_color,
                                   hover_color=self.button_hover_color,
                                   round_height_to_even_numbers=False,
                                   round_width_to_even_numbers=False,
                                   state=self.state)
        
        self.down_button = CTkButton(self.button_frame, 
                                     width=self.width-(self.width-(self.border_width*2))*0.8-self.border_width*2,
                                     height=self.height/2-self.border_width,
                                     text="-",
                                     image=self.button_down_image,
                                     corner_radius=self.corner_radius,
                                     border_width=0,
                                     font=self.button_font,
                                     fg_color=self.fg_color,
                                     hover_color=self.button_hover_color,
                                     round_height_to_even_numbers=False,
                                     round_width_to_even_numbers=False,
                                     state=self.state)
        
        if self.button_up_image is not None:
            self.up_button.configure(text="")
        if self.button_down_image is not None:
            self.down_button.configure(text="")
                
    def _map_spinbox(self) -> None:
        """Maps the elements inside the spinbox widget"""
        self.label.pack(side="left", padx=(self.border_width,0))
        self.button_frame.pack(side="right", pady=self.border_width+5, padx=(0,self.border_width+5))
        self.up_button.pack(side="top")
        self.down_button.pack(side="bottom")
    
    def _unmap_spinbox(self) -> None:
        """Unmaps the elements inside the spinbox widget"""
        self.label.place_forget()
        self.up_button.place_forget()
        self.down_button.place_forget()

    def _on_mouse_down(self, button_id:int):
        self._mouse_id = True
        self._pressed_id = button_id
        self._move_spinbox_value()
    
    def _on_mouse_up(self):
        self._mouse_id = False
        self._pressed_id = None
        if self._after_id:
            self.master.after_cancel(self._after_id)
            self._after_id = None

    def _move_spinbox_value(self):
        if self._mouse_id:
            if self._pressed_id == 0: self.spinbox_up()
            else: self.spinbox_down()
            self._after_id = self.master.after(self.speed, self._move_spinbox_value)
        else: 
            self.spinbox_down()

    def update_spinbox(self) -> None:
        """Updates the spinbox value"""
        match self.text_placement:
            case "right": self.label.configure(text=f"{self.text} {self.value}{self.unit}")
            case "left": self.label.configure(text=f"{self.value}{self.unit} {self.text}")
            case _: raise TypeError
            
    def spinbox_up(self) -> None:
        """Increases the spinbox value by a given step. Stops at a given maximum or loops around. Can be binded to a key"""
        self.value += self.step

        if self.maximum != None:
            if self.value > self.maximum:
                if self.minimum != None: self.value = self.minimum
                else: self.value -= self.step

        self.update_spinbox()

    def spinbox_down(self) -> None:
        """Decreases the spinbox value by a given step. Stops at a given minimum or loops around. Can be binded to a key"""
        self.value -= self.step
        
        if self.minimum != None:
            if self.value < self.minimum:
                if self.maximum != None: self.value = self.maximum
                else: self.value += self.step

        self.update_spinbox()

    def get_value(self) -> int:
        """Gets the value of the spinbox"""
        return self.value
    
    def _configure(self):
        self.spinbox.configure(width=self.width, 
                               height=self.height, 
                               border_width=self.border_width, 
                               corner_radius=self.corner_radius, 
                               border_color=self.border_color)
        self.label.configure(width=(self.width-(self.border_width*2))*0.8,
                             height=self.height-(self.border_width*2)-1,
                             text_color=self.text_color,
                             font=self.text_font,
                             corner_radius=self.corner_radius,
                             fg_color=self.fg_color,
                             bg_color=self.fg_color)
        self.up_button.configure(width=self.width-(self.width-(self.border_width*2))*0.8-self.border_width*2,
                                 height=self.height/2-self.border_width,
                                 text="+",
                                 bg_color=self.fg_color,
                                 font=self.button_font,
                                 fg_color=self.fg_color,
                                 hover_color=self.button_hover_color,
                                 state=self.state)
        self.down_button.configure(width=self.width-(self.width-(self.border_width*2))*0.8-self.border_width*2,
                                   height=self.height/2-self.border_width,
                                   text="-",
                                   bg_color=self.fg_color,
                                   font=self.button_font,
                                   fg_color=self.fg_color,
                                   hover_color=self.button_hover_color,
                                   state=self.state)
        
        if self.button_up_image is not None:
            self.up_button.configure(text="")
        if self.button_down_image is not None:
            self.down_button.configure(text="")

    def configure(self, **kwargs) -> None:
        """Can configure various aspects of the spinbox, not including button image and size"""
        if "width" in kwargs: self.width = kwargs.pop("width")
        if "height" in kwargs: self.height = kwargs.pop("height")
        if "corner_radius" in kwargs: self.corner_radius = kwargs.pop("corner_radius")
        if "border_width" in kwargs: self.border_width = kwargs.pop("border_width")
        if "value" in kwargs: self.value = kwargs.pop("value")
        if "step" in kwargs: self.step = kwargs.pop("step")
        if "maximum" in kwargs: self.maximum = kwargs.pop("maximum")
        if "minimum" in kwargs: self.minimum = kwargs.pop("minimum")
        if "border_color" in kwargs: self.border_color = kwargs.pop("border_color")
        if "fg_color" in kwargs: self.fg_color = kwargs.pop("fg_color")
        if "text_color" in kwargs: self.text_color = kwargs.pop("text_color")
        if "text" in kwargs: self.text = kwargs.pop("text")
        if "text_placement" in kwargs: self.text_placement = kwargs.pop("text_placement")
        if "button_hover_color" in kwargs: self.button_hover_color = kwargs.pop("button_hover_color")
        if "unit" in kwargs: self.unit = kwargs.pop("unit")
        if "state" in kwargs: self.state = kwargs.pop("state")
        if "text_font" in kwargs: self.text_font = kwargs.pop("text_font")
        if "button_font" in kwargs: self.button_font = kwargs.pop("button_font")

        self._configure()
        self.update_spinbox()
        self._map_spinbox()

    def cget(self, attribute_name:str):
        if attribute_name == "parent_frame": return self.spinbox
        elif attribute_name == "width": return self.width
        elif attribute_name == "height": return self.height
        elif attribute_name == "corner_radius": return self.corner_radius
        elif attribute_name == "border_width": return self.border_width
        elif attribute_name == "step": return self.step
        elif attribute_name == "maximum": return self.maximum
        elif attribute_name == "minimum": return self.minimum
        elif attribute_name == "border_color": return self.border_color
        elif attribute_name == "fg_color": return self.fg_color
        elif attribute_name == "text_color": return self.text_color
        elif attribute_name == "text": return self.text
        elif attribute_name == "text_placement": return self.text_placement
        elif attribute_name == "button_hover_color": return self.button_hover_color
        elif attribute_name == "unit": return self.unit
        elif attribute_name == "state": return self.state
        elif attribute_name == "text_font": return self.text_color
        elif attribute_name == "button_font": return self.button_font
        
    def place(self, **kwargs) -> None:
        """
        Place a widget in the parent widget. Use as options:
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0 relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0 relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        bordermode="inside" or "outside" - whether to take border width of master widget into account
        """
        self._map_spinbox()
        self.spinbox.place(**kwargs)

    def place_forget(self) -> None:
        """ Unmap this widget. """
        self._unmap_spinbox()
        self.spinbox.place_forget()

    def pack(self, **kwargs) -> None:
        """
        Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self._map_spinbox()
        self.spinbox.pack(**kwargs)

    def pack_forget(self) -> None:
        """ Unmap this widget. """
        self._unmap_spinbox()
        self.spinbox.pack_forget()

    def grid(self, **kwargs) -> None:
        """
        Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this widget stick to the cell boundary
        """
        self._map_spinbox()
        self.spinbox.grid(**kwargs)

    def grid_forget(self) -> None:
        """ Unmap this widget. """
        self._unmap_spinbox()
        self.spinbox.grid_forget()

if __name__ == "__main__":
    root = CTk()
    root.geometry(f"500x500+{int(root.winfo_screenwidth()/2 - 250)}+{int(root.winfo_screenheight()/2.2 - 250)}")
    root.title("CTkSpinbox")

    frame = CTkFrame(root, width=300, height=300, fg_color="#202020", corner_radius=10)
    frame.pack(expand=True)

    spinbox = CTkSpinbox(frame, speed=100, maximum=100, minimum=0, corner_radius=10)
    spinbox.pack(pady=200)

    root.bind("<Up>", spinbox.spinbox_up)
    root.bind("<Down>", spinbox.spinbox_down)

    root.mainloop()