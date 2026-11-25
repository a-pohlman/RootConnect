<p align="center">
  <img src="repository_images/RootConnect_Logo_V2(transparent).png" alt="RootConnect Logo" width="500">
</p>

# RootConnect

## Description
An application that connects and can move around iRobot's Root 1 education robots with a unique, clean interface. The application is able to connect iRobot Root 1 robot to move the robot around a given surface. Also available is the feature of attaching an external Root Controller to move the robot around. Created by Aaron Pohlman for the Maker Engineering Project at Ohio Northern University.

<p align="center">
  <img src="repository_images/rootconnect_0.3.0_main.png" alt="RootConnect Logo" width="500">
</p>

<p align="center">
  <img src="repository_images/rootconnect_0.3.0_controller.png" alt="RootConnect Logo" width="500">
</p>


## Features 
- New user interface
- Allows the ability to change robots name
- Saves previous robots used
- Can use RootController and RootGyro controllers (BLE Only)
- Can run multiple robots at a time

## Requirements
- Bluetooth<sup>©</sup> Low Energy (BLE)
- Windows 10/11 or Python 3.12
- iRobot<sup>©</sup> Root 1

## Version 0.3.0 - Beta
Stable release as of **11/25/2026**. The project will be considered in the beta stages as not all elements of the app are fully developed as they could be. Some of the issues that may arise could be or not be solved in the future.

### Version Build
This version of the application was built using Tkinter and Customtkinter GUI libraries. View the list below to see what external python modules are needed to run the application (if using the python files)
- PySide6
- iRobot SDK
  - iRobot Robots (Root)
  - iRobot Bluetooth Backend
- Bleak Version 0.22.0

## Setup
### Windows 10 or 11 Specific
1. First, go to the releases tab and find the current release of the app
2. Download the 'root_connect_setup.exe' from the release tab
3. Find and run the setup wizard you just downloaded
4. Follow the steps on screen

The application should be where you set it to and a desktop icon will appear (if kept checked); your ready to start moving! In order to find the application folder, it will be in the Users > YOUR_USERNAME folder.

### Python Version
> [!CAUTION]
> Python 3.12 is strongly recommended as Python ^3.12 will not work for this application!

> [!IMPORTANT]
> Bleak module 0.22.0 was and should be used to communicate with the robot. Pip commands may not be able to install directly from a command line. It is recommended to download Bleak 0.22.0 from PyPl and build the wheel yourself using pip.

1. Install and setup a Python environment either on host or virtual
2. Install all of the required python modules
   ```
   pip install PySide6
   pip install bleak 0.22.2
   pip install irobot_edu_sdk
   ```
   
> [!TIP]
> Ensure that you have the correct versions for Python (3.12) and the Bleak Module (0.22.2)

3. Download or clone this repository
4. Navigate inside the cloned or downloaded folder, RootConnect > RootConnect_0.3.0 > bin
5. Use Python to run the file called: root_connect.pyw

## Issues?
You may report issues to the issues tab, however, like mentioned above, they may or may not be enacted on.
