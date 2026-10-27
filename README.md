# Termux-python-scripts-11

## Shelby Transsion & X6852 Scripts

A collection of Python-based Android utilities by Shelby for Transsion devices and the Infinix Note 40 5G (X6852).

## Scripts

### 1. Shelby Transsion Script

A command-line utility for Infinix, TECNO, and itel devices. Includes firmware scanning, Fastboot device checks, reboot options, partition management, and flashing-related functions.

- **Source code:** [Shelby_Transsion_Script.py](https://github.com/gopinqth12/Termux-python-scripts-11/blob/main/Shelby_Transsion_Script.py)
- **Direct download:** [Download Python file](https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_Transsion_Script.py)

### 2. Shelby X6852 Script

A device-specific utility for the Infinix Note 40 5G (X6852). Includes firmware scanning, Fastboot device checks, reboot options, bootloader unlock commands, and flashing-related functions.

- **Source code:** [Shelby_X6852_Script.py](https://github.com/gopinqth12/Termux-python-scripts-11/blob/main/Shelby_X6852_Script.py)
- **Direct download:** [Download Python file](https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_X6852_Script.py)

## Setup Instructions

### Requirements

- Android with Termux, or a compatible Linux environment
- Python 3
- Android Platform Tools (`fastboot`) for Fastboot operations
- A suitable USB connection for connected-device operations

### 1. Update Termux packages

**Click to copy:**

```bash
pkg update && pkg upgrade
```

### 2. Install Python and curl

**Click to copy:**

```bash
pkg install python curl
```

### 3. Install Android platform tools

**Click to copy:**

```bash
pkg install android-tools
```

If `android-tools` is unavailable in your Termux repository, consult the current Termux package instructions. Installing Fastboot does not guarantee that every Android device can be controlled from Termux; USB access and device mode also matter.

## Download and Run

Choose the script you want. You do not need to download both.

### Option A — Shelby Transsion Script

**Download the script — click to copy:**

```bash
curl -fL -o Shelby_Transsion_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_Transsion_Script.py
```

**Run the script — click to copy:**

```bash
python Shelby_Transsion_Script.py
```

### Option B — Shelby X6852 Script

**Download the script — click to copy:**

```bash
curl -fL -o Shelby_X6852_Script.py https://raw.githubusercontent.com/gopinqth12/Termux-python-scripts-11/main/Shelby_X6852_Script.py
```

**Run the script — click to copy:**

```bash
python Shelby_X6852_Script.py
```

## Currently Supported Models & Keywords

The Transsion script uses these keywords to identify matching firmware ZIP filenames. **A keyword match does not confirm that a firmware package is compatible with a device.**

### Brands

`infinix`, `tecno`, `itel`, `transsion`, `spice`

### OS and firmware keywords

`xos`, `hios`, `stock`, `firmware`, `rom`, `official`

### Infinix

- **Hot series and related identifiers:** `x6833`, `x6835`, `x6816`, `x6818`, `x6819`, `x6820`, `x6823`, `x6826`, `x6827`, `x6829`, `x6830`
- **Note series and related identifiers:** `x6716`, `x6717`, `x6739`, `x6833b`, `x6833c`, `x6851`, `x6853`, `x6852`
- **Zero series:** `x6815`, `x6817`, `x6821`, `x6840`, `x6850`
- **GT series:** `x6871`, `x6873`, `x6885`, `x6893`
- **Smart series:** `x6525`, `x6526`, `x6527`, `x6528`, `x6529`, `x6531`, `x6515`, `x6516`, `x6517`, `x6518`
- **Older model identifiers:** `x680`, `x682`, `x683`, `x687`, `x688`, `x690`, `x692`, `x693`, `x694`, `x695`, `x696`

### TECNO

- **Camon series:** `ci6`, `ci7`, `ci8`, `cg7`, `cg8`, `ch6`, `ch7`, `ck6`, `ck7`, `ck8`, `cl6`, `cl7`, `cl8`, `cm6`, `cm7`, `cm8`
- **Spark series:** `kd6`, `kd7`, `ke5`, `ke6`, `ke7`, `ke8`, `kf6`, `kf7`, `kf8`, `kg5`, `kg6`, `kg7`, `kg8`, `kh5`, `kh6`, `kh7`, `kh8`, `ki5`, `ki6`, `ki7`, `ki8`, `kj5`, `kj6`, `kj7`, `kj8`
- **Pop series:** `lf7`, `lf8`, `lg6`, `lg7`, `lh6`, `lh7`, `lh8`, `li6`, `li7`, `li8`
- **Pova series:** `le6`, `le7`, `le8`, `lf6`

### itel

- **A series:** `a571`, `a572`, `a581`, `a582`, `a591`, `a601`, `a602`, `a661`, `a662`, `a671`, `a672`, `a681`
- **P series:** `p371`, `p372`, `p381`, `p382`, `p391`, `p401`, `p402`, `p551`, `p661`
- **S series:** `s661`, `s671`, `s681`

**Note:** The X6852-specific script uses a smaller keyword list focused on Infinix, X6852, Note 40, XOS, and stock firmware terms.

## Troubleshooting

### `fastboot: command not found`

**Click to copy:**

```bash
pkg install android-tools
```

### Check whether Fastboot detects a device

**Click to copy:**

```bash
fastboot devices
```

### Check Python version

**Click to copy:**

```bash
python --version
```

If no device appears, check the USB cable, device mode, USB permissions, and whether your environment supports access to the connected device.

## Important Safety Notice

- Verify the exact device model, region, build number, and firmware compatibility before flashing.
- Bootloader unlocking and partition flashing can erase user data or leave a device unable to boot.
- Do not flash a preloader, bootloader, or other partition unless you have confirmed the image is correct for the exact device and the procedure is appropriate.
- Keep a verified backup and a known-good firmware package available.
- Review the source code before running it.
- Do not assume a success message means every operation completed correctly. Stop if Fastboot reports an error.

## Credits

**Developer:** Shelby  
**Platform:** Python · Android · Termux · Fastboot  
**Repository:** [gopinqth12/Termux-python-scripts-11](https://github.com/gopinqth12/Termux-python-scripts-11)

## Disclaimer

This project is provided for educational and device-maintenance purposes. Use it at your own risk. The developer is not responsible for data loss, device damage, or failed flashing operations.
