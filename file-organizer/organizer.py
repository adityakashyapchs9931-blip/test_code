"""
File Organizer
--------------
Scans a directory and sorts files into subfolders based on their type
(Images, Documents, Videos, Audio, Archives, Code, Others).

Usage:
    python organizer.py                # organizes the current directory
    python organizer.py /path/to/dir   # organizes a specific directory
"""

import os
import shutil
import sys

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
}


def get_category(extension: str) -> str:
    """Return the folder name a given file extension belongs to."""
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def organize_directory(directory: str) -> None:
    """Move every file in `directory` into a category subfolder."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    moved_count = 0
    skipped_count = 0

    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)

        # Skip subfolders and the script itself
        if os.path.isdir(entry_path):
            continue

        _, extension = os.path.splitext(entry)
        if not extension:
            skipped_count += 1
            continue

        category = get_category(extension)
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)

        destination = os.path.join(category_path, entry)

        # Avoid overwriting files with the same name
        if os.path.exists(destination):
            base, ext = os.path.splitext(entry)
            counter = 1
            while os.path.exists(destination):
                destination = os.path.join(category_path, f"{base}_{counter}{ext}")
                counter += 1

        shutil.move(entry_path, destination)
        print(f"Moved: {entry} -> {category}/")
        moved_count += 1

    print(f"\nDone. {moved_count} file(s) organized, {skipped_count} skipped.")


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    organize_directory(target_dir)
