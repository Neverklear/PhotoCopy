# 🧰 Data Recovery Tool by Neverklear Technologies

A powerful and easy-to-use Windows utility designed to recover user data from drives. Originally forked from the "PhotoCopy" project, this version adds enhanced recovery features for documents, music, videos, QuickBooks files, and full user profiles — all while maintaining folder structure and logging errors along the way.

---

## ✅ Features

- 🔍 **Deep Drive Scanning**
  - Recursively searches directories on any drive
  - Works with internal, external, and USB drives

- 📁 **Copy Modes**
  - **Copy User Data:** Grabs all folders from `C:\Users`
  - **Copy Documents:** `.doc`, `.docx`, `.xls`, `.pdf`, etc.
  - **Copy Music:** `.mp3`, `.wav`, `.m4a`, etc.
  - **Copy Videos:** `.mp4`, `.avi`, `.mkv`, etc.
  - **Copy QuickBooks Files:** `.QBW`, `.QBB`, `.QBM`, `.ND`, `.TLG`, and more

- 🔒 **Safe Copying**
  - Skips unreadable or locked files without crashing
  - Logs errors and failed copies to `logfile.txt`

- 📐 **Preserves Folder Structure**
  - Recreates full path structure in destination folder

- 📊 **Progress Tracking**
  - Live progress bar
  - Status summary on completion

- ❌ **Cancel Button with Confirmation**
  - Cleanly stops scanning and copying on demand

- 📏 **Minimum File Size Filter**
  - Set file size threshold (e.g., skip small cache files)

---

## 🖥️ How to Run

### Option 1: Run with Python (Windows)
1. Install Python 3.9+ from [python.org](https://www.python.org/)
2. Clone the repository:
   ```bash
   git clone https://github.com/neverklear/
   cd data-recovery-tool
