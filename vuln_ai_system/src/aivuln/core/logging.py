import logging
from pathlib import Path


def setup_logging(run_dir: str) -> None:
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(run_dir) / "run.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

