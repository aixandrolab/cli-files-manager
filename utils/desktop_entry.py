#!/usr/bin/env python3
# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------

import os
import sys
from pathlib import Path


class DesktopEntryCreator:
    def __init__(self, app_name: str = "CLI Files Manager"):
        self.app_name = app_name
        self.app_executable = sys.executable
        self.app_path = os.path.abspath(sys.argv[0])
        self.icon_path = self.find_icon_path()
        self.version = "1.0.0"

    def find_icon_path(self):
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(__file__), "..", "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(sys.argv[0]), "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(sys.argv[0]), "icon.png"),
            os.path.expanduser("~/.local/share/icons/cli-files-manager.png"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return ""

    def generate_desktop_content(self):
        exec_line = f'"{self.app_executable}" "{self.app_path}"'
        icon_line = self.icon_path if self.icon_path else 'utilities-terminal'
        comment = "A comprehensive command-line file management tool with advanced features"

        content = f"""[Desktop Entry]
Version={self.version}
Type=Application
Name={self.app_name}
Comment={comment}
Exec={exec_line}
Icon={icon_line}
Terminal=true
Categories=Utility;FileManager;System;
StartupNotify=true
Keywords=file;manager;cli;filesystem;search;md5;
"""
        return content

    def create_app_menu_entry(self):
        try:
            desktop_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(desktop_dir, exist_ok=True)

            desktop_file = os.path.join(desktop_dir, "cli-files-manager.desktop")

            content = self.generate_desktop_content()

            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)

            os.chmod(desktop_file, 0o755)

            return True, desktop_file

        except Exception as e:
            return False, str(e)

    def create_desktop_shortcut(self):
        try:
            desktop_dir = os.path.expanduser("~/Desktop")
            os.makedirs(desktop_dir, exist_ok=True)

            desktop_file = os.path.join(desktop_dir, "cli-files-manager.desktop")

            content = self.generate_desktop_content()

            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)

            os.chmod(desktop_file, 0o755)

            return True, desktop_file

        except Exception as e:
            return False, str(e)

    def create_entries(self, create_app_menu=True, create_desktop=True):
        created_files = []
        errors = []

        if create_app_menu:
            success, message = self.create_app_menu_entry()
            if success:
                created_files.append(f"Application Menu: {message}")
            else:
                errors.append(f"Application Menu: {message}")

        if create_desktop:
            success, message = self.create_desktop_shortcut()
            if success:
                created_files.append(f"Desktop: {message}")
            else:
                errors.append(f"Desktop: {message}")

        return created_files, errors
