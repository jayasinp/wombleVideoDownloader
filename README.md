# Womble Video Downloader
- Works on youtube and twitter videos
- Download responsibly

## Setup
- Clone wombleVideoDownloader from https://github.com/jayasinp/wombleVideoDownloader
- Create a python virtual environment on your machine:
```bash
python -m venv venv
```
- Install the requirements:
```bash
pip install -r requirements.txt
```
- Build the app:
```bash
pyinstaller --noconfirm --onefile --windowed womble.py
```
- Open the app and start downloading videos.