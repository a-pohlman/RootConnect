#import imaging modules (external)
from customtkinter import CTkImage 
from PIL import Image              
from tkinter import PhotoImage

#import internal modules
from tooling.__init__ import __image_dir__, __enable_pillow__

class Theme:
    color: dict = {"bg":"#202020", "bg_light":"#303030", "bg_dark":"#101010", "green":"#61A707", "orange":"#FF8B00"}
    text_color: dict = {"normal":"#FFFFFF", "disabled":"#7C7C7C"}

class Icons:  
    if __enable_pillow__:
        controller_image = CTkImage(Image.open(__image_dir__+"controller.png"), size=(45,45))
        close_image = CTkImage(Image.open(__image_dir__+"close.png"), size=(45,45))
        play_image = CTkImage(Image.open(__image_dir__+"play.png"), size=(45,45))
        configure_image = CTkImage(Image.open(__image_dir__+"configure.png"), size=(45,45))
        robot_image = CTkImage(Image.open(__image_dir__+"robot.png"), size=(45,45))
        text_image = CTkImage(Image.open(__image_dir__+"text.png"), size=(45,45))
        info_image = CTkImage(Image.open(__image_dir__+"info.png"), size=(45,45))
        view_more_image = CTkImage(Image.open(__image_dir__+"more.png"), size=(45,45))
        view_less_image = CTkImage(Image.open(__image_dir__+"less.png"), size=(45,45))
        root_logo_image = CTkImage(Image.open(__image_dir__+"root_logo.png"), size=(800,600))
        left_image = CTkImage(Image.open(__image_dir__+"left.png"), size=(100,100))
        right_image = CTkImage(Image.open(__image_dir__+"right.png"), size=(100,100))
        up_image = CTkImage(Image.open(__image_dir__+"up.png"), size=(100,100))
        down_image = CTkImage(Image.open(__image_dir__+"down.png"), size=(100,100))
        a_image = CTkImage(Image.open(__image_dir__+"a.png"), size=(80,80))
        b_image = CTkImage(Image.open(__image_dir__+"b.png"), size=(80,80))
        x_image = CTkImage(Image.open(__image_dir__+"x.png"), size=(80,80))
        y_image = CTkImage(Image.open(__image_dir__+"y.png"), size=(80,80)) 
    else:
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
        self.controller_image = PhotoImage(file=__image_dir__+"controller.png")
        self.close_image = PhotoImage(file=__image_dir__+"close.png")
        self.play_image = PhotoImage(file=__image_dir__+"play.png")
        self.configure_image = PhotoImage(file=__image_dir__+"configure.png")
        self.robot_image = PhotoImage(file=__image_dir__+"robot.png")
        self.text_image = PhotoImage(file=__image_dir__+"text.png")
        self.view_more_image = PhotoImage(file=__image_dir__+"more.png")
        self.view_less_image = PhotoImage(file=__image_dir__+"less.png")
        self.info_image = PhotoImage(file=__image_dir__+"info.png")
        self.root_logo_image = PhotoImage(file=__image_dir__+"root_logo.png")
        self.left_image = PhotoImage(file=__image_dir__+"left.png")
        self.right_image = PhotoImage(file=__image_dir__+"right.png")
        self.up_image = PhotoImage(file=__image_dir__+"up.png")
        self.down_image = PhotoImage(file=__image_dir__+"down.png")
        self.a_image = PhotoImage(file=__image_dir__+"a.png")
        self.b_image = PhotoImage(file=__image_dir__+"b.png")
        self.x_image = PhotoImage(file=__image_dir__+"x.png")
        self.y_image = PhotoImage(file=__image_dir__+"y.png")    
