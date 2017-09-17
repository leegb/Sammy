# Main UI

from PyQt5.QtCore import (Qt,
                          QSettings)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QMainWindow,
                             QAction,
                             QToolBar,
                             QLabel,
                             QMessageBox,
                             QTableView)
from resources.models import (StockMonitoringTableModel)
from resources.constant import (RAW_RECORD,
                                RECORD)
import sammy

ABOUT = 'A software monitoring tool for stock market investors using the Strategic Averaging Method (SAM) aka flipping.'


class Sammy(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.companies = []
        self._widgets()
        self._properties()
        self._actions()
        self._menus()
        self._toolbar()
        self._statusbar()
        self.check_REST_API()
        self._read_settings()

    def _widgets(self):

        self.stock_table_model = StockMonitoringTableModel()
        self.stockmonitoringTableView = QTableView()
        self.statusbarLabel = QLabel()
        self.statusNormalLabel = QLabel()

    def _properties(self):

        # Main window
        self.setWindowTitle('Sammy | What stocks to buy today?')
        self.setCentralWidget(self.stockmonitoringTableView)
        self.resize(920, 457)

        # Central Widget
        self.stockmonitoringTableView.setModel(self.stock_table_model)

    def _actions(self):

        # File menu actions
        self.newAction = QAction("&New", self,
                                 shortcut=QKeySequence.New,
                                 statusTip='Add a stock to monitor',
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

        # temp, normal, permanent
        self.statusbar = self.statusBar()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbar.addPermanentWidget(self.statusNormalLabel)
        self.statusbar.showMessage('Ready', 7000)

    def check_REST_API(self):

        # TODO: always check the API if active or not every 2-3 minutes
        try:
            timestamp = sammy.as_of()
            self.statusNormalLabel.setText('Online')
            print(timestamp)
        except Exception as e:
            self.statusNormalLabel.setText('Offline')
            print(e)

    def _read_settings(self):

        settings = QSettings('CodersGym', 'Sammy')
        self.restoreGeometry(settings.value('sammy_geometry', self.saveGeometry()))
        self.restoreState(settings.value('sammy_state', self.saveState()))

        # Reload previously monitored companies
        self.companies = settings.value('companies', self.companies)
        for raw_quote in self.companies:
            self.actions(raw_quote['symbol'],
                         raw_quote['buy_below'],
                         raw_quote['target_price'])
        print(self.companies)

    def _write_settings(self):

        settings = QSettings('CodersGym', 'Sammy')
        settings.setValue('sammy_geometry', self.saveGeometry())
        settings.setValue('sammy_state', self.saveState())
        settings.setValue('companies', self.companies)
        print(self.companies)

    # Actions
    def on_new_action(self):

        from src.dialogs.new import New
        dialog = New()

        if dialog.exec():
            symbol = dialog.stocklistComboBox.currentText()
            buy_below = float(dialog.buybelowLineEdit.text())
            target_price = float(dialog.targetpriceLineEdit.text())

            raw_quote = {'symbol': symbol,
                         'buy_below': buy_below,
                         'target_price': target_price}

            self.actions(raw_quote['symbol'],
                         raw_quote['buy_below'],
                         raw_quote['target_price'])

            # save user input
            self.companies.append(raw_quote)

    def on_edit_action(self):

        print('TODO: editing?')

    def on_aboutAction_clicked(self):

        QMessageBox.about(self, 'About Sammy', ABOUT)

    # TODO: for cleaning, this is ugly
    def actions(self, stock_code, buy_below, target_price):

        try:
            # Request query to Phisix API
            company = sammy.stock(stock_code)
            as_of = sammy.as_of()

            # Determine what action to take based on stock's current market price
            if company['price'] < buy_below:  # BUY
                action = 'Buy'
            elif buy_below <= company['price'] < target_price:  # HOLD
                action = 'Hold'
            elif company['price'] >= target_price:  # SELL
                action = 'Sell'

            # Packaging values in ordered
            RAW_RECORD['company'] = company['company']
            RAW_RECORD['symbol'] = company['symbol']
            RAW_RECORD['price'] = '{0} ({1})'.format(company['price'], company['change'])
            RAW_RECORD['BB'] = buy_below
            RAW_RECORD['TP'] = target_price
            RAW_RECORD['action'] = action
            RAW_RECORD['remarks'] = 'dailypik.com/undervalued-stocks-in-the-philippines-latest-list/'

            # Transfer packed record to the table model
            RECORD.append(list(RAW_RECORD.values()))
            self.stock_table_model.insertRows(len(RECORD), 1)
            self.stockmonitoringTableView.setModel(self.stock_table_model)

            # Display market time
            self.statusbar.showMessage('Market price as of {}'.format(as_of))

        except Exception as e:
            self.statusbar.showMessage('Last request to API failed, try again.', 7000)
            print(e)

    def closeEvent(self, e):

        self._write_settings()



