from PySide6.QtGui import QColor, QPixmap

try: from internal.__init__ import __icon_dir__, __style_dir__
except: from __init__ import __icon_dir__, __style_dir__

class Theme:
    _bg: str = "rgb(32,32,32)"
    _light_bg: str = "rgb(42,42,42)"
    _bright_bg: str = "rgb(102,102,102)"
    _gr: str = "rgb(97,167,7)"
    _org: str = "rgb(255,139,0)"
    
    bg = QColor(32,32,32)
    light_bg = QColor(42,42,42)
    bright_bg = QColor(102,102,102)
    gr = QColor(97,167,7)
    org = QColor(255,139,0)
    light_shadow = QColor(110,110,110)
    dark_shadow = QColor(10,10,10)
    
    root_attributes: list[str] = ["--bg", "--gr", "--org", "--light_bg", "--bright_bg"]
    qss_attributes: dict = {"--bg":_bg,"--gr":_gr,"--org":_org,"--light_bg":_light_bg, "--bright_bg":_bright_bg}
    
    def get_stylesheet(stylesheet_name: str) -> None:
        stylesheet: str = ""
        with open(f"{__style_dir__}{stylesheet_name}", mode="r") as file:
            try: 
                for data in file:
                    for rt_att in Theme.root_attributes:
                        if rt_att in data:
                            data = data.replace(rt_att, Theme.qss_attributes[rt_att])
                    stylesheet += data
            except: pass
        return stylesheet
    
class Icons:
    add: QPixmap = ...
    play: QPixmap = ...
    help: QPixmap = ...
    settings: QPixmap = ...
    connectivity: QPixmap = ...
    clock: QPixmap = ...
    battery: QPixmap = ...
    menu: QPixmap = ...
    robot: QPixmap = ...
    exit: QPixmap = ...
    up: QPixmap = ...
    down: QPixmap = ...
    left: QPixmap = ...
    right: QPixmap = ...
    a: QPixmap = ...
    b: QPixmap = ...
    x: QPixmap = ...
    y: QPixmap = ...

    def initIcons():
        Icons.add = QPixmap(__icon_dir__+"add.png")
        Icons.play = QPixmap(__icon_dir__+"play.png")
        Icons.help = QPixmap(__icon_dir__+"help.png")
        Icons.settings = QPixmap(__icon_dir__+"settings.png")
        Icons.connectivity = QPixmap(__icon_dir__+"connectivity.png")
        Icons.clock = QPixmap(__icon_dir__+"clock.png")
        Icons.battery = QPixmap(__icon_dir__+"battery.png")
        Icons.menu = QPixmap(__icon_dir__+"menu.png")
        Icons.robot = QPixmap(__icon_dir__+"irobot_rt1.png")
        Icons.exit = QPixmap(__icon_dir__+"exit.png")
        Icons.up = QPixmap(__icon_dir__+"up.png")
        Icons.down = QPixmap(__icon_dir__+"down.png")
        Icons.left = QPixmap(__icon_dir__+"left.png")
        Icons.right = QPixmap(__icon_dir__+"right.png")
        Icons.a = QPixmap(__icon_dir__+"a.png")
        Icons.b = QPixmap(__icon_dir__+"b.png")
        Icons.x = QPixmap(__icon_dir__+"x.png")
        Icons.y = QPixmap(__icon_dir__+"y.png")