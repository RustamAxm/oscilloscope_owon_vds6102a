"""
Functions shared by multiple modules
"""

import logging

logging_formatter = logging.Formatter(
    fmt='[%(asctime)s] %(name)s %(levelname).1s %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S'
)


def set_logging(logger: logging.Logger, logfile: str = '', verbose: str = ''):
    """
    Apply log settings to the given logger: setup formatter and add
    appropriate log handler (file or stdout)
    """
    formatter = logging_formatter
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    if logfile:
        fh = logging.FileHandler(filename=logfile)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
