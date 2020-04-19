from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import QAbstractTableModel, Qt

from gui import main
from lib import databaseOperations
from lib import table1Operations, table2Operations, table3Operations

global current_row

"""
        tableview Init
        """


class PythonMongoDB(main.Ui_MainWindow, QtWidgets.QMainWindow):

    def return_current_row(self, row):
        """

        :rtype: object
        """
        global current_row
        current_row = 1
        row1 = current_row
        for index in sorted(self.tableView.selectionModel().selectedRows()):
            row1 = index.row()
        row1 = row
        print(row)
        return row




    def __init__(self):
        super(PythonMongoDB, self).__init__()
        self.setupUi(self)
        # data = {'photo': ":/icons/images/photo.jpg",  'name': 'rajiv'}
        # databaseOperations.insert_data(data)
        self.user_data = databaseOperations.get_multiple_data()
        self.model1 = table1Operations.CustomTable1Model(self.user_data)
        self.model2 = table2Operations.CustomTable2Model(self.user_data)
        self.model3 = table3Operations.CustomTable3Model(self.user_data)
        self.delegate = table1Operations.InLineEditDelegate()
        self.delegate2 = table2Operations.InLineEditDelegate()
        self.tableView.setModel(self.model1)
        self.tableView.setItemDelegate(self.delegate)
        self.tableView_2.setItemDelegate(self.delegate2)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.context_menu)
        self.tableView_2.customContextMenuRequested.connect(self.context_menu)
        self.tableView.customContextMenuRequested.connect(self.return_current_row)
        self.tableView_2.customContextMenuRequested.connect(self.return_current_row)
        self.tableView.verticalHeader().setDefaultSectionSize(50)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.hideColumn(0)

    """
           Add CRUD implementation
            """

    def context_menu(self):
        menu = QtWidgets.QMenu()
        add_data = menu.addAction("Add New Data")
        refresh = menu.addAction("View")
        refresh.triggered.connect(lambda: self.tableView_2.updateEditorData())
        refresh.triggered.connect(lambda: self.tableView_2.setModel(self.model2))
        add_data.triggered.connect(lambda: self.model1.insertRows())
        remove_data = menu.addAction("Remove Data")
        remove_data.triggered.connect(lambda: self.model1.removeRows(self.tableView.currentIndex()))
        self.tableView_2.setModel(self.model3)
        self.tableView_3.setModel(self.model3)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


if __name__ == '__main__':
    global current_row

    app = QtWidgets.QApplication([])

    my_app = PythonMongoDB()

    my_app.show()
    app.exec_()
