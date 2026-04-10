# Root Connect

## Description
An application that connects and can move around iRobot's Root 1 education robots with a unique, intuitive interface. Created for the Maker Engineering Project at Ohio Northern University, an application to connect iRobot Root 1 roomba to a software to move the roomba around a given surface. Also available is the feature of attaching an external controller to move the robot around.

## Features 
- Friendly user interface
- Easy to install on Windows
- Intutive design / No guides necessary
- Customizablilty in button functions functions
- Allows the abilty to change roombas namae
- Auto saving feature to remember previous choices
- Custom external controller allowed

> [!IMPORTANT]
> <em>Bluetooth is required for this application to work properly!</em>

## Version 0.2 - Beta
This version is of the lastest stable build to be released as of **04/10/2026**. The project will be considered in the beta stages as not all elements of the app are fully developed as they could be. Some of the issues that may arise could be or not be solve in the future. This application was built using Python 3.13 and works successfully

> [!WARNING]
> This project **may or may not** continue for future development

> [!CAUTION]
> Python 3.14 does NOT work with this application if downloading and running the Python Fork of the application

### Version Build
This verison of the application was built using Tkinter and Customtkinter GUI libaries. View the list below to see what external python modules are needed to run the application (if using the python fork)
- Tkinter / Tk (Linux Distributions)
- Customtkinter (All Systems)
- Pyserial (All Systems)
- iRobot SDK (All Systems)
  - Bleak
  - iRobot Robots (Root & Create3)
  - iRobot Bluetooth Backend

To download these, it's recommended to us pip by Python to download all of these external packages (Tkinter will not be shown). To do this, first, make sure that pip is installed:
```
python -m ensurepip --upgrade
```
OR 

```
python3 -m ensurepip --upgrade
```

Then, once pip has successfully installed, run:

```
pip install customtkinter pillow irobot_edu_sdk pyserial
```

### Bug Fixes
- None

### Change Log
- None

## Setup
### Windows 10 or 11 Fork
If downloading and using this application using the Windows systems fork, it has been made extremely easy. The only downside is that this version of the app is that it can not be changed at all. This is a precompiled build of the application. Some features are missing, like being able to connect to a Create3 Robot and needing a Root Connect controller. However, if just wanting to use the touch controls, this app should make it very easy and quick to do so. Let's start!
1. First, start off by downloading repository or cloning it.
2. After extracting the repository (if applicable), navigate into the folder and find the setup wizard provided named 'root_connect_setup.exe'
3. Run the setup wizard
4. Follow the steps on screen
> [!IMPORTANT]
> It is recommended to install the application NOT in the program folders, but rather in the downloads folder
> If not done, you may recieve errors with permission errors for trying to write to files.

That's it! The application should be where you set it to and a desktop icon will appear (if kept checked); your ready to start moving!

### Python Fork
The Python fork for this application is also straightforward. It is assumed that you have all the external modules necessary to run the application as shown in the version section. With this version of the fork, you have the ability to change how the application works and behaves if you have prior knowledge with coding in CustomTkinter and Tkinter. For this version, you only need to download or clone the git repository. Once down, you'll have access to the full python files to either modify or use the application using Python. If any forks are made of this application, please make reference back to this repository, thanks! 

> [!TIP]
> It is recommended to use a Python 3.13 enviornment

## Issues?
You may report issues to the issues tab, however, like mentioned above, they may or may not be enacted on. This project has a chance of not continuing future development; beware of that note, hence the Python Fork. 
