import datetime
import inspect
import logging
import os

import colorlog

LOG_COLOR_CONFIG = {
    "DEBUG": "light_green",
    "INFO": "white",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


def get_current_datetime_str() -> str:
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d_%H_%M_%S")
    return date_str


def name_to_path(ident: str, use_time: bool = True) -> str:
    parts = ident.split(".")
    parts = ["./log"] + parts  # add `log`
    if use_time:
        parts[-1] += f"_{get_current_datetime_str()}"
    parts[-1] += ".log"
    return os.path.join(*parts)


def get_logger(
    name: str, identity: str = None, path: str = None, level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    raw_format_string = (
        "[%(asctime)s.%(msecs)03d] [%(levelname)s] "
        + "%(filename)s:%(lineno)d <%(funcName)s> : %(message)s"
    )

    formatter = logging.Formatter(raw_format_string, datefmt="%Y-%m-%d %H:%M:%S")

    """File Handler"""
    if identity is None:
        identity = name

    if path is None:
        path = name_to_path(identity)
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_formatter = colorlog.ColoredFormatter(
        fmt=f"%(log_color)s{raw_format_string}",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=LOG_COLOR_CONFIG,
    )
    """Stream Handler"""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(console_formatter)
    logger.addHandler(stream_handler)

    return logger


def add_logger(cls=None, *, level=logging.INFO):
    if cls is None:
        return lambda cls: add_logger(cls, level=level)

    module = inspect.getmodule(cls).__name__
    name = cls.__name__
    logger = get_logger(name, f"{module}.{name}", level=level)
    setattr(cls, "logger", logger)
    return cls


if __name__ == "__main__":
    logger = get_logger("demo")
    logger.info("Hello, world!")
    logger.warning("Warning Message!")
