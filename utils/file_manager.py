# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
import os
import sys
import shutil
import fnmatch
import subprocess
import hashlib
import readline
import tempfile
import time
from pathlib import Path
from typing import Union, Optional, List, Tuple

from utils.colors import Colors
from utils.asciiart import ASCIIArt
from utils.completer import Completer
from utils.desktop_entry import DesktopEntryCreator


class FileManager:
    def __init__(self):
        self.current_path = Path.cwd()
        self.search_results: List[Path] = []
        self.last_search_pattern = ""
        self.setup_completer()

    def setup_completer(self):
        completer = Completer()
        completer.current_path = self.current_path
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims(' \t\n;')

    def smart_input(self, prompt: str, use_current_dir: bool = True) -> str:
        if use_current_dir:
            completer = Completer()
            completer.current_path = self.current_path
            readline.set_completer(completer.complete)
        else:
            readline.set_completer(None)

        return input(prompt)

    def clear_screen(self):
        os.system('cls' if sys.platform == 'win32' else 'clear')

    def get_width(self) -> int:
        try:
            return os.get_terminal_size().columns
        except:
            return 80

    def format_size(self, size_bytes: int) -> str:
        if size_bytes == 0:
            return f"{Colors.YELLOW}0 B{Colors.RESET}"

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                color = Colors.GREEN if unit == 'B' else Colors.CYAN if unit == 'KB' else Colors.YELLOW if unit == 'MB' else Colors.MAGENTA
                return f"{color}{size_bytes:.2f} {unit}{Colors.RESET}"
            size_bytes /= 1024.0
        return f"{Colors.RED}{size_bytes:.2f} PB{Colors.RESET}"

    def calculate_md5(self, file_path: Union[str, Path]) -> Optional[str]:
        file_path = Path(file_path)
        if not file_path.is_file():
            print(f"{Colors.RED}❌ Not a file!{Colors.RESET}")
            return None

        try:
            print(f"{Colors.DIM}Calculating MD5 hash...{Colors.RESET}")
            hash_md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"{Colors.RED}❌ MD5 Error: {e}{Colors.RESET}")
            return None

    def create_desktop_entries(self):
        print(f"\n{Colors.BG_CYAN}{Colors.BOLD} 🖥️ CREATE DESKTOP ENTRIES {Colors.RESET}\n")
        print(f"{Colors.DIM}This will create shortcuts in:{Colors.RESET}")
        print(f"  {Colors.GREEN}1.{Colors.RESET} Application Menu (~/.local/share/applications/)")
        print(f"  {Colors.GREEN}2.{Colors.RESET} Desktop (~/Desktop/)")
        print(f"  {Colors.GREEN}3.{Colors.RESET} Both")
        print(f"  {Colors.GREEN}0.{Colors.RESET} Cancel")
        print()

        choice = input(f"{Colors.YELLOW}👉 Choose option: {Colors.RESET}").strip()

        creator = DesktopEntryCreator()

        if choice == '1':
            created_files, errors = creator.create_entries(create_app_menu=True, create_desktop=False)
        elif choice == '2':
            created_files, errors = creator.create_entries(create_app_menu=False, create_desktop=True)
        elif choice == '3':
            created_files, errors = creator.create_entries(create_app_menu=True, create_desktop=True)
        else:
            print(f"{Colors.YELLOW}Cancelled.{Colors.RESET}")
            input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        if created_files and not errors:
            print(f"\n{Colors.BG_GREEN}{Colors.BOLD} ✅ SUCCESS {Colors.RESET}")
            for file in created_files:
                print(f"{Colors.GREEN}✓ {file}{Colors.RESET}")
            if creator.icon_path:
                print(f"{Colors.GREEN}✓ Icon found at: {creator.icon_path}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠️  Icon not found, using default icon{Colors.RESET}")
            print(f"\n{Colors.DIM}You may need to log out and back in for changes to take effect.{Colors.RESET}")
        elif created_files and errors:
            print(f"\n{Colors.BG_YELLOW}{Colors.BOLD} ⚠️ PARTIAL SUCCESS {Colors.RESET}")
            for file in created_files:
                print(f"{Colors.GREEN}✓ {file}{Colors.RESET}")
            for error in errors:
                print(f"{Colors.RED}✗ {error}{Colors.RESET}")
        else:
            print(f"\n{Colors.BG_RED}{Colors.BOLD} ❌ FAILED {Colors.RESET}")
            for error in errors:
                print(f"{Colors.RED}✗ {error}{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def show_current_location(self):
        home = Path.home()
        display_path = self.current_path

        if str(display_path).startswith(str(home)):
            display_path = Path("~") / display_path.relative_to(home)

        print(f"\n{Colors.BG_BLUE}{Colors.BOLD} 📍 CURRENT LOCATION {Colors.RESET}")
        print(f"{Colors.CYAN} └─ {display_path}{Colors.RESET}")

        try:
            items = list(self.current_path.iterdir())
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]

            print(f"{Colors.DIM}    ├─ 📁 {len(dirs)} directories{Colors.RESET}")
            print(f"{Colors.DIM}    └─ 📄 {len(files)} files{Colors.RESET}")
        except:
            pass

    def display_menu(self):
        print(ASCIIArt.LOGO)
        self.show_current_location()

        menu_items = [
            ("📊", "ANALYZE SIZE", "File/folder size analysis"),
            ("🗑️", "DELETE", "Remove files or folders"),
            ("📖", "VIEW TEXT", "Display text file content"),
            ("🔍", "VIEW HEX", "Show binary/hex view"),
            ("🔐", "MD5 HASH", "Calculate file MD5 checksum"),
            ("📂", "OPEN LOCATION", "Open in file explorer"),
            ("🔎", "SEARCH", "Search files on entire device"),
            ("📁", "CHANGE DIR", "Change working directory"),
            ("💾", "FILE INFO", "Detailed file information"),
            ("🖥️", "DESKTOP ENTRY", "Create desktop shortcuts"),
            ("🚪", "EXIT", "Close application")
        ]

        print(f"\n{Colors.BOLD}{Colors.BG_CYAN} ⚡ MAIN MENU {Colors.RESET}")
        print(f"{Colors.BLUE}┌{'─' * 78}┐{Colors.RESET}")

        for i, (icon, name, desc) in enumerate(menu_items, 1):
            if i == 11:
                color = Colors.RED
                print(
                    f"{Colors.BLUE}{Colors.RESET} {Colors.BOLD}{color} 0.{Colors.RESET} {icon} {Colors.CYAN}{name:<14}{Colors.RESET} "
                    f"{Colors.DIM}{desc:<56}{Colors.RESET}{Colors.BLUE}{Colors.RESET}")
            else:
                color = Colors.GREEN if i <= 3 else Colors.YELLOW if i <= 6 else Colors.MAGENTA
                print(
                    f"{Colors.BLUE}{Colors.RESET} {Colors.BOLD}{color}{i:2}.{Colors.RESET} {icon} {Colors.CYAN}{name:<14}{Colors.RESET} "
                    f"{Colors.DIM}{desc:<56}{Colors.RESET}{Colors.BLUE}{Colors.RESET}")

        print(f"{Colors.BLUE}└{'─' * 78}┘{Colors.RESET}")
        print()

    def page_output(self, content: str, file_path: Optional[Path] = None):
        if not content:
            return

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp:
            if file_path:
                tmp.write(f"{'=' * 80}\n")
                tmp.write(f"FILE: {file_path}\n")
                tmp.write(f"{'=' * 80}\n\n")
            tmp.write(content)
            tmp_path = tmp.name

        try:
            pager = os.environ.get('PAGER', 'less' if sys.platform != 'win32' else 'more')
            subprocess.call([pager, tmp_path])
        except:
            print(content)
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        finally:
            os.unlink(tmp_path)

    def check_file_size(self, file_path: Union[str, Path]) -> float:
        file_path = Path(file_path)
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)

    def get_size_recursive(self, folder_path: Union[str, Path]) -> Tuple[int, List[Tuple[str, int]]]:
        folder_path = Path(folder_path)
        total_size = 0
        file_info_list = []

        print(f"\n{Colors.BG_CYAN}{Colors.BOLD} 📊 SCANNING FOLDER {Colors.RESET}")
        print(f"{Colors.CYAN} └─ {folder_path}{Colors.RESET}\n")

        files = list(folder_path.rglob('*'))
        for i, file_path in enumerate(files):
            if file_path.is_file():
                file_size = file_path.stat().st_size
                total_size += file_size
                file_info_list.append((file_path.name, file_size))

                progress = int((i + 1) / len(files) * 40)
                bar = f"{Colors.GREEN}{'█' * progress}{Colors.DIM}{'░' * (40 - progress)}{Colors.RESET}"
                print(f"\r{bar} {i + 1}/{len(files)} files", end='', flush=True)

        print(f"\n\n{Colors.BLUE}┌{'─' * 50}┐{Colors.RESET}")
        print(f"{Colors.BOLD}📁 TOTAL SIZE: {self.format_size(total_size)}{Colors.RESET}")
        print(f"{Colors.BLUE}└{'─' * 50}┘{Colors.RESET}\n")

        return total_size, file_info_list

    def delete_path(self, path: Union[str, Path]) -> bool:
        path = Path(path)
        try:
            if path.is_file():
                path.unlink()
                print(f"{Colors.BG_GREEN}{Colors.BOLD} ✅ DELETED {Colors.RESET} {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"{Colors.BG_GREEN}{Colors.BOLD} ✅ DELETED {Colors.RESET} {path}")
            return True
        except Exception as e:
            print(f"{Colors.BG_RED}{Colors.BOLD} ❌ ERROR {Colors.RESET} {e}")
            return False

    def read_file_bytes(self, file_path: Union[str, Path]) -> Optional[bytes]:
        file_path = Path(file_path)
        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            output_lines = []
            output_lines.append(f"{Colors.MAGENTA}{'=' * 80}{Colors.RESET}")
            output_lines.append(f"{Colors.BOLD}🔍 HEX VIEW: {file_path.name}{Colors.RESET}")
            output_lines.append(f"{Colors.MAGENTA}{'=' * 80}{Colors.RESET}")
            output_lines.append(f"Total size: {len(data)} bytes\n")

            for i in range(0, len(data), 16):
                chunk = data[i:i + 16]
                hex_part = ' '.join(f'{b:02x}' for b in chunk)
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
                output_lines.append(f"{Colors.DIM}{i:08x}{Colors.RESET}  {hex_part:<48}  {ascii_part}")

            output_lines.append(f"\n{Colors.MAGENTA}{'=' * 80}{Colors.RESET}")

            self.page_output('\n'.join(output_lines), file_path)
            return data

        except Exception as e:
            print(f"{Colors.BG_RED}{Colors.BOLD} ❌ ERROR {Colors.RESET} {e}")
            return None

    def view_text_file(self, file_path: Union[str, Path]) -> Optional[str]:
        file_path = Path(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            header = f"{Colors.GREEN}{'=' * 80}{Colors.RESET}\n"
            header += f"{Colors.BOLD}📄 TEXT VIEW: {file_path.name}{Colors.RESET}\n"
            header += f"{Colors.GREEN}{'=' * 80}{Colors.RESET}\n\n"

            full_content = header + content

            self.page_output(full_content, file_path)
            return content

        except UnicodeDecodeError:
            print(f"{Colors.YELLOW}⚠️  File is not a text file or has different encoding.{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.BG_RED}{Colors.BOLD} ❌ ERROR {Colors.RESET} {e}")
            return None

    def get_file_info(self, file_path: Union[str, Path]):
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"{Colors.RED}❌ File does not exist!{Colors.RESET}")
            return

        stat = file_path.stat()

        created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime))
        modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
        accessed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_atime))

        print(f"\n{Colors.BG_CYAN}{Colors.BOLD} 💾 FILE INFORMATION {Colors.RESET}")
        print(f"{Colors.CYAN}┌{'─' * 60}┐{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Name:{Colors.RESET}        {file_path.name}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Path:{Colors.RESET}        {file_path.parent}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Size:{Colors.RESET}        {self.format_size(stat.st_size)}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Created:{Colors.RESET}     {created_time}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Modified:{Colors.RESET}    {modified_time}")
        print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}Accessed:{Colors.RESET}    {accessed_time}")

        if file_path.is_file():
            md5_hash = self.calculate_md5(file_path)
            if md5_hash:
                print(f"{Colors.CYAN}{Colors.RESET} {Colors.BOLD}MD5:{Colors.RESET}        {md5_hash}")

        print(f"{Colors.CYAN}└{'─' * 60}┘{Colors.RESET}")

    def open_file_location(self, file_path: Union[str, Path]) -> bool:
        file_path = Path(file_path)
        parent_dir = file_path.parent if file_path.is_file() else file_path

        try:
            if sys.platform == 'win32':
                os.startfile(parent_dir)
            elif sys.platform == 'darwin':
                subprocess.run(['open', parent_dir])
            else:
                subprocess.run(['xdg-open', parent_dir])

            print(f"{Colors.BG_GREEN}{Colors.BOLD} ✅ OPENED {Colors.RESET} {parent_dir}")
            return True
        except Exception as e:
            print(f"{Colors.BG_RED}{Colors.BOLD} ❌ ERROR {Colors.RESET} {e}")
            return False

    def search_files(self, pattern: str, search_root: Optional[Union[str, Path]] = None) -> List[Path]:
        if search_root is None:
            search_root = Path('/' if sys.platform != 'win32' else os.environ.get('SystemDrive', 'C:'))
        else:
            search_root = Path(search_root)

        self.clear_screen()
        print(ASCIIArt.SEPARATOR)
        print(f"{Colors.BOLD}{Colors.CYAN}🔍 SEARCH FILES{Colors.RESET}")
        print(f"{Colors.DIM}Pattern: {pattern}{Colors.RESET}")
        print(f"{Colors.DIM}Root: {search_root}{Colors.RESET}")
        print(ASCIIArt.SEPARATOR)

        matches = []
        try:
            for root, dirs, files in os.walk(search_root):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in
                           ['System Volume Information', '$Recycle.Bin', 'Windows', 'Program Files']]

                for filename in files:
                    if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                        file_path = Path(root) / filename
                        matches.append(file_path)

                if len(matches) > 500:
                    print(f"{Colors.YELLOW}⚠️  Showing first 500 results...{Colors.RESET}")
                    break

            self.search_results = matches
            self.last_search_pattern = pattern

            if matches:
                self.display_search_results()
            else:
                print(f"\n{Colors.YELLOW}❌ No files found matching '{pattern}'{Colors.RESET}\n")
                input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}❌ Search error: {e}{Colors.RESET}")

        return matches

    def display_search_results(self):
        print(f"\n{Colors.BG_GREEN}{Colors.BOLD} ✅ FOUND {len(self.search_results)} FILES {Colors.RESET}\n")

        for i, file_path in enumerate(self.search_results, 1):
            size = self.format_size(file_path.stat().st_size if file_path.exists() else 0)
            icon = "📄" if file_path.is_file() else "📁"
            print(
                f"{Colors.CYAN}{i:3}.{Colors.RESET} {icon} {Colors.WHITE}{file_path.name:<40}{Colors.RESET} {Colors.DIM}({size}){Colors.RESET}")
            print(f"     {Colors.DIM}└─ {file_path.parent}{Colors.RESET}")

        if len(self.search_results) > 50:
            print(f"\n{Colors.YELLOW}... and {len(self.search_results) - 50} more files{Colors.RESET}")

        while True:
            print(f"\n{Colors.BLUE}┌{'─' * 50}┐{Colors.RESET}")
            print(
                f"{Colors.BLUE} {Colors.RESET} {Colors.BOLD}Options:{Colors.RESET} [1-{min(50, len(self.search_results))}] view file | [0] back to main menu{Colors.BLUE} {Colors.RESET}")
            print(f"{Colors.BLUE}└{'─' * 50}┘{Colors.RESET}")

            choice = input(f"{Colors.YELLOW}👉 Enter number: {Colors.RESET}").strip()

            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= min(50, len(self.search_results)):
                selected = self.search_results[int(choice) - 1]
                self.search_file_action_menu(selected)
                self.clear_screen()
                print(ASCIIArt.SEPARATOR)
                print(f"{Colors.BOLD}{Colors.CYAN}🔍 SEARCH RESULTS{Colors.RESET}")
                print(f"{Colors.DIM}Pattern: {self.last_search_pattern}{Colors.RESET}")
                print(ASCIIArt.SEPARATOR)
                print(f"\n{Colors.BG_GREEN}{Colors.BOLD} ✅ FOUND {len(self.search_results)} FILES {Colors.RESET}\n")
                for i, file_path in enumerate(self.search_results[:50], 1):
                    size = self.format_size(file_path.stat().st_size if file_path.exists() else 0)
                    icon = "📄" if file_path.is_file() else "📁"
                    print(
                        f"{Colors.CYAN}{i:3}.{Colors.RESET} {icon} {Colors.WHITE}{file_path.name:<40}{Colors.RESET} {Colors.DIM}({size}){Colors.RESET}")
                    print(f"     {Colors.DIM}└─ {file_path.parent}{Colors.RESET}")
                if len(self.search_results) > 50:
                    print(f"\n{Colors.YELLOW}... and {len(self.search_results) - 50} more files{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Invalid choice!{Colors.RESET}")

    def search_file_action_menu(self, file_path: Path):
        while True:
            self.clear_screen()
            width = self.get_width()

            print(f"{Colors.MAGENTA}{'─' * width}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.MAGENTA}  📁 SELECTED FILE{Colors.RESET}")
            file_path_str = str(file_path)
            if len(file_path_str) > width - 6:
                file_path_str = "..." + file_path_str[-(width - 9):]
            print(f"{Colors.CYAN}  └─ {file_path_str}{Colors.RESET}")
            print(f"{Colors.MAGENTA}{'─' * width}{Colors.RESET}")

            print(f"\n{Colors.BOLD}Actions:{Colors.RESET}")
            print(f"  {Colors.GREEN}1.{Colors.RESET} 📂 Open file location")
            print(f"  {Colors.GREEN}2.{Colors.RESET} 📖 View text content")
            print(f"  {Colors.GREEN}3.{Colors.RESET} 🔍 View hex/bytes")
            print(f"  {Colors.GREEN}4.{Colors.RESET} 🔐 Calculate MD5 hash")
            print(f"  {Colors.GREEN}5.{Colors.RESET} 💾 File information")
            print(f"  {Colors.GREEN}6.{Colors.RESET} 🗑️  Delete file")
            print(f"  {Colors.GREEN}0.{Colors.RESET} Back to search results")

            choice = input(f"\n{Colors.YELLOW}👉 Choose action [0-6]: {Colors.RESET}").strip()

            if choice == '0':
                break
            elif choice == '1':
                self.open_file_location(file_path)
                input(f"{Colors.DIM}\nPress Enter to continue...{Colors.RESET}")
            elif choice == '2':
                self.view_text_file(file_path)
                input(f"{Colors.DIM}\nPress Enter to continue...{Colors.RESET}")
            elif choice == '3':
                self.read_file_bytes(file_path)
                input(f"{Colors.DIM}\nPress Enter to continue...{Colors.RESET}")
            elif choice == '4':
                md5_hash = self.calculate_md5(file_path)
                if md5_hash:
                    print(f"\n{Colors.GREEN}MD5 Hash:{Colors.RESET}")
                    print(f"{Colors.BOLD}{md5_hash}{Colors.RESET}")
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            elif choice == '5':
                self.get_file_info(file_path)
                input(f"{Colors.DIM}\nPress Enter to continue...{Colors.RESET}")
            elif choice == '6':
                confirm = input(f"{Colors.RED}⚠️  Delete '{file_path.name}'? (yes/no): {Colors.RESET}").lower()
                if confirm == 'yes':
                    if self.delete_path(file_path):
                        self.search_results.remove(file_path)
                        break
                else:
                    print(f"{Colors.YELLOW}Cancelled.{Colors.RESET}")
                    input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Invalid choice!{Colors.RESET}")

    def interactive_menu(self):
        while True:
            self.clear_screen()
            self.display_menu()

            choice = input(f"{Colors.YELLOW}{Colors.BOLD}⚡ SELECT OPTION [0-9] ⚡{Colors.RESET} ").strip()

            if choice == '0':
                self.clear_screen()
                print(f"\n{Colors.GREEN}{Colors.BOLD}👋 Thank you for using CLI Files Manager v1.0.0!{Colors.RESET}\n")
                print(f"{Colors.DIM}© 2026 Alexander Suvorov. All rights reserved.{Colors.RESET}\n")
                sys.exit(0)

            elif choice == '1':
                self.clear_screen()
                print(f"\n{Colors.BOLD}📊 Analyze File/Folder Size{Colors.RESET}\n")
                path = self.smart_input(
                    f"{Colors.YELLOW}📂 Enter path (or press Enter for current directory, TAB for completion): {Colors.RESET}")
                if not path:
                    path = str(self.current_path)
                self.analyze_path(path)
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == '2':
                self.clear_screen()
                print(f"\n{Colors.BOLD}🗑️  Delete File/Folder{Colors.RESET}\n")
                path = self.smart_input(
                    f"{Colors.YELLOW}📂 Enter path (or press Enter for current directory, TAB for completion): {Colors.RESET}")
                if not path:
                    path = str(self.current_path)
                confirm = input(
                    f"{Colors.RED}⚠️  PERMANENTLY delete '{path}'? (yes/no): {Colors.RESET}").strip().lower()
                if confirm == 'yes':
                    self.delete_path(path)
                else:
                    print(f"{Colors.YELLOW}Cancelled.{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == '3':
                self.clear_screen()
                print(f"\n{Colors.BOLD}📖 View Text File{Colors.RESET}\n")
                path = self.smart_input(f"{Colors.YELLOW}📂 Enter file path (TAB for completion): {Colors.RESET}")
                self.view_text_file(path)

            elif choice == '4':
                self.clear_screen()
                print(f"\n{Colors.BOLD}🔍 View Hex/Bytes{Colors.RESET}\n")
                path = self.smart_input(f"{Colors.YELLOW}📂 Enter file path (TAB for completion): {Colors.RESET}")
                self.read_file_bytes(path)

            elif choice == '5':
                self.clear_screen()
                print(f"\n{Colors.BOLD}🔐 Calculate MD5 Hash{Colors.RESET}\n")
                path = self.smart_input(f"{Colors.YELLOW}📂 Enter file path (TAB for completion): {Colors.RESET}")
                if path:
                    md5_hash = self.calculate_md5(path)
                    if md5_hash:
                        print(f"\n{Colors.GREEN}MD5 Hash of {Path(path).name}:{Colors.RESET}")
                        print(f"{Colors.BOLD}{Colors.CYAN}{md5_hash}{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == '6':
                self.clear_screen()
                print(f"\n{Colors.BOLD}📂 Open Location{Colors.RESET}\n")
                path = self.smart_input(
                    f"{Colors.YELLOW}📂 Enter path (or press Enter for current directory, TAB for completion): {Colors.RESET}")
                if not path:
                    path = str(self.current_path)
                self.open_file_location(path)
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == '7':
                self.clear_screen()
                print(f"\n{Colors.BOLD}🔎 Search Files{Colors.RESET}\n")
                print(f"{Colors.DIM}Examples: *.txt, test*, image*.png, README.md{Colors.RESET}\n")
                pattern = input(f"{Colors.YELLOW}🔍 Enter search pattern: {Colors.RESET}").strip()
                if pattern:
                    root = input(
                        f"{Colors.YELLOW}📁 Search root (press Enter for entire device): {Colors.RESET}").strip()
                    self.search_files(pattern, root if root else None)

            elif choice == '8':
                self.clear_screen()
                print(f"\n{Colors.BOLD}📁 Change Directory{Colors.RESET}\n")
                print(f"{Colors.DIM}Current: {self.current_path}{Colors.RESET}\n")
                new_dir = self.smart_input(
                    f"{Colors.YELLOW}📂 Enter new directory path (TAB for completion): {Colors.RESET}")
                if new_dir:
                    if Path(new_dir).exists() and Path(new_dir).is_dir():
                        os.chdir(new_dir)
                        self.current_path = Path.cwd()
                        self.setup_completer()
                        print(f"{Colors.GREEN}✅ Changed to: {self.current_path}{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}❌ Invalid directory!{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")


            elif choice == '9':
                self.clear_screen()
                print(f"\n{Colors.BOLD}💾 File Information{Colors.RESET}\n")
                path = self.smart_input(f"{Colors.YELLOW}📂 Enter file path (TAB for completion): {Colors.RESET}")
                self.get_file_info(path)
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == '10':
                self.clear_screen()
                print(f"\n{Colors.BOLD}🖥️ Create Desktop Entry{Colors.RESET}\n")
                self.create_desktop_entries()

            else:
                print(f"{Colors.RED}❌ Invalid option! Press Enter to try again...{Colors.RESET}")
                input()

    def analyze_path(self, path: str):
        path_obj = Path(path)

        if not path_obj.exists():
            print(f"{Colors.RED}❌ Path does not exist: {path}{Colors.RESET}")
            return

        if path_obj.is_file():
            size_mb = self.check_file_size(path_obj)
            print(f"\n{Colors.BG_CYAN}{Colors.BOLD} 📄 FILE ANALYSIS {Colors.RESET}")
            print(f"{Colors.CYAN}┌{'─' * 50}┐{Colors.RESET}")
            print(f"{Colors.CYAN} {Colors.RESET} {Colors.BOLD}File:{Colors.RESET}      {path_obj.name}")
            print(
                f"{Colors.CYAN} {Colors.RESET} {Colors.BOLD}Size:{Colors.RESET}      {self.format_size(path_obj.stat().st_size)} ({size_mb:.2f} MB)")
            print(f"{Colors.CYAN} {Colors.RESET} {Colors.BOLD}Path:{Colors.RESET}      {path_obj.parent}")
            print(f"{Colors.CYAN}└{'─' * 50}┘{Colors.RESET}\n")
        elif path_obj.is_dir():
            self.get_size_recursive(path_obj)
