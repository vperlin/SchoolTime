from PySide6.QtWidgets import QApplication

import logging


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        logging.basicConfig(level=logging.WARNING)
