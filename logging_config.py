import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging():
    current_file_path = Path(__file__).resolve()
    log_dir = current_file_path.parent / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir / 'app.log' 

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3)
    log_handler.setFormatter(log_formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    return logger