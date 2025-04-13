import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from threading import Thread
from pathlib import Path
from tkinter.ttk import Progressbar

PHOTO_EXTENSIONS = {
    ".jpeg", ".jpg", ".gif", ".pdf", ".png",
    ".heic", ".tiff", ".tif", ".bmp", ".webp", ".raw"
}

class FileScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drive Scanner and Photo Copier")
        self.root.geometry("620x570")
        self.root.resizable(False, False)

        self.source_drive = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.min_file_size_kb = tk.IntVar(value=50)
        self.cancel_requested = False

        self.create_widgets()

    def create_widgets(self):
        # Source drive dropdown
        tk.Label(self.root, text="Select Drive to Scan:").pack(pady=(10, 0))
        drives = self.get_available_drives()
        self.source_drive.set(drives[0] if drives else "")
        tk.OptionMenu(self.root, self.source_drive, *drives).pack()

        # Destination folder picker
        tk.Label(self.root, text="Select Destination Folder:").pack(pady=(10, 0))
        entry_frame = tk.Frame(self.root)
        entry_frame.pack()
        tk.Entry(entry_frame, textvariable=self.destination_folder, width=50).pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(entry_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Minimum file size filter
        tk.Label(self.root, text="Minimum File Size to Copy (KB):").pack(pady=(10, 0))
        tk.Entry(self.root, textvariable=self.min_file_size_kb, width=10).pack()

        # Progress bar
        tk.Label(self.root, text="Progress:").pack(pady=(10, 0))
        self.progress = Progressbar(self.root, length=580, mode='determinate')
        self.progress.pack(pady=(0, 10))

        # Start and Cancel buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Start Scan", command=self.start_scan_thread).pack(side=tk.LEFT, padx=10)
        self.cancel_button = tk.Button(button_frame, text="Cancel Scan", command=self.cancel_scan)
        self.cancel_button.pack(side=tk.LEFT)
        self.cancel_button.config(state=tk.DISABLED)

        # Log output
        self.log_output = scrolledtext.ScrolledText(self.root, height=15, width=72, state='disabled')
        self.log_output.pack(padx=10, pady=10)

        # Footer
        tk.Label(self.root, text="Designed by Neverklear Technologies 2025", font=("Arial", 9), fg="gray").pack(pady=(5, 5))

    def get_available_drives(self):
        drives = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if os.path.exists(f"{letter}:\\"):
                drives.append(f"{letter}:\\")
        return drives

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder.set(folder)

    def start_scan_thread(self):
        self.cancel_requested = False
        self.cancel_button.config(state=tk.NORMAL)
        thread = Thread(target=self.scan_and_copy_files)
        thread.start()

    def cancel_scan(self):
        self.cancel_requested = True
        self.cancel_button.config(state=tk.DISABLED)

    def log(self, message):
        self.log_output.configure(state='normal')
        self.log_output.insert(tk.END, message + "\n")
        self.log_output.see(tk.END)
        self.log_output.configure(state='disabled')

    def scan_and_copy_files(self):
        source = self.source_drive.get()
        dest = self.destination_folder.get()
        min_size_bytes = self.min_file_size_kb.get() * 1024

        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid source drive.")
            return

        if not dest:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        self.log(f"Scanning {source} for image/PDF files > {self.min_file_size_kb.get()} KB...\n")

        # Step 1: Find all files to copy
        files_to_copy = []
        for root_dir, _, files in os.walk(source):
            for file in files:
                if self.cancel_requested:
                    self.log("\n🚫 Scan canceled by user.")
                    return
                if any(file.lower().endswith(ext) for ext in PHOTO_EXTENSIONS):
                    full_path = os.path.join(root_dir, file)
                    try:
                        if os.path.getsize(full_path) >= min_size_bytes:
                            files_to_copy.append(full_path)
                    except Exception:
                        continue

        total_files = len(files_to_copy)
        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        # Step 2: Copy files
        copied = 0
        failed = 0

        for full_path in files_to_copy:
            if self.cancel_requested:
                self.log("\n🚫 Scan canceled by user.")
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

        if not self.cancel_requested:
            self.log(f"\n✅ Scan Complete. {copied} copied, {failed} failed.\n")
        self.cancel_button.config(state=tk.DISABLED)

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FileScannerApp(root)
    root.mainloop()
