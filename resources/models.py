# Models

from PyQt5.QtCore import (Qt,
                          QModelIndex,
                          QAbstractTableModel)


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

        return 5

    def columnCount(self, parent):

        return 7
