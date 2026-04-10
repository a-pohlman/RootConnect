#import imaging modules (external)
from customtkinter import CTkImage 
from PIL import Image              
##from tkinter import PhotoImage => Linux Only

#import internal modules
from tooling.__base_dir__ import __base_dir__

class Theme:
    color: dict = {"bg":"#202020", "bg_light":"#303030", "bg_dark":"#101010", "green":"#61A707", "orange":"#FF8B00"}
    text_color: dict = {"normal":"#FFFFFF", "disabled":"#7C7C7C"}

class Icons:
    dir_to_images: str = __base_dir__+"\\tooling\\images\\"
    
    controller_image = CTkImage(Image.open(dir_to_images+"controller.png"), size=(45,45))
    close_image = CTkImage(Image.open(dir_to_images+"close.png"), size=(45,45))
    play_image = CTkImage(Image.open(dir_to_images+"play.png"), size=(45,45))
    configure_image = CTkImage(Image.open(dir_to_images+"configure.png"), size=(45,45))
    robot_image = CTkImage(Image.open(dir_to_images+"robot.png"), size=(45,45))
    text_image = CTkImage(Image.open(dir_to_images+"text.png"), size=(45,45))
    info_image = CTkImage(Image.open(dir_to_images+"info.png"), size=(45,45))
    view_more_image = CTkImage(Image.open(dir_to_images+"more.png"), size=(45,45))
    view_less_image = CTkImage(Image.open(dir_to_images+"less.png"), size=(45,45))
    root_logo_image = CTkImage(Image.open(dir_to_images+"root_logo.png"), size=(800,600))
    left_image = CTkImage(Image.open(dir_to_images+"left.png"), size=(100,100))
    right_image = CTkImage(Image.open(dir_to_images+"right.png"), size=(100,100))
    up_image = CTkImage(Image.open(dir_to_images+"up.png"), size=(100,100))
    down_image = CTkImage(Image.open(dir_to_images+"down.png"), size=(100,100))
    a_image = CTkImage(Image.open(dir_to_images+"a.png"), size=(80,80))
    b_image = CTkImage(Image.open(dir_to_images+"b.png"), size=(80,80))
    x_image = CTkImage(Image.open(dir_to_images+"x.png"), size=(80,80))
    y_image = CTkImage(Image.open(dir_to_images+"y.png"), size=(80,80)) 
    """
    controller_image: PhotoImage = ...
    close_image: PhotoImage = ...
    play_image: PhotoImage = ...
    configure_image: PhotoImage = ...
    robot_image: PhotoImage = ...
    text_image: PhotoImage = ...
    view_more_image: PhotoImage = ...
    view_less_image: PhotoImage = ...
    info_image: PhotoImage = ...
    root_logo_image: PhotoImage = ...
    left_image: PhotoImage = ...
    right_image: PhotoImage = ...
    up_image: PhotoImage = ...
    down_image: PhotoImage = ...
    a_image: PhotoImage = ...
    b_image: PhotoImage = ...
    x_image: PhotoImage = ...
    y_image: PhotoImage = ...

    def create_photo_images(self) -> None:
        self.controller_image = PhotoImage(file=self.dir_to_images+"controller.png")
        self.close_image = PhotoImage(file=self.dir_to_images+"close.png")
        self.play_image = PhotoImage(file=self.dir_to_images+"play.png")
        self.configure_image = PhotoImage(file=self.dir_to_images+"configure.png")
        self.robot_image = PhotoImage(file=self.dir_to_images+"robot.png")
        self.text_image = PhotoImage(file=self.dir_to_images+"text.png")
        self.view_more_image = PhotoImage(file=self.dir_to_images+"more.png")
        self.view_less_image = PhotoImage(file=self.dir_to_images+"less.png")
        self.info_image = PhotoImage(file=self.dir_to_images+"info.png")
        self.root_logo_image = PhotoImage(file=self.dir_to_images+"root_logo.png")
        self.left_image = PhotoImage(file=self.dir_to_images+"left.png")
        self.right_image = PhotoImage(file=self.dir_to_images+"right.png")
        self.up_image = PhotoImage(file=self.dir_to_images+"up.png")
        self.down_image = PhotoImage(file=self.dir_to_images+"down.png")
        self.a_image = PhotoImage(file=self.dir_to_images+"a.png")
        self.b_image = PhotoImage(file=self.dir_to_images+"b.png")
        self.x_image = PhotoImage(file=self.dir_to_images+"x.png")
        self.y_image = PhotoImage(file=self.dir_to_images+"y.png")    
    """