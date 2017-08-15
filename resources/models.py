# Models

from PyQt5.QtCore import (Qt,
                          QModelIndex,
                          QAbstractTableModel,  # for table
                          QAbstractListModel)   # for list


class StockMonitoringTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.header = ['Company', 'Stock Code', 'Market Price', 'Buy Below', 'Target Price', 'Action', 'Remarks']

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]

    def data(self, index, role):

        pass

    def rowCount(self, parent):

        return 0

    def columnCount(self, parent):

        return 7


# TODO: have a good mechanism and naming convention for your models
class StockListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__stock_symbols = ['FGEN', 'CEB', 'MEG', 'COSCO']

    def data(self, index, role):

        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__stock_symbols[row]
            return value

    def rowCount(self, parent):

        return len(self.__stock_symbols)

