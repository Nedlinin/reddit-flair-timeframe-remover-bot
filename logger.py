import logging
import os


class Logger:
    def __init__(self):
        self.log = logging.getLogger('reddit-bot')
        self.log.setLevel(logging.DEBUG)

        if self.log.hasHandlers() is True:
            return

        fh = logging.FileHandler(('{}/data/run.log'.format(os.path.dirname(os.path.realpath(__file__)))), 'w', 'utf-8')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s : %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.log.addHandler(fh)
        self.log.addHandler(ch)

    def info(self, message: str):
        self.log.info(message)

    def error(self, message: str):
        self.log.error(message)

    def exception(self, message: str):
        self.log.exception(message)
