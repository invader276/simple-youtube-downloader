# Simple YouTube Downloader

A user-friendly desktop application for downloading YouTube videos and audio. It features a modern interface built with `customtkinter` and leverages `yt-dlp` for efficient downloads. The app offers a clean, customizable interface with adjustable settings for colors, fonts, and window dimensions.


![Screenshot](https://raw.githubusercontent.com/invader276/simple-youtube-downloader/2c59e1a5a6afdd738d3bd9f8157d82ecf2a48c30/assets/Screenshot.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Download YouTube videos in multiple formats (e.g., mp4, mp3/m4a).
- Clean and User-friendly GUI built with `customtkinter`.
- Ability to select the download directory.
- Customizable appearance for the GUI.

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/invader276/simple-youtube-downloader.git
   cd simple-youtube-downloader
   ```

2. **Install dependencies**:
   - Ensure you have Python 3.9 or higher installed. Download it from [here](https://www.python.org/downloads/).
   - Install the required Python packages:
     ```
     pip install -r requirements.txt
     ```

3. **Ensure you have an ffmpeg binary in the `ffmpeg` folder**:
   - Download it from the [official FFmpeg page](https://www.ffmpeg.org/download.html) or use the one provided with the source code.

## Usage

1. **Run the application**:
   ```
   python main.py
   ```

2. **Using the GUI**:
   - Enter the URL of the YouTube video you wish to download.
   - Select the download directory.
   - Choose whether to download audio or video.
   - Click the Download button to start the download.

## Configuration

The application uses a `config.json` file to store user preferences. You can modify this file to set theme colors, fonts, and window properties such as dimensions and size.

## Dependencies

- Python 3.9 or higher
- `yt_dlp`
- `customtkinter`
- `tkinter-tooltip` (`tktooltip`)
- `ffmpeg` (for processing video/audio files)

## Known Issues

- **Font Availability**: The application uses the `Inter` font from Google. It does not currently check for the font's presence or attempt to install it, which may result in a less polished visual experience on systems where the font is missing. Future updates may address this by incorporating a font fallback mechanism or bundling the font with the application.

- **File Availability**: The application does not currently verify the existence of critical files, such as `ffmpeg.exe` or configuration files, in their expected locations. This lack of validation can lead to runtime errors or malfunction if these files are missing or incorrectly placed. An enhancement to include checks for the presence and correct path of these files is planned for future updates to ensure a more robust user experience.

- **Quality Selection**: As of now, the application currently downloads the best available quality video or audio for the given YouTube video. Users do not have the option to select between different resolutions or bitrates. This design ensures that the highest quality content is downloaded by default, but future versions may include options for quality selection to provide users with more control over their downloads.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. Your input is greatly appreciated.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [tktooltip](https://github.com/gnikit/tkinter-tooltip): A tooltip implementation for tkinter.
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter): A customizable tkinter GUI library.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): A Python library for downloading YouTube videos and audio.
- [ffmpeg](https://ffmpeg.org): A cross-platform video and audio processing tool.
