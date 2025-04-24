# 🧰 Data Recovery Tool by Neverklear Technologies

A comprehensive and technician-friendly Windows utility for recovering user data from internal and external drives. Designed to assist IT professionals, this tool scans deeply and preserves folder structures while supporting a variety of data types.

---

## ✅ Features

- 🔍 **Deep Drive Scanning**
  - Recursively searches all directories
  - Supports internal, external, and USB drives
  - Maintains original folder structure

- 📁 **Copy Modes**
  - **Copy Photos**: `.jpg`, `.png`, `.heic`, `.raw`, `.pdf`, and more
  - **Copy Documents**: `.doc`, `.docx`, `.xls`, `.pdf`, `.txt`, etc.
  - **Copy Music**: `.mp3`, `.wav`, `.flac`, `.aac`, etc.
  - **Copy Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`, etc.
  - **Copy QuickBooks Files**: `.qbw`, `.qbb`, `.qbm`, `.nd`, `.tlg`, and many others
  - **Copy User Data**: Copies entire contents of the `Users` folder (e.g., `C:\Users`)

- 📊 **Smart File Copying**
  - File size filter to skip small or temporary files
  - Skips files that can’t be accessed (logs them instead)
  - Auto-scroll live log view with real-time status

- 🔴 **Cancel with Confirmation**
  - Stop any scan/copy operation safely mid-process

- 📁 **Logging**
  - Detailed output in GUI
  - Errors written to `logfile.txt` for review

---

## 🖥️ How to Run

### Option 1: Run with Python (Windows)
1. Install Python 3.9+ from [python.org](https://www.python.org/)
2. Clone or download the repository:
   ```bash
   git clone https://github.com/your-username/data-recovery-tool.git
   cd data-recovery-tool
