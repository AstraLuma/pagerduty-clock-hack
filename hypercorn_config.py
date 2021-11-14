# bind = ['127.0.0.1:9081']

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "asyncio": {
            "level": "INFO",
        },
        "hypercorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "hypercorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "app": {
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
    },
    "formatters": {
        "generic": {
            "format": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
            "class": "logging.Formatter",
        }
    },
}

try:
    import uvloop  # noqa: F401
except ImportError:
    pass
else:
    worker_class = 'uvloop'
