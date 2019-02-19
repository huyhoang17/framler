import os
import logging


def get_logger(name, f_handler=False, f_name='spam.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # formatter
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(fmt)

    if f_handler:
        if os.path.exists(f_name):
            os.remove(f_name)
            logging.info('Completed delete %s', f_name)
        file_handler = logging.FileHandler(f_name, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)

    # add handler to formatter
    logger.addHandler(handler)
    if f_handler:
        logger.addHandler(file_handler)

    return logger
