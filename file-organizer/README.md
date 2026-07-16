# File Organizer

A simple Python script that scans a directory and automatically sorts files
into subfolders based on their type: Images, Documents, Videos, Audio,
Archives, Code, and Others.

## How it works

1. Scans all files in the target directory (top-level only, ignores existing subfolders).
2. Identifies each file's category based on its extension.
3. Creates category folders if they don't already exist.
4. Moves each file into its matching folder, renaming duplicates instead of overwriting them.

## Usage

```bash
# Organize the current directory
python organizer.py

# Organize a specific directory
python organizer.py "C:/Users/YourName/Downloads"
```

## Requirements

No external dependencies — uses only Python's standard library (`os`, `shutil`, `sys`).

## Example

```
Before:
Downloads/
  photo.jpg
  notes.pdf
  song.mp3
  archive.zip

After:
Downloads/
  Images/photo.jpg
  Documents/notes.pdf
  Audio/song.mp3
  Archives/archive.zip
```
