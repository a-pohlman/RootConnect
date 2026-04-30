# Root Connect

## Description
An application that connects and can move around iRobot's Root 1 education robots with a unique, intuitive interface. Created for the Maker Engineering Project at Ohio Northern University, an application to connect iRobot Root 1 robot to a software to move the robot around a given surface. Also available is the feature of attaching an external controller to move the robot around.

## Features 
- Friendly user interface
- Easy to install on Windows
- Intuitive design / No guides necessary
- Customizability in button functions functions
- Allows the ability to change robots name
- Auto saving feature to remember previous choices
- Custom external controller allowed

> [!IMPORTANT]
> <em>Bluetooth is required for this application to work properly!</em>

## Version 0.2.1 - Beta
This version is of the latest stable build to be released as of **04/15/2026**. The project will be considered in the beta stages as not all elements of the app are fully developed as they could be. Some of the issues that may arise could be or not be solve in the future. This application was built using Python 3.13 and works successfully

> [!WARNING]
> This project **may or may not** continue for future development

> [!CAUTION]
> Python 3.14 does NOT work with this application if downloading and running the Python files of the application

> [!CAUTION]
> You must have a Bluetooth antenna to use on your computer! Otherwise, the app will not be able to connect with a Bluetooth controller, or with the iRobot Root 1 robots

### Version Build
This version of the application was built using Tkinter and Customtkinter GUI libraries. View the list below to see what external python modules are needed to run the application (if using the python files)
- Tkinter / Tk (Linux Distributions)
- Customtkinter (All Systems)
- Pyserial (All Systems)
- iRobot SDK (All Systems)
  - Bleak
  - iRobot Robots (Root & Create3)
  - iRobot Bluetooth Backend

To download these, it's recommended to use pip by Python to download all of these external packages. However, Tkinter will not be shown, so look up how to install tkinter for your linux distribution or version of macOS (it should already come with Windows compiled version of Python). For the rest of the modules, first, make sure that pip is installed:
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
- Fixed controller not disconnecting on app closing
- Fixed not being able to find controller

### Change Log (04/15/2026)
- App now resets after closing controls window without having to use 'exit connection' button
- Added a way to detect system for path management (mainly for python version)
- Cleaned code and files

> [!IMPORTANT]
> A new setup wizard and compiled version has been made for Window users to use to reflect these changes.

## Setup
### Windows 10 or 11 Specific
If downloading and using this application for Windows, it has been made extremely easy. The only downside is that version of the app can not be changed at all. This is a precompiled build of the application. Some features are missing, like being able to connect to a Create3 Robot and needing a Root Connect controller. However, if just wanting to use the touch controls, this app should make it very easy and quick to do so. Let's start!
1. First, go to the releases tab and find the current release of the app
2. Download the 'root_connect_setup.exe' from the release tab
3. Find and run the setup wizard you just downloaded
4. Follow the steps on screen
> [!IMPORTANT]
> It is recommended to install the application NOT in the program folders, but somewhere in the users folder.
> If not done, you may recieve errors with permission errors for trying to write to files.

That's it! The application should be where you set it to and a desktop icon will appear (if kept checked); your ready to start moving!

### Python Version
The Python Version for this application is also straightforward. Simply clone the repository and you should be able to run the python application in an appropriate location. It is assumed that you have all the external modules necessary to run the application as shown in the version section. You should be using the file named run.pyw to run the application as this is what allows it to restart and properly save, unlike main.pyw

> [!TIP]
> If the run.pyw file doesn't do anything or returns an error, you may have to configure it just a little bit. Open the file in a IDE or text editor, and using the comments, uncomment the correct conditional and comment the other one (or delete it).
> If you need to configure other app defaults for any reason, you can find them in tooling >> \_\_init__.py

With this version, you have the ability to change how the application works and behaves if you have prior knowledge with coding in CustomTkinter and Tkinter. For this version, you only need to download or clone the git repository. Once done, you'll have access to the full python files to either modify or use the application using Python. If any forks are made of this application, please make reference back to this repository, thanks! 

> [!TIP]
> It is recommended to use a Python 3.13 environment, as mentioned earlier, Python 3.14 is NOT compatible in its current state.

## Issues?
You may report issues to the issues tab, however, like mentioned above, they may or may not be enacted on. This project has a chance of not continuing future development.
