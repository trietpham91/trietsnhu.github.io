from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from gui import main
from lib import databaseOperations
from lib import customModel

"""
        tableview Init
        """


class PythonMongoDB(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(PythonMongoDB, self).__init__()
        self.setupUi(self)

        # data = {'photo': ":/icons/images/photo.jpg",  'name': 'rajiv'}
        # databaseOperations.insert_data(data)
        self.user_data = databaseOperations.get_multiple_data()
        self.user_data = databaseOperations.get_multiple_data()
        self.model1 = customModel.CustomTable1Model(self.user_data)
        self.model2 = customModel.CustomTable2Model(self.user_data)
        self.delegate = customModel.InLineEditDelegate()
        self.tableView.setModel(self.model1)
        self.tableView.setItemDelegate(self.delegate)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.context_menu)
        self.tableView.verticalHeader().setDefaultSectionSize(50)
        self.tableView.setColumnWidth(0, 100)
        self.tableView.hideColumn(0)

    """
           Add CRUD implementation
            """

    def context_menu(self):
        menu = QtWidgets.QMenu()
        add_data = menu.addAction("Add New Data")
        add_data.triggered.connect(lambda: self.model1.insertRows())
        for index in sorted(self.tableView.selectionModel().selectedRows()):
            row = index.row
            selected_row = self.user_data[index.row()]
            print(selected_row)
            self.tableView_2.currentIndex()
            print(self.tableView_2.currentIndex())
            self.tableView_2.setModel(self.model2)
            remove_data = menu.addAction("Remove Data")
            remove_data.triggered.connect(lambda: self.model1.removeRows(self.tableView.currentIndex()))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    my_app = PythonMongoDB()
    my_app.show()
    app.exec_()
