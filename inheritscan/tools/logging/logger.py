import logging
import os


def get_logger(name="default", log_dir="logs"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
            )
        )
        logger.addHandler(console_handler)

        # File handler
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
            )
        )
        logger.addHandler(file_handler)

    return logger
