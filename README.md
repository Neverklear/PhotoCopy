# 📂 Drive Scanner & Photo Copier GUI

This Python-based GUI tool allows users to scan an entire drive for image and document files (e.g., `.jpg`, `.png`, `.pdf`, `.tiff`, etc.), then copy those files to a destination folder while preserving the original folder structure.

---

## ✅ Features

- 🔍 Scan entire drive (including hidden folders and subdirectories)
- 🖼️ Supports multiple image and document formats:
  - `.jpeg`, `.jpg`, `.png`, `.gif`, `.tiff`, `.bmp`, `.webp`, `.heic`, `.pdf`, `.raw`, etc.
- 📁 Maintains original folder structure
- 🚫 Set minimum file size filter (in KB)
- 🧭 Real-time progress bar and log output
- ❌ Cancel button to safely stop scanning mid-process
- 🖥️ Built-in GUI using Python `tkinter`

---

## 🖥️ Requirements

- Python 3.8+
- No additional packages needed — uses only standard libraries (`tkinter`, `os`, `shutil`, etc.)

---

## ▶️ How to Run

1. Clone this repository or download the ZIP
2. Open a terminal and run:

```bash
python photo_copier_gui.py
