import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from threading import Thread
from pathlib import Path
from tkinter.ttk import Progressbar

EXTENSIONS = {
    "Photos": {".jpeg", ".jpg", ".gif", ".pdf", ".png", ".heic", ".tiff", ".tif", ".bmp", ".webp", ".raw"},
    "Documents": {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".rtf", ".odt"},
    "Music": {".mp3", ".wav", ".flac", ".aac", ".wma", ".ogg", ".m4a"},
    "Videos": {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".mpeg"},
    "QuickBooks": {".qbw", ".qbb", ".qbm", ".qbo", ".des", ".qbr", ".qwc", ".qbstbl2.usa", ".qbx",
                    ".qba", ".qby", ".qbj", ".iif", ".nd", ".tlg", ".ecml", ".qbp", ".qsm", ".qss",
                    ".qst", ".qb2016", ".qb2019", ".mac.qbb"}
}

class FileCopyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Recovery Tool")
        self.root.geometry("660x700")
        self.root.resizable(False, False)

        self.source = tk.StringVar()
        self.destination = tk.StringVar()
        self.min_file_size_kb = tk.IntVar(value=50)
        self.cancel_requested = False
        self.file_type_mode = None

        self.build_menu()

    def build_menu(self):
        tk.Label(self.root, text="Select Operation", font=("Arial", 14)).pack(pady=10)

        btns = [
            ("Copy Photos", lambda: self.select_and_copy("Photos")),
            ("Copy Documents", lambda: self.select_and_copy("Documents")),
            ("Copy Music", lambda: self.select_and_copy("Music")),
            ("Copy Videos", lambda: self.select_and_copy("Videos")),
            ("Copy QB Files", lambda: self.select_and_copy("QuickBooks")),
            ("Copy User Data", self.copy_user_data)
        ]

        for label, cmd in btns:
            tk.Button(self.root, text=label, width=30, command=cmd).pack(pady=5)

        tk.Label(self.root, text="Minimum File Size to Copy (KB):").pack(pady=(10, 0))
        tk.Entry(self.root, textvariable=self.min_file_size_kb, width=10).pack()

        tk.Label(self.root, text="Progress:").pack(pady=(10, 0))
        self.progress = Progressbar(self.root, length=580, mode='determinate')
        self.progress.pack(pady=(0, 5))

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10), fg="blue")
        self.status_label.pack(pady=(0, 5))

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(0, 10))
        self.cancel_button = tk.Button(button_frame, text="Cancel Scan", command=self.cancel_scan_confirm, bg="red", fg="white")
        self.cancel_button.pack()
        self.cancel_button.config(state=tk.DISABLED)

        self.log_output = scrolledtext.ScrolledText(self.root, height=15, width=75, state='disabled')
        self.log_output.pack(padx=10, pady=5)

        tk.Label(self.root, text="Designed by Neverklear Technologies 2025", font=("Arial", 9), fg="gray").pack(pady=5)

    def log(self, message):
        self.log_output.configure(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)
        self.log_output.configure(state='disabled')
        with open("logfile.txt", "a", encoding="utf-8") as logf:
            logf.write(message + "\n")

    def cancel_scan_confirm(self):
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel the scan?"):
            self.cancel_requested = True
            self.status_label.config(text="Scan cancelled by user.")
            self.cancel_button.config(state=tk.DISABLED)

    def select_and_copy(self, file_type):
        self.cancel_requested = False
        self.file_type_mode = file_type
        source = filedialog.askdirectory(title="Select Drive to Scan")
        dest = filedialog.askdirectory(title="Select Destination Folder")
        if source and dest:
            self.source.set(source)
            self.destination.set(dest)
            self.start_thread()

    def copy_user_data(self):
        self.cancel_requested = False
        drive = filedialog.askdirectory(title="Select Windows Installation Drive (e.g., C:\\)")
        dest = filedialog.askdirectory(title="Select Destination Folder")
        if not drive or not dest:
            return
        user_root = os.path.join(drive, "Users")
        if not os.path.exists(user_root):
            messagebox.showerror("Error", "The selected drive does not appear to contain a Users folder.")
            return

        self.source.set(user_root)
        self.destination.set(dest)
        self.file_type_mode = "UserData"
        self.start_thread()

    def start_thread(self):
        self.progress["value"] = 0
        self.progress.update()
        self.status_label.config(text="Scanning and copying files...")
        self.cancel_button.config(state=tk.NORMAL)
        thread = Thread(target=self.perform_copy)
        thread.start()

    def perform_copy(self):
        source = self.source.get()
        dest = self.destination.get()
        min_size_bytes = self.min_file_size_kb.get() * 1024

        files_to_copy = []

        if self.file_type_mode == "UserData":
            for user in os.listdir(source):
                user_path = os.path.join(source, user)
                if os.path.isdir(user_path):
                    files_to_copy.extend([os.path.join(dp, f) for dp, dn, filenames in os.walk(user_path) for f in filenames])
        else:
            extensions = EXTENSIONS.get(self.file_type_mode, set())
            for root_dir, _, files in os.walk(source):
                for file in files:
                    if self.cancel_requested:
                        return
                    if any(file.lower().endswith(ext) for ext in extensions):
                        full_path = os.path.join(root_dir, file)
                        try:
                            if os.path.getsize(full_path) >= min_size_bytes:
                                files_to_copy.append(full_path)
                        except Exception as e:
                            self.log(f"✘ Error reading size of {full_path}: {e}")

        total_files = len(files_to_copy)
        self.progress["maximum"] = total_files
        copied = 0
        failed = 0

        for full_path in files_to_copy:
            if self.cancel_requested:
                self.log("🚫 Scan cancelled by user.")
                break
            try:
                relative_path = os.path.relpath(full_path, source)
                dest_path = os.path.join(dest, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(full_path, dest_path)
                self.log(f"✔ Copied: {relative_path}")
                copied += 1
            except Exception as e:
                self.log(f"✘ Failed: {full_path} ({e})")
                failed += 1
            self.progress["value"] += 1
            self.progress.update()

        self.status_label.config(text=f"✅ Done: {copied} copied, {failed} failed, {total_files} total.")
        self.cancel_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyTool(root)
    root.mainloop()
