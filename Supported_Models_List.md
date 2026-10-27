# Shelby Transsion & X6852 Scripts

Python-based Android utilities for Transsion devices, including Infinix, TECNO, and itel. Includes firmware scanning, Fastboot checks, reboot options, and flashing-related functions.

## Features

- Transsion firmware ZIP scanning
- Supported-model keyword detection
- Fastboot device checking
- Reboot options
- Bootloader unlock commands
- Firmware flashing and partition operations
- Dedicated Infinix Note 40 5G (X6852) script

## Scripts

| Script | Target |
|---|---|
| `Shelby_Transsion_Script.py` | Transsion device firmware scanning |
| `Shelby_X6852_Script.py` | Infinix Note 40 5G (X6852) |

## Setup

### Requirements

- Android with Termux, or a compatible Linux environment
- Python 3
- Android Platform Tools (`fastboot`) for Fastboot operations

### Install dependencies

```bash
pkg update && pkg upgrade
pkg install python curl android-tools
```

### Run the Transsion script

```bash
curl -fL -o Shelby_Transsion_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_Transsion_Script.py
python Shelby_Transsion_Script.py
```

### Run the X6852 script

```bash
curl -fL -o Shelby_X6852_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_X6852_Script.py
python Shelby_X6852_Script.py
```

## Currently Supported Models & Keywords

The Transsion script uses the following brand, firmware, and model keywords to identify matching firmware ZIP files. **Keyword detection does not guarantee that every listed model supports every flashing operation.**

### Brands

- Infinix
- TECNO
- itel
- Transsion
- Spice

### OS and firmware keywords

- XOS
- HiOS
- Stock
- Firmware
- ROM
- Official

### Infinix

**Hot series and related model identifiers**  
`X6833`, `X6835`, `X6816`, `X6818`, `X6819`, `X6820`, `X6823`, `X6826`, `X6827`, `X6829`, `X6830`

**Note series and related model identifiers**  
`X6716`, `X6717`, `X6739`, `X6833B`, `X6833C`, `X6851`, `X6853`, `X6852`

**Zero series**  
`X6815`, `X6817`, `X6821`, `X6840`, `X6850`

**GT series**  
`X6871`, `X6873`, `X6885`, `X6893`

**Smart series**  
`X6525`, `X6526`, `X6527`, `X6528`, `X6529`, `X6531`, `X6515`, `X6516`, `X6517`, `X6518`

**Older model identifiers**  
`X680`, `X682`, `X683`, `X687`, `X688`, `X690`, `X692`, `X693`, `X694`, `X695`, `X696`

### TECNO

**Camon series**  
`CI6`, `CI7`, `CI8`, `CG7`, `CG8`, `CH6`, `CH7`, `CK6`, `CK7`, `CK8`, `CL6`, `CL7`, `CL8`, `CM6`, `CM7`, `CM8`

**Spark series**  
`KD6`, `KD7`, `KE5`, `KE6`, `KE7`, `KE8`, `KF6`, `KF7`, `KF8`, `KG5`, `KG6`, `KG7`, `KG8`, `KH5`, `KH6`, `KH7`, `KH8`, `KI5`, `KI6`, `KI7`, `KI8`, `KJ5`, `KJ6`, `KJ7`, `KJ8`

**Pop series**  
`LF7`, `LF8`, `LG6`, `LG7`, `LH6`, `LH7`, `LH8`, `LI6`, `LI7`, `LI8`

**Pova series**  
`LE6`, `LE7`, `LE8`, `LF6`

### itel

**A series**  
`A571`, `A572`, `A581`, `A582`, `A591`, `A601`, `A602`, `A661`, `A662`, `A671`, `A672`, `A681`

**P series**  
`P371`, `P372`, `P381`, `P382`, `P391`, `P401`, `P402`, `P551`, `P661`

**S series**  
`S661`, `S671`, `S681`

## Safety Notice

- Verify the exact device model, region, firmware build, and partition compatibility before flashing.
- Bootloader unlocking and flashing may erase user data.
- Incorrect partition images can cause boot failure or permanently damage a device.
- Keep a verified backup and use reliable firmware sources.
- Review the source code before running any script.

## Disclaimer

This project is provided for educational and device-maintenance purposes. Use it at your own risk. The developer is not responsible for data loss, device damage, or failed flashing operations.

## Developer

**Shelby**

Repository: https://github.com/gopinqth12/Termux-python-scripts-11
