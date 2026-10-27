# Termux-python-scripts-11
Shelby Transsion & X6852 Scripts

A collection of Python-based Android utilities by Shelby, designed for Transsion devices and the Infinix Note 40 5G (X6852).

Scripts

1. Shelby Transsion Script

A command-line utility designed for Infinix, TECNO, and itel devices, with firmware scanning, Fastboot device checks, reboot options, partition management, and flashing-related functions.

- Source code: https://github.com/gopinqth12/Termux-python-scripts-11/blob/main/Shelby_Transsion_Script.py
- Direct download: https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_Transsion_Script.py

2. Shelby X6852 Script

A device-specific utility for the Infinix Note 40 5G (X6852), with firmware scanning, Fastboot device checks, reboot options, bootloader unlock commands, and flashing-related functions.

- Source code: https://github.com/gopinqth12/Termux-python-scripts-11/blob/main/Shelby_X6852_Script.py
- Direct download: https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_X6852_Script.py

Setup Instructions

Requirements

- Android device with Termux, or another compatible Linux environment
- Python 3
- Android platform-tools ("fastboot") for Fastboot operations
- USB OTG or a suitable USB connection when working with a connected device

Install dependencies

pkg update && pkg upgrade
pkg install python curl

Install Fastboot if a compatible package is available in your Termux repositories:

pkg install android-tools

Download and run — Transsion Script

curl -fL -o Shelby_Transsion_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_Transsion_Script.py
python Shelby_Transsion_Script.py

Download and run — X6852 Script

curl -fL -o Shelby_X6852_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_X6852_Script.py
python Shelby_X6852_Script.py

Important Safety Notice

- Verify firmware compatibility with your exact device model and region before flashing.
- Bootloader unlocking and partition flashing can erase data or render a device unbootable.
- Keep a verified backup and use the correct firmware images.
- Review the source code before running it. Successful command execution does not necessarily mean every partition was flashed successfully.

Credits

Developer: Shelby
Platform: Python · Android · Termux · Fastboot
Repository: https://github.com/gopinqth12/Termux-python-scripts-11
