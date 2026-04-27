# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2026, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------

import os
from pathlib import Path


class Completer:
    def __init__(self):
        self.current_path = Path.cwd()

    def complete(self, text, state):
        if not text:
            text = '.'

        current_dir = Path(text).parent if '/' in text or '\\' in text else Path('.')
        if str(current_dir) == '.':
            current_dir = self.current_path

        try:
            matches = []
            for item in current_dir.glob(f"{Path(text).name}*"):
                if item.is_dir():
                    matches.append(str(item) + os.sep)
                else:
                    matches.append(str(item))

            matches.sort()
            return matches[state] if state < len(matches) else None
        except:
            return None
