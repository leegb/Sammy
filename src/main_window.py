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
from resources.constant import (ABOUT,
                                COMPANIES,
                                RAW_RECORD,
                                RECORD)
# # [] TODO: add a new method in sammy that can retrieve all stocks in one query
import sammy


# [] TODO: add a 'Refresh' feature
# [] TODO: removing of stocks in the main table
# [x] TODO: editing of stocks in the table
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
        self._connections()
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
        self.deleteAction = QAction('&Delete', self,
                                    triggered=self.on_delete_action)

        # Tools: actions
        self.refreshAction = QAction('&Refresh', self,
                                     shortcut='F5',
                                     statusTip='Refresh stock table',
                                     toolTip='Refresh',
                                     triggered=self.on_refresh_action)

        # Help: actions
        self.aboutAction = QAction('&About', self,
                                   triggered=self.on_aboutAction_clicked)

    def _menus(self):

        # File: menu
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        # Edit: menu
        self.editMenu = self.menuBar().addMenu('&Edit')
        self.editMenu.addAction(self.editAction)

        # Tools: menu
        self.toolsMenu = self.menuBar().addMenu('&Tools')
        self.toolsMenu.addAction(self.refreshAction)

        # Help: menu
        self.helpMenu = self.menuBar().addMenu('&Help')
        self.helpMenu.addAction(self.aboutAction)

    def _toolbar(self):

        # File: toolbar
        self.fileToolBar = QToolBar('File')
        self.fileToolBar.setMovable(False)
        self.fileToolBar.addAction(self.newAction)
        self.addToolBar(Qt.LeftToolBarArea, self.fileToolBar)

        # # Edit: toolbar
        # self.editToolBar = QToolBar('Edit')
        # self.editToolBar.setMovable(False)
        # self.editToolBar.addAction(self.editAction)
        # self.addToolBar(Qt.LeftToolBarArea, self.editToolBar)

        # Delete: toolbar
        self.deleteToolBar = QToolBar('Delete')
        self.deleteToolBar.setMovable(False)
        self.deleteToolBar.addAction(self.deleteAction)
        self.addToolBar(Qt.LeftToolBarArea, self.deleteToolBar)

        # Refresh: toolbar
        self.refreshToolBar = QToolBar('Refresh')
        self.refreshToolBar.setMovable(False)
        self.refreshToolBar.addAction(self.refreshAction)
        self.addToolBar(Qt.LeftToolBarArea, self.refreshToolBar)

    def _statusbar(self):

        # temp, normal, permanent
        self.statusbar = self.statusBar()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbar.addPermanentWidget(self.statusNormalLabel)
        self.statusbar.showMessage('Ready', 7000)

    def check_REST_API(self):

        # [] TODO: always check the API if active or not every 2-3 minutes
        try:
            timestamp = sammy.as_of()
            self.statusNormalLabel.setText('Online')
            print(timestamp)
        except Exception as e:
            self.statusNormalLabel.setText('Offline')
            print(e)

    def _connections(self):

        self.stockmonitoringTableView.clicked.connect(self.on_stockmonitoringTableView_clicked)

    def _read_settings(self):

        settings = QSettings('CodersGym', 'Sammy')
        self.restoreGeometry(settings.value('sammy_geometry', self.saveGeometry()))
        self.restoreState(settings.value('sammy_state', self.saveState()))
        companies = settings.value('COMPANIES', COMPANIES)

        # Reload previously monitored companies
        for raw_quote in companies:
            self.decide(raw_quote['symbol'],
                        raw_quote['buy_below'],
                        raw_quote['target_price'],
                        raw_quote['remarks'])

    # [x] TODO: self.companies doesn't update when the user edit something in the table
    def _write_settings(self):

        settings = QSettings('CodersGym', 'Sammy')
        settings.setValue('sammy_geometry', self.saveGeometry())
        settings.setValue('sammy_state', self.saveState())
        settings.setValue('COMPANIES', COMPANIES)

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
                         'target_price': target_price,
                         'remarks': ''}

            self.decide(raw_quote['symbol'],
                        raw_quote['buy_below'],
                        raw_quote['target_price'],
                        raw_quote['remarks'])

    def on_edit_action(self):

        print('TODO: editing?')
        import sammy
        all_stocks = sammy.stocks()
        print(all_stocks)

    # [] TODO: you are struggling how to remove a single row in your table T_T
    def on_delete_action(self):

        index = self.stockmonitoringTableView.currentIndex()
        row = index.row()
        col = index.column()

        # 2, 0
        print('cell:', row, col)
        print(len(RECORD))
        # Remove selected row base on current selected cell
        self.stock_table_model.removeRows(row, len(RECORD))
        self.stockmonitoringTableView.setModel(self.stock_table_model)

        print('delete {0} {1}?'.format(row, col))

    # [] TODO: successfully packaging the output in the terminal, needs to show it on the main table
    def on_refresh_action(self) -> None:
        """ Reload monitored companies. """

        # [x] TODO: remove records in the table
        # [x] TODO: get all_stocks

        import sammy
        all_stocks = sammy.stocks()

        print(COMPANIES)

        # Remove first the rows in the table
        self.stock_table_model.removeRows(0, len(RECORD))
        self.stockmonitoringTableView.setModel(self.stock_table_model)
        RECORD.clear()

        # nested for loop
        for raw_quote in COMPANIES:
            for stock in all_stocks['stock']:
                if raw_quote['symbol'] == stock['symbol']:
                    # Parse to get necessary values
                    company = stock['name']
                    symbol = stock['symbol']
                    price = stock['price']['amount']
                    change = stock['percent_change']

                    # Determine what action to follow
                    if price < raw_quote['buy_below']:
                        action = 'Buy'
                    elif raw_quote['buy_below'] <= price < raw_quote['target_price']:
                        action = 'Hold'
                    elif price >= raw_quote['target_price']:
                        action = 'Sell'

                    # Package retrieved values
                    RAW_RECORD['company'] = company
                    RAW_RECORD['symbol'] = symbol
                    RAW_RECORD['price'] = '{0} ({1})'.format(price, change)
                    RAW_RECORD['BB'] = raw_quote['buy_below']
                    RAW_RECORD['TP'] = raw_quote['target_price']
                    RAW_RECORD['action'] = action
                    RAW_RECORD['remarks'] = raw_quote['remarks']

                    # Transfer packed record to the table model
                    RECORD.append(list(RAW_RECORD.values()))
                    self.stock_table_model.insertRows(len(RECORD), 1)
                    self.stockmonitoringTableView.setModel(self.stock_table_model)

                    print(RAW_RECORD)

        print('refreshed!')

    def on_stockmonitoringTableView_clicked(self):

        #print('cell')
        pass

    def on_aboutAction_clicked(self):

        QMessageBox.about(self, 'About Sammy', ABOUT)

    # [] TODO: for cleaning, this is ugly
    def decide(self, stock_code, buy_below, target_price, remarks):

        try:
            # Perform query to Phisix API
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
            RAW_RECORD['remarks'] = remarks

            # Transfer packed record to the table model
            RECORD.append(list(RAW_RECORD.values()))
            self.stock_table_model.insertRows(len(RECORD), 1)
            self.stockmonitoringTableView.setModel(self.stock_table_model)

            # Display market time
            self.statusbar.showMessage('Market price as of {}'.format(as_of))

            # Update self.companies with 'remarks'
            raw_quote = {'symbol': stock_code,
                         'buy_below': buy_below,
                         'target_price': target_price,
                         'remarks': remarks}
            COMPANIES.append(raw_quote)

        except Exception as e:
            self.statusbar.showMessage('Last request to API failed, try again or press F5 to refresh', 7000)
            print(e)

    def closeEvent(self, e):

        self._write_settings()



