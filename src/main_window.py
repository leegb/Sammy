# Main UI

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QMainWindow,
                             QAction,
                             QToolBar,
                             QLabel,
                             QMessageBox)

ABOUT = 'A software monitoring tool for stock market investors using the Strategic Averaging Method (SAM).'


class Sammy(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets()
        self._properties()
        self._actions()
        self._menus()
        self._toolbar()
        self._statusbar()

    def _widgets(self):

        self.statusbarLabel = QLabel()

    def _properties(self):

        # Main window
        self.setWindowTitle('Sammy | What stocks to buy today?')
        self.resize(920, 457)

    def _actions(self):

        # File menu actions
        self.newAction = QAction("&New", self,
                                 shortcut=QKeySequence.New,
                                 statusTip='Create a stock to monitor',
                                 toolTip='New',
                                 triggered=self.on_new_action)
        self.exitAction = QAction("E&xit", self,
                                  shortcut="Ctrl+Q",
                                  statusTip="Exit the application",
                                  triggered=self.close)

        # Edit: actions
        self.editAction = QAction('&Edit', self,
                                  triggered=self.on_edit_action)

        # Help: actions
        self.aboutAction = QAction('&About', self,
                                   triggered=self.on_aboutAction_clicked)

    def _menus(self):

        # File: menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        # Edit: menu
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.editAction)

        # Help: menu
        self.helpMenu = self.menuBar().addMenu('&Help')
        self.helpMenu.addAction(self.aboutAction)

    def _toolbar(self):

        # File: toolbar
        self.fileToolBar = QToolBar('File')
        self.fileToolBar.setMovable(False)
        self.fileToolBar.addAction(self.newAction)
        self.addToolBar(Qt.LeftToolBarArea, self.fileToolBar)

        # Edit: toolbar
        self.editToolBar = QToolBar('Edit')
        self.editToolBar.setMovable(False)
        self.editToolBar.addAction(self.editAction)
        self.addToolBar(Qt.LeftToolBarArea, self.editToolBar)

    def _statusbar(self):

        self.statusbar = self.statusBar()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbar.showMessage('Ready', 7000)

    # Actions
    def on_new_action(self):

        print('TODO: show a new dialog')

    def on_edit_action(self):

        print('TODO: editing?')

    def on_aboutAction_clicked(self):

        QMessageBox.about(self, 'About Sammy', ABOUT)

    # Events
    def resizeEvent(self, event):

        print('w x h -> {0} x {1}'.format(self.width(), self.height()))

