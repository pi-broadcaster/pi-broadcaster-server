# pi-broadcaster

**Broadcast platform powered by Raspberry Pi. YouTube supported.**

<!-- old
![Python Version](https://img.shields.io/pypi/pyversions/paramiko?style=flat)
![Platform](https://img.shields.io/powershellgallery/p/PackageManagement)
![License](https://img.shields.io/github/license/pham-tuyen/pi-music)

This [repository](https://github.com/pham-tuyen/pi-broadcaster) and [pim-gui](https://github.com/doan08/pim-gui) are a product. This [repository](https://github.com/pham-tuyen/pi-broadcaster) is developing for the hardware [(Raspberry PI)](https://raspberrypi.com) and [pim-gui](https://github.com/doan08/pim-gui) is developing for the software (client).
-->
## Requirements
##### Internet required
For `/server/`:
```
yt-dlp
mpg123
Python 3.7+
gTTS
```
For `/client/`:
```
pysftp
paramiko
Python 3.9+
```
## Installation
Download this repo, or clone this repo:
```
git clone https://github.com/pi-broadcaster/pi-broadcaster.git
```
Copy `/client/` into your computer, `/server/` into your RPi.

Run these commands in your RPi, in `/server`:
```
sudo apt update
sudo apt install mpg123
pip install -r requirements.txt
```
Run these commands in your computer:
```
pip install -r requirements.txt
```
Enable SSH in your RPi and set up `.bashrc` to automatically run `main.py` in startup.
## Run
Reboot your RPi, and run 
```
python main.pyw
```
in your computer.
## Usage
Follow the guide in your app.
## FAQs
