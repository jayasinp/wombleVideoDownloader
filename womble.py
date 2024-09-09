# New and improved with bear and wombat themes
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from threading import Thread
import yt_dlp

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Womble Video Downloader")
        self.root.geometry("400x500")  # Set the window size

        # Initialize themes
        self.themes = {
            "Wombat": {
                "bg_color": '#D2B48C',  # Pastel brown background
                "fg_color": '#4E342E',  # Dark brown text color
                "button_color": '#795548',  # Medium brown button color
                "progress_color": '#A1887F'  # Light brown for progress bar
            },
            "Bear": {
                "bg_color": '#3E2723',  # Dark brown background
                "fg_color": '#FFFFFF',  # White text color
                "button_color": '#5D4037',  # Darker brown button color
                "progress_color": '#8D6E63'  # Medium brown for progress bar
            }
        }

        self.current_theme = "Wombat"

        # Step Instructions
        self.step1_label = ttk.Label(root, text="First, paste in your URL:")
        self.step1_label.pack(pady=(20, 5))

        # URL Entry
        self.url_entry = ttk.Entry(root, width=40)
        self.url_entry.pack(pady=(0, 15))

        # Step Instructions
        self.step2_label = ttk.Label(root, text="Now select a burrow to stash your video:")
        self.step2_label.pack(pady=(10, 5))

        # Output Directory Button
        self.output_dir_button = ttk.Button(root, text="Select a Burrow", command=self.select_output_directory)
        self.output_dir_button.pack(pady=(0, 15))

        # Step Instructions
        self.step3_label = ttk.Label(root, text="Now unleash your wombat:")
        self.step3_label.pack(pady=(10, 5))

        # Download Button
        self.download_button = ttk.Button(root, text="🏴‍☠️ Pirate This Video 🏴‍☠️", command=self.start_download)
        self.download_button.pack(pady=(0, 15))

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient='horizontal', length=250, mode='determinate')
        self.progress.pack(pady=(10, 15))

        # Step Instructions
        self.step4_label = ttk.Label(root, text="See how the wombat is doing in the console below:")
        self.step4_label.pack(pady=(10, 5))

        # Scrolled Text for Output
        self.output_console = scrolledtext.ScrolledText(root, width=50, height=10, font=('TkDefaultFont', 10))
        self.output_console.pack(pady=(0, 20))

        # Theme Switcher Button
        self.theme_button = ttk.Button(root, text="Bear", command=self.toggle_theme)
        self.theme_button.pack(pady=(10, 15))

        # Initialize output directory
        self.output_directory = None

        # Apply the initial theme
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name):
        theme = self.themes[theme_name]
        bg_color = theme['bg_color']
        fg_color = theme['fg_color']
        button_color = theme['button_color']
        progress_color = theme['progress_color']

        # Set background color
        self.root.configure(bg=bg_color)

        # Apply style to widgets
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TLabel', font=('TkDefaultFont', 12), background=bg_color, foreground=fg_color)
        style.configure('TButton', font=('TkDefaultFont', 12), background=button_color, foreground='white')
        style.configure('TEntry', font=('TkDefaultFont', 12), padding=5)
        style.configure('TProgressbar', thickness=10, troughcolor=bg_color, background=progress_color)
        # Customize button hover color
        style.map('TButton',
            background=[('active', '#6A4F4B')],  # Darker brown hover color
            foreground=[('active', 'white')])
        # Update colors for widgets
        self.output_console.configure(bg=bg_color, fg=fg_color)

    def toggle_theme(self):
        # Toggle between themes
        if self.current_theme == "Wombat":
            self.current_theme = "Bear"
            self.theme_button.config(text="Wombat")
        else:
            self.current_theme = "Wombat"
            self.theme_button.config(text="Bear")
        self.apply_theme(self.current_theme)

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
