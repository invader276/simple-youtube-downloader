import os
import re
import threading
from json import load

import customtkinter as ctk
import yt_dlp


class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self, colors, properties):
        super().__init__()
        self.colors = colors
        self.properties = properties
        del colors, properties
        self.path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.title("YouTube Downloader")
        self.iconbitmap(self.properties["windowIconLocation"])
        self.configure(fg_color=self.colors["windowBackground"])
        self.geometry(self._calculate_geometry())
        self.minsize(*self.properties["windowDimensions"])
        self.resizable(*self.properties["windowResizable"])
        self.font = ctk.CTkFont(
            family=self.properties["font"], size=self.properties["fontSize"]
        )
        self.onlyAudio = ctk.StringVar(value="off")
        self.is_downloading = False
        self._create_widgets()
        self._pack_widgets()

    def _calculate_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width, window_height = self.properties["windowDimensions"]
        xspawn = (screen_width - window_width) // 2
        yspawn = (screen_height - window_height) // 2
        return f"{window_width}x{window_height}+{xspawn}+{yspawn}"

    def _create_widgets(self):
        self.row1 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.row2 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.row3 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.row4 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.row5 = ctk.CTkFrame(master=self, fg_color="transparent")
        self.entryLink = ctk.CTkEntry(
            master=self.row1,
            width=700,
            height=50,
            font=self.font,
            justify="center",
            border_width=self.properties["borderWidth"],
            border_color=self.colors["labelBorderColor"],
            corner_radius=self.properties["cornerRadius"],
            placeholder_text="Enter YouTube video link here",
            placeholder_text_color=self.colors["placeholderTextColor"],
            fg_color=self.colors["labelBackground"],
            text_color=self.colors["labelTextColor"],
        )
        self.entryBrowse = ctk.CTkEntry(
            master=self.row2,
            width=560,
            height=40,
            font=self.font,
            justify="center",
            corner_radius=self.properties["cornerRadius"],
            border_width=self.properties["borderWidth"],
            border_color=self.colors["labelBorderColor"],
            placeholder_text=self.path,
            placeholder_text_color=self.colors["placeholderTextColor"],
            fg_color=self.colors["labelBackground"],
            text_color=self.colors["labelTextColor"],
        )
        self.entryBrowse.configure(state="readonly")
        self.buttonBrowse = ctk.CTkButton(
            master=self.row2,
            text="Browse",
            width=120,
            height=40,
            font=self.font,
            corner_radius=self.properties["cornerRadius"],
            border_width=self.properties["borderWidth"],
            border_color=self.colors["labelBorderColor"],
            fg_color=self.colors["buttonBackground"],
            text_color=self.colors["buttonTextColor"],
            hover_color=self.colors["buttonBorderColor"],
            command=self.browse,
        )
        self.checkboxAudio = ctk.CTkCheckBox(
            master=self.row3,
            text="Audio only",
            font=self.font,
            checkbox_width=28,
            checkbox_height=28,
            onvalue="on",
            offvalue="off",
            variable=self.onlyAudio,
            text_color=self.colors["labelTextColor"],
            fg_color=self.colors["labelBackground"],
            hover_color=self.colors["labelBorderColor"],
        )
        self.labelStatus = ctk.CTkLabel(
            master=self.row4,
            text="",
            font=ctk.CTkFont(family="Inter Bold", size=16),
            text_color=self.colors["statusTextSuccess"],
        )
        self.buttonDownload = ctk.CTkButton(
            master=self.row5,
            text="Download",
            width=200,
            height=40,
            font=self.font,
            corner_radius=self.properties["cornerRadius"],
            border_width=self.properties["borderWidth"],
            border_color=self.colors["labelBorderColor"],
            fg_color=self.colors["buttonBackground"],
            text_color=self.colors["buttonTextColor"],
            hover_color=self.colors["buttonBorderColor"],
            command=self.download,
        )

    def _pack_widgets(self):
        self.row1.pack()
        self.row2.pack()
        self.row3.pack()
        self.row4.pack()
        self.row5.pack()
        self.entryLink.pack(pady=36)
        self.entryBrowse.pack(pady=24, side=ctk.LEFT, anchor="e", padx=10)
        self.buttonBrowse.pack(pady=24, side=ctk.LEFT, anchor="w", padx=10)
        self.checkboxAudio.pack(pady=24)
        self.labelStatus.pack(pady=24)
        self.buttonDownload.pack(pady=37, side=ctk.BOTTOM)

    def split_string(self, text, char_limit):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= char_limit:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)

    def browse(self):
        fileDialogPath = ctk.filedialog.askdirectory()
        self.path = fileDialogPath if fileDialogPath else self.path
        self.insertText(self.entryBrowse, self.path)

    def insertText(self, widget, text):
        limit = 40
        if len(text) > limit:
            text = text[:limit] + "..."
        elif text == "":
            return
        widget.configure(state="normal")
        widget.delete(0, ctk.END)
        widget.insert(0, text)
        widget.configure(state="readonly")

    def showStatus(self, outcome, text):
        self.labelStatus.configure(text_color=self.colors[f"statusText{outcome}"])
        self.labelStatus.configure(text=self.split_string(text, 90))

    def hideStatus(self):
        self.labelStatus.configure(text="")

    def progress_hook(self, d):
        if d["status"] == "downloading":
            percentage = d.get("_percent_str", "0.00%")
            match = re.search(r"(\d+\.\d+)%", percentage)
            percentage_clean = match.group(1) + "%" if match else "0.00%"
            self.labelStatus.configure(text=f"Downloading... {percentage_clean}")
            self.update()

    def _download_thread(self):
        self.buttonDownload.configure(state="disabled")
        self.hideStatus()
        self.update()
        url = self.entryLink.get()
        if url:
            if "youtube" in url or "youtu.be" in url:
                self.showStatus("Success", "Downloading...")
                self.update()
                output_path = self.path
                audio_only = self.onlyAudio.get() == "on"
                ffmpegPath = os.path.join(
                    os.path.curdir, self.properties["ffmpegLocation"]
                )
                ydl_opts = {
                    "format": (
                        "bestaudio/best" if audio_only else "bestvideo+bestaudio/best"
                    ),
                    "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                    "ffmpeg_location": ffmpegPath,
                    "continuedl": True,
                    "noplaylist": True,
                    "nooverwrites": False,
                    "quiet": False,
                    "progress_hooks": [self.progress_hook],
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(url, download=True)
                    video_title = info_dict.get("title", "Unknown Title")
                    self.showStatus("Success", f"Downloaded {video_title}")
                except Exception as e:
                    self.showStatus("Failure", f"An error occurred: {str(e)}")
                finally:
                    self.buttonDownload.configure(state="normal")
                return
        self.showStatus("Failure", "Please enter a valid YouTube link")
        self.buttonDownload.configure(state="normal")

    def download(self):
        if not self.is_downloading:
            self.is_downloading = True
            threading.Thread(target=self._download_thread, daemon=True).start()
            self.is_downloading = False


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = load(f)
        colors = config["colors"]
        properties = config["properties"]
    app = YouTubeDownloaderApp(colors, properties)
    app.mainloop()
