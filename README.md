# F1 LED Leaderboard Display
***

![Travis (.org)](https://img.shields.io/travis/feram18/f1-led-leaderboard?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/feram18/f1-led-leaderboard?style=for-the-badge)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/feram18/f1-led-leaderboard?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/feram18/f1-led-leaderboard?style=for-the-badge)

[//]: # (![Libraries.io dependency status for GitHub repo]&#40;https://img.shields.io/librariesio/github/feram18/f1-led-leaderboard?style=for-the-badge&#41;)
[//]: # (![GitHub commits since latest release &#40;by date&#41; for a branch]&#40;https://img.shields.io/github/commits-since/feram18/f1-led-leaderboard/latest/dev?style=for-the-badge&#41;)

An LED Formula 1 leaderboard. Requires a Raspberry Pi, and a 64×32 LED board connected to the Raspberry Pi via the 
GPIO pins.

## Table of Contents
* [Features](#features)
* [Installation](#installation)
  * [Hardware](#hardware)
  * [Software](#software)
* [Usage](#usage)
  * [Flags](#flags)
  * [Execution](#execution)
  * [Debug](#debug)
* [Sources](#sources)
* [Disclaimer](#disclaimer)
* [License](#license)

## Features
- **Constructor Standings**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/constructor_standings.gif" /><br>)

[//]: # (</p>)
- **Driver Standings**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/driver_standings.gif" /><br>)

[//]: # (</p>)

- **Grand Prix Qualifying Results**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/qualifying_results.gif" /><br>)

[//]: # (</p>)

- **Grand Prix Results**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/last_gp.gif" /><br>)

[//]: # (</p>)

- **Next Grand Prix Information**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/next_gp.gif" /><br>)

[//]: # (</p>)

- **Schedule**

[//]: # (<p align="center">)

[//]: # (<img src="assets/img/demo/schedule.gif" /><br>)

[//]: # (</p>)

## Installation
### Hardware
Materials needed:
- [Raspberry Pi] (Only tested on 3B+ and 4B, but should work on other models)
- Adafruit RGB Matrix [HAT] or [Bonnet]
- [64×32] RGB LED matrix

### Software
**Pre-requisites**

- Git
- PIP
- Python 3.7+

```sh
sudo apt-get update
sudo apt-get install git python-pip
```

**Installation**

First, clone this repository. Using the `--recursive` flag will install the rgbmatrix binaries, which come from
hzeller's [rpi-rgb-led-matrix] library. This library is used to render the data onto the LED matrix.

```sh
git clone --recursive https://github.com/feram18/f1-led-leaderboard.git
cd f1-led-leaderboard
chmod +x install.sh
./install.sh
```

**Updating**

From the `f1-led-leaderboard` directory, run the update script. The script will also take care of updating all 
dependencies.

```sh
./update.sh
```

## Usage
Make sure the timezone on your Raspberry Pi is correct. It will often have it as London by default, but can be changed 
through the Raspberry Pi configuration tool.

```sh
sudo raspi-config
```

### Flags
The LED matrix is configured with the flags provided by the [rpi-rgb-led-matrix] library. 
More details on these flags/arguments can be found in the library's documentation.

```
--led-rows                Display panel rows. (Default: 32)
--led-cols                Display panel columns. (Default: 64)
--led-multiplexing        Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)
--led-row-addr-type       Addressing of rows: 0 = default; 1 = AB-addressed panels. (Default: 0)
--led-panel-type          Chipset of the panel. Supported panel types: FM6126A; FM6127.
--led-gpio-mapping        Name of GPIO mapping used: regular, adafruit-hat, adafruit-hat-pwm, compute-module. (Default: regular)
--led-slowdown-gpio       Slow down writing to GPIO. Needed for faster Pi's and/or slower panels. Range: 0..4. (Default: 1)
--led-chain               Number of daisy-chained boards. (Default: 1)
--led-parallel            For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)
--led-pixel-mapper        Apply pixel mappers: Mirror (Horizontal) = "Mirror:H"; Mirror (Vertical) = "Mirror:V"; Rotate (Degrees) = eg. "Rotate: 90"; U-Mapper = "U-mapper"
--led-brightness          Brightness level. Range: 1..100. (Default: 100)
--led-pwm-bits            Bits used for PWM. Range 1..11. (Default: 11)
--led-show-refresh        Shows the current refresh rate of the LED panel.
--led-limit-refresh       Limit refresh rate to this frequency in Hz. Useful to keep a constant refresh rate on loaded system. 0=no limit. (Default: 0)
--led-scan-mode           Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)
--led-pwm-lsb-nanosecond  Base time-unit for the on-time in the lowest significant bit in nanoseconds. (Default: 130)
--led-pwm-dither-bits     Time dithering of lower bits. (Default: 0)
--led-no-hardware-pulse   Don't use hardware pin-pulse generation.
--led-inverse             Switch if your matrix has inverse colors on.
--led-rgb-sequence        Switch if your matrix has led colors swapped. (Default: RGB)
```

### Execution
From the `f1-led-leaderboard` directory run the command

```sh
sudo python3 main.py --led-gpio-mapping="adafruit-hat" --led-slowdown-gpio=2 --led-brightness=60
```
You can modify and include [flags](#Flags) as necessary. Running as root is necessary in order for the matrix to render.

### Debug
If you are experiencing issues, you can turn on debug messages by running the software and appending the `--debug` flag 
to your execution command, logs are written to the `f1-led-leaderboard.log` file.

## Roadmap
- [X] Race Schedule
- [X] Grand Prix Results
- [X] Grand Prix Qualifying Results
- [ ] 128x64 Layout
- [ ] World Drivers' Championship Winner
- [ ] World Constructors' Championship Winner
- [ ] Customization options
  - [ ] Preferred Constructor Summary

## Sources
This project relies on the following:
- [Ergast API] to retrieve Formula 1 data.
- [rpi-rgb-led-matrix] library to make everything work with the LED matrix. It is included into this repository as a 
  submodule, so when cloning the repository it is necessary to use the `--recursive` flag.

## Limitations
Unfortunately the data provided by the [Ergast API] is not live, though it is updated a few hours after results are up.

## Disclaimer
This application is dependent on the [Ergast API] relaying accurate and updated data.

## License
GNU General Public License v3.0

[Raspberry Pi]: <https://www.raspberrypi.org/products/>
[64×32]: <https://www.adafruit.com/product/2279>
[HAT]: <https://www.adafruit.com/product/2345>
[Bonnet]: <https://www.adafruit.com/product/3211>
[Ergast API]: <http://ergast.com/mrd/>
[rpi-rgb-led-matrix]: <https://github.com/hzeller/rpi-rgb-led-matrix>