# CLI Files Manager <sup>v1.0.2</sup>

---

**A comprehensive, powerful command-line file management tool with advanced features for Linux.**

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/aixandrolab/cli-files-manager)](https://github.com/aixandrolab/cli-files-manager/)
![GitHub top language](https://img.shields.io/github/languages/top/aixandrolab/cli-files-manager)
[![GitHub](https://img.shields.io/github/license/aixandrolab/cli-files-manager)](https://github.com/aixandrolab/cli-files-manager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/aixandrolab/cli-files-manager?style=social)](https://github.com/aixandrolab/cli-files-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aixandrolab/cli-files-manager?style=social)](https://github.com/aixandrolab/cli-files-manager/network/members)

---

**Powerful file operations, MD5 checksums, hex viewing, recursive size analysis, device-wide search, and desktop integration — all from your terminal.**

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks for file operations, deletions, and system interactions.

**Full legal disclaimer:** See [DISCLAIMER.md](DISCLAIMER.md)

---

## Features

- **Recursive size analysis** - Scan folders and see detailed size breakdowns
- **Safe deletion** - Delete files and folders with confirmation prompts
- **Text file viewer** - View any text file with paging support
- **Hex/Binary viewer** - Examine raw file contents in hexadecimal format
- **MD5 hash calculator** - Generate and verify file checksums
- **Open location** - Open current or selected path in system file explorer
- **Device-wide search** - Find files by pattern with preview and navigation
- **Interactive directory navigation** - Change working directory with tab completion
- **Detailed file info** - View metadata, timestamps, sizes, and MD5
- **Desktop integration** - Create .desktop entries for app menu and desktop
- **Color-coded output** - Beautiful terminal UI with intuitive color coding
- **Tab completion** - Auto-complete file and directory paths

---

![Main Menu](https://github.com/aixandrolab/cli-files-manager/blob/master/data/images/main_menu.png)

---

## Installation

### Dependencies

```bash
# Arch Linux
sudo pacman -S python python-pip

# Debian/Ubuntu
sudo apt install python3 python3-pip

# Fedora/RHEL
sudo dnf install python3 python3-pip

# No additional Python packages required — uses only standard library!
```

### Setup from Repository

1. **Clone the repository:**
   ```bash
   cd ~
   git clone https://github.com/aixandrolab/ cli-files-manager.git
   cd  cli-files-manager
   ```

2. **Run directly (development mode):**
   ```bash
   python app.py
   ```

3. **Create desktop entries (from within the app):**
   - Launch: ` cli-files-manager`
   - Select option `10` → `🖥️ DESKTOP ENTRY`
   - Choose menu integration (application menu, desktop, or both)

---

## Quick Start

```bash
# Launch the interactive menu
 cli-files-manager

# Inside the application:

# 1. Analyze folder size
ANALYZE SIZE → /home/user/Downloads

# 2. Search for files
SEARCH → pattern: *.txt

# 3. View file in hex
VIEW HEX → select any binary file

# 4. Calculate MD5
MD5 HASH → select any file

# 5. Create desktop shortcut
DESKTOP ENTRY → create system integration
```

---

## Main Menu Options

| Option | Command       | Description                                  |
|--------|---------------|----------------------------------------------|
| 1      | ANALYZE SIZE  | Analyze file/folder size with progress bar   |
| 2      | DELETE        | Permanently delete files or folders          |
| 3      | VIEW TEXT     | Display text file content with pager         |
| 4      | VIEW HEX      | Show binary/hexadecimal file view            |
| 5      | MD5 HASH      | Calculate MD5 checksum of any file           |
| 6      | OPEN LOCATION | Open path in system file explorer            |
| 7      | SEARCH        | Search entire device for files by pattern    |
| 8      | CHANGE DIR    | Change working directory with TAB completion |
| 9      | FILE INFO     | Show detailed file metadata                  |
| 10     | DESKTOP ENTRY | Install app to system menu/desktop           |
| 0      | EXIT          | Exit application                             |

---

## Usage Examples

### Analyze Folder Size
```bash
# Select option 1, enter path or press Enter for current directory
/home/user/Downloads

# Output example:
[████████████████████████████████████████] 1250/1250 files
TOTAL SIZE: 2.45 GB
```

### Search Files Device-Wide
```bash
# Select option 7
Enter search pattern: *.mp3
Search root: /home/user/Music

# Results show all matches with sizes and paths
# You can select any result to: open location, view, delete, get MD5, or see info
```

### Calculate MD5 Hash
```bash
# Select option 5
Enter file path: /path/to/file.iso

# Output:
MD5 Hash of file.iso:
a1b2c3d4e5f678901234567890123456
```

### View Binary File in Hex
```bash
# Select option 4
Enter file path: binary_file.bin

# Output shows hex dump with ASCII representation:
00000000  89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52  .PNG........IHDR
00000010  00 00 02 00 00 00 02 00  08 06 00 00 00  ... etc
```

### Create Desktop Integration
```bash
# Select option 10
Choose option: 3 (Both)

# Output:
SUCCESS
Application Menu: /home/user/.local/share/applications/ cli-files-manager.desktop
Desktop: /home/user/Desktop/ cli-files-manager.desktop
Icon found at: /opt/ cli-files-manager/data/icons/icon.png
```

---

## File Structure

```
 cli-files-manager/
├── app.py                     # Main entry point
├── utils/
│   ├── logo.py                # Logo and separators
│   ├── colors.py              # Terminal color definitions
│   ├── completer.py           # Tab completion handler
│   ├── desktop_entry.py       # .desktop file creator
│   └── file_manager.py        # Core file management logic
├── data/
│   ├── icons/
│   │   └── icon.png           # Application icon
│   └── images/
│       └── main_menu.png      # Menu screenshot (documentation)
├── .gitignore
├── LICENSE                     # BSD 3-Clause License
└── README.md                   # This file
```

---

## How It Works

- **Pure Python 3** — Uses only standard library (no external dependencies)
- **Tab completion** — Powered by Python's `readline` module with custom path completer
- **Recursive scanning** — Efficient directory walking with real-time progress
- **Hex viewer** — Binary-safe reading with hexdump-style formatting
- **MD5 calculation** — Streaming hash computation for files of any size
- **Desktop integration** — Generates freedesktop.org-compatible `.desktop` files
- **Paging support** — Uses `less`/`more` for long output, falls back to inline display

---

## Security & Safety Notes

- **Deletion is permanent** — No recycle bin, files are removed immediately
- **All operations require confirmation** — Especially destructive actions
- **No data collection** — Works completely offline, no telemetry
- **Respects permissions** — Cannot access files without proper OS permissions
- **Desktop files are safe** — Created in user directories, not system-wide

---

## Troubleshooting

### Tab completion not working?
```bash
# Install readline if missing (usually included)
# For minimal Python installations:
pip3 install readline
```

### "less" pager not found?
```bash
# Install less (or use more):
sudo apt install less  # Debian/Ubuntu
sudo pacman -S less    # Arch
```

### Desktop entries not showing?
```bash
# Update desktop database:
update-desktop-database ~/.local/share/applications/

# Log out and back in, or restart your desktop environment
```

### Permission denied errors?
```bash
# Run with appropriate user permissions
# Do NOT run as root unless necessary
# Check file ownership: ls -la /path/to/file
```

---

## Development & Testing

```bash
# Run with verbose output (no arguments - just use menu)
python app.py
```

---

## Author & Repository

- **Author:** [Alexander Suvorov](https://github.com/aixandrolab)
- **GitHub:** [@aixandrolab](https://github.com/aixandrolab)
- **Repository:** [aixandrolab/cli-files-manager](https://github.com/aixandrolab/cli-files-manager)
- **License:** BSD 3-Clause

---

## Similar Projects

- **Smart 2FA Manager** — TOTP 2FA manager for Linux (Bash)
- **Smart File Manager CLI** — This project
- More tools at [aixandrolab](https://github.com/aixandrolab)

---

## License

*Licensed under [BSD 3-Clause License](LICENSE) • Copyright (©) 2026, [Alexander Suvorov](https://github.com/aixandrolab)*

---

**Made with ❤️ for terminal lovers who want powerful file management at their fingertips.**
