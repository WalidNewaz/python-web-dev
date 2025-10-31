import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger once with the same format/level used before."""
    logging.basicConfig(level=level, format=LOG_FORMAT)