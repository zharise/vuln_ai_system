from pathlib import Path
from typing import Set


class RunState:
    def __init__(self, run_dir: str) -> None:
        self.path = Path(run_dir) / "state.done"
        self.done: Set[str] = set()
        if self.path.exists():
            self.done = {line.strip() for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()}

    def is_done(self, key: str) -> bool:
        return key in self.done

    def mark_done(self, key: str) -> None:
        if key in self.done:
            return
        with self.path.open("a", encoding="utf-8") as f:
            f.write(key + "\n")
        self.done.add(key)

