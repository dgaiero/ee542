# https: // www.toptal.com/python/in-depth-python-logging

import logging
import logging.config
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

import colorlog

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s — %(name)s — %(levelname)s — %(message)s",
            "log_colors":
            {
                "DEBUG":    "cyan",
                "INFO":     "green",
                "WARNING":  "yellow",
                "ERROR":    "red",
                "CRITICAL": "red,bg_white"
            }
        },
        "default": {
            "()": "logging.Formatter",
            "format": "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "./logs/run.log",
            "formatter": "default"
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file"]
        }
    },
    "disable_existing_loggers": False
}


def setup_root_logger(logger_name: str, logging_dict: Dict = LOGGING_CONFIG) -> logging.Logger:

    logging.config.dictConfig(logging_dict)
    return logging.getLogger(logger_name)
