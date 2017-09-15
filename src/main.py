"""
Sammy | What stocks to buy today?
    A software monitoring tool for stock market investors using the Strategic Averaging Method (SAM) aka flipping.

Feature(s):
    * Easily identify what stocks to buy based on its current market price

Interface: GUI (PyQt5)
Language: Python 3.5.2
Created: 13 Aug 2017 7:08 PM
Author: mokachokokarbon <tokidokitalkyou@gmail.com>
"""

import sys
from PyQt5.QtWidgets import QApplication

sys.path.append('..')

APP = QApplication(sys.argv)

if __name__ == '__main__':
    from src.main_window import Sammy
    window = Sammy()
    window.show()
    APP.exec()
