README.md
Beatbox - Terminal Music Tool

**Beatbox** is a terminal-based music player made using Python, designed to stream and download songs directly from YouTube — right inside Termux!

## Features

- Stream music from YouTube (audio only)
- Download songs to your device
- Manage offline songs easily
- Like songs and create your own favorites list
- Loop and shuffle mode
- Smooth terminal UI with clean controls

## How to Use

1. **Clone the repository**

git clone https://github.com/aexy-boi/beatbox
cd beatbox

2. **Install the required Python libraries**
'''python
pip install -r requirements.txt
___

3. **Run Beatbox**

python beatbox.py

4. **Follow on-screen options to play, download, like, or manage songs.**

## Requirements

- Termux or any terminal with Python 3
- `yt-dlp`, `aria2c` (for fast downloads)
- Python modules: `pytube`, `rich`, `httpx`, etc.

## Notes

- Make sure you have internet connection for streaming/downloading.
- Downloads are saved to `~/storage/shared/Beatbox/` and should appear in your gallery.

## Credits

Made with love by [aexy-boi](https://github.com/aexy-boi)
