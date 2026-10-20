# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------

from utils.colors import Colors


class Logo:

    TITLE = f"{Colors.CYAN}{Colors.BOLD}CLI Files Manager{Colors.RESET}"
    VERSION = "v1.0.2"

    WIDTH = 78

    @classmethod
    def header(cls) -> str:
        line = "─" * cls.WIDTH
        return (
            f"{Colors.BLUE}┌{line}┐{Colors.RESET}\n"
            f"{Colors.BLUE}│{Colors.RESET}  {cls.TITLE}  "
            f"{Colors.DIM}{cls.VERSION}{Colors.RESET}"
            f"{' ' * (cls.WIDTH - 3 - len('CLI Files Manager') - len(cls.VERSION) - 2)}"
            f"{Colors.BLUE} │{Colors.RESET}\n"
            f"{Colors.BLUE}└{line}┘{Colors.RESET}"
        )

    @classmethod
    def separator(cls) -> str:
        return f"{Colors.BLUE}{'─' * cls.WIDTH}{Colors.RESET}"

    @classmethod
    def section(cls, title: str) -> str:
        return f"\n{Colors.CYAN}{Colors.BOLD}▸ {title}{Colors.RESET}\n{cls.separator()}"