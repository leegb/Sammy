# Models

from PyQt5.QtCore import (Qt,
                          QModelIndex,
                          QAbstractTableModel,  # for table
                          QAbstractListModel)   # for list
from resources.constant import (COMPANIES,
                                RECORD)


# [x] TODO: make the Remarks column editable
class StockMonitoringTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.header = ['Company', 'Symbol', 'Market Price', 'Buy Below', 'Target Price', 'Action', 'Remarks']

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]

    def data(self, index, role):

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            value = RECORD[row][col]
            return value

        if role == Qt.EditRole:
            return RECORD[row][col]

    def setData(self, index, value, role=Qt.DisplayRole):

        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            RECORD[row][col] = value
            COMPANIES[row]['remarks'] = value
            print(COMPANIES)
            return True

    def flags(self, index):

        col = index.column()
        if col == 6:    # Make the 'Remarks' column editable only
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):

        return len(RECORD)

    def columnCount(self, parent):

        return len(self.header)

    def insertRows(self, position, rows, parent=QModelIndex()):

        self.beginInsertRows(parent, position, position + rows - 1)
        # Still works!
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):

        self.beginRemoveRows(parent, position, position + rows - 1)
        # Perform removal of values in your internal list
        self.endRemoveRows()
        return True


# TODO: have a good mechanism and naming convention for your models
class StockListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__stock_symbols = ['FGEN', 'MEG', 'COSCO', 'MBT', 'CEB', 'MPI']
        self.__stock_symbols.sort()

    def data(self, index, role):

        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__stock_symbols[row]
            return value

    def rowCount(self, parent):

        return len(self.__stock_symbols)

