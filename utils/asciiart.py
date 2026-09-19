# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------

from utils.colors import Colors


class ASCIIArt:
    LOGO = f"""
{Colors.CYAN}{Colors.BOLD}    ╔══════════════════════════════════════════════════════════════╗
    ║     ██████╗██╗     ██╗      ███████╗██╗██╗     ███████╗      ║
    ║    ██╔════╝██║     ██║      ██╔════╝██║██║     ██╔════╝      ║
    ║    ██║     ██║     ██║█████╗█████╗  ██║██║     █████╗        ║
    ║    ██║     ██║     ██║╚════╝██╔══╝  ██║██║     ██╔══╝        ║
    ║    ╚██████╗███████╗██║      ██║     ██║███████╗███████╗      ║
    ║     ╚═════╝╚══════╝╚═╝      ╚═╝     ╚═╝╚══════╝╚══════╝      ║
    ║                  FILES MANAGER v1.0.1                        ║
    ╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

    SEPARATOR = f"{Colors.BLUE}╔{'═' * 78}╗{Colors.RESET}"
    SEPARATOR_MID = f"{Colors.BLUE}╠{'═' * 78}╣{Colors.RESET}"
    SEPARATOR_BOTTOM = f"{Colors.BLUE}╚{'═' * 78}╝{Colors.RESET}"
