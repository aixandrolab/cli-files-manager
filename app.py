# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------

import sys
from utils.file_manager import FileManager
from utils.colors import Colors


def main():
    try:
        manager = FileManager()
        manager.interactive_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()
