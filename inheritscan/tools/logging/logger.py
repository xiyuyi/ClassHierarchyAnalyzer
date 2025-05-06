import logging
import os

from inheritscan.configs.config_loader import load_json_config


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        import json

        return json.dumps(
            {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
        )


def get_logger(name="default"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    config = load_json_config("logger_config")

    # 设置日志级别
    log_level = getattr(
        logging, config.get("log_level", "INFO").upper(), logging.INFO
    )
    logger.setLevel(log_level)

    # 设置格式
    if config.get("json_format", False):
        formatter = JsonLogFormatter()
    else:
        formatter = logging.Formatter(
            config.get(
                "format",
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            )
        )

    # 控制台输出
    if config.get("log_to_console", True):
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # 文件输出
    if config.get("log_to_file", True):
        log_dir = config.get("log_dir", "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_name = (
            f"{name}.log" if config.get("per_module_file", True) else "app.log"
        )
        log_path = os.path.join(log_dir, file_name)
        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
