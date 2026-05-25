import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": '["%(asctime)s"] | "%(levelname)s" | "%(funcName)s" | %(name)s | "%(message)s"',
        },
        "file": {
            "format": (
                "[%(asctime)s] | %(levelname)s | %(name)s | "
                '%(filename)s:%(lineno)d | %(funcName)s() | "%(message)s"'
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "console",
            "stream": "ext://sys.stdout",
        },
        "file_main": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/main.log",
            "encoding": "utf-8",
            "mode": "w",
        },
        "file_reports": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/reports.log",
            "encoding": "utf-8",
            "mode": "w",
        },
        "file_services": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/services.log",
            "encoding": "utf-8",
            "mode": "w",
        },
        "file_utils": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/utils.log",
            "encoding": "utf-8",
            "mode": "w",
        },
        "file_views": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/views.log",
            "encoding": "utf-8",
            "mode": "w",
        },
        "file_root": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "../logs/app.log",
            "maxBytes": 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "mode": "w",
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["file_main", "console"],
            "propagate": False,
        },
        "reports": {
            "level": "DEBUG",
            "handlers": ["file_reports", "console"],
            "propagate": False,
        },
        "services": {
            "level": "DEBUG",
            "handlers": ["file_services", "console"],
            "propagate": False,
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["file_utils", "console"],
            "propagate": False,
        },
        "views": {
            "level": "DEBUG",
            "handlers": ["file_views", "console"],
            "propagate": False,
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file_root", "console"],
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
