from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtCore import QAbstractTableModel, Qt
from lib import databaseOperations

class CustomTable3Model(QtCore.QAbstractTableModel):
    """
    Custom Table Model to handle MongoDB Data
    """

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self.user_data = data
        self.columns = list(self.user_data[0])[0:4]

    def flags(self, index):
        """
        Make table editable.
        make first column non editable
        :param index:
        :return:
        """
        if index.column() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif index.column() == 1:
            return QtCore.Qt.DecorationRole
        else:
            return QtCore.Qt.ItemIsSelectable

    def rowCount(self, *args, **kwargs):
        """
        set row counts
        :param args:
        :param kwargs:
        :return:
        """
        return len(self.user_data)

    def columnCount(self, *args, **kwargs):
        """
        set column counts
        :param args:
        :param kwargs:
        :return:
        """
        return 7

    header_labels = ['id', '50-Day Low', '50-Day Low', '200S SMA', 'Performance (YTD)', 'Performance (Weekly)',
                     'Performance (Quarter)']

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role):
        """
        Display Data in table cells
        :param index:
        :param role:
        :return:
        """
        column = self.columns[1]
        row = self.user_data[index.row()]
        row1 = index.row()
        try:
            if index.column() == 1:
                selected_row = self.user_data[row1]
                company = selected_row['50-Day Low']
                return company
            if index.column() == 2:
                selected_row = self.user_data[row1]
                ticker = selected_row['50-Day High']
                return ticker
            if index.column() == 3:
                selected_row = self.user_data[row1]
                ticker = selected_row['200-Day Simple Moving Average']
                return ticker
            if index.column() == 4:
                selected_row = self.user_data[row1]
                company = selected_row['Performance (YTD)']
                return company
            if index.column() == 5:
                selected_row = self.user_data[row1]
                ticker = selected_row['Performance (Week)']
                return ticker
            if index.column() == 6:
                selected_row = self.user_data[row1]
                ticker = selected_row['Performance (Quarter)']
                return ticker
            elif role == QtCore.Qt.DisplayRole:
                return str(row[column])
        except KeyError:
            return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Edit data in table cells
        :param index:
        :param value:
        :param role:
        :return:
        """
        if index.isValid():
            selected_row = self.user_data[index.row()]
            selected_column = self.columns[index.column()]
            selected_row[selected_column] = value
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
            ok = databaseOperations.update_existing(selected_row['_id'], selected_row)
            if ok:
                return True
        return False

    """
            Function to insert rows
            """

    def insertRows(self):

        """
                Insert data in table cells

                """
        row_count = len(self.user_data)
        self.beginInsertRows(QtCore.QModelIndex(), row_count, row_count)
        empty_data = {key: None for key in self.columns if not key == '_id'}
        document_id = databaseOperations.insert_data(empty_data)
        new_data = databaseOperations.get_single_data(document_id)
        self.user_data.append(new_data)
        row_count += 1
        self.endInsertRows()
        return True

    """
        Function to remove rows
            """

    def removeRows(self, position):
        """
                Remove data in table cells
                :param position:
                """
        row_count = self.rowCount()
        row_count -= 1
        self.beginRemoveRows(QtCore.QModelIndex(), row_count, row_count)
        row_id = position.row()
        document_id = self.user_data[row_id]['_id']
        databaseOperations.remove_data(document_id)
        self.user_data.pop(row_id)
        self.endRemoveRows()
        return True

