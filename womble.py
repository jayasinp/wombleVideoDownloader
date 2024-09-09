import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from threading import Thread
import yt_dlp

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Womble Video Downloader")

        # Step Instructions
        self.step1_label = ttk.Label(root, text="First, paste in your URL.")
        self.step1_label.pack(pady=5)

        # URL Entry
        self.url_label = ttk.Label(root, text="Video URL:")
        self.url_label.pack(pady=5)
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Step Instructions
        self.step2_label = ttk.Label(root, text="Now select a burrow to stash your video.")
        self.step2_label.pack(pady=5)

        # Output Directory Button
        self.output_dir_button = ttk.Button(root, text="Select a Burrow", command=self.select_output_directory)
        self.output_dir_button.pack(pady=5)

        # Step Instructions
        self.step3_label = ttk.Label(root, text="Now unleash your wombat.")
        self.step3_label.pack(pady=5)

        # Download Button
        self.download_button = ttk.Button(root, text="🏴‍☠️Pirate This Video🏴‍☠️", command=self.start_download)
        self.download_button.pack(pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=5)

        # Step Instructions
        self.step4_label = ttk.Label(root, text="See how the wombat is doing in the console below.")
        self.step4_label.pack(pady=5)

        # Scrolled Text for Output
        self.output_console = scrolledtext.ScrolledText(root, width=60, height=15)
        self.output_console.pack(pady=5)

        # Initialize output directory
        self.output_directory = None

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        self.output_console.insert(tk.END, f"Output directory selected: {self.output_directory}\n")
        self.output_console.yview(tk.END)

    def start_download(self):
        video_url = self.url_entry.get()
        if video_url and self.output_directory:
            Thread(target=self.download_video, args=(video_url,)).start()

    def download_video(self, url):
        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 1)
                percentage = (downloaded / total) * 100
                self.progress['value'] = percentage
            elif d['status'] == 'finished':
                self.progress['value'] = 100

        ydl_opts = {
            'format': 'best',
            'progress_hooks': [progress_hook],
            'outtmpl': f'{self.output_directory}/%(title)s.%(ext)s',
            'quiet': True,
            'noprogress': True,
            'logger': MyLogger(self.output_console)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

class MyLogger:
    def __init__(self, output_console):
        self.output_console = output_console

    def debug(self, msg):
        self.log(msg)

    def warning(self, msg):
        self.log(f"WARNING: {msg}")

    def error(self, msg):
        self.log(f"ERROR: {msg}")

    def log(self, msg):
        self.output_console.insert(tk.END, msg + "\n")
        self.output_console.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
