# coding: utf-8

import PySide2
import typing
from PySide2 import QtWidgets, QtCore, QtGui


class TestItem:

    def __init__(self, data, parent=None):
        self._data = data
        self._parent = parent
        if parent:
            parent.appendChild(self)
        self._child = list()

    def appendChild(self, item):
        self._child.append(item)

    def child(self, row):
        if row < 0 or row >= len(self._child):
            return None
        return self._child[row]

    def childCount(self):
        return len(self._child)

    def columnCount(self):
        return len(self._data)

    def data(self, column, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[column]
        if role == QtCore.Qt.UserRole:
            return "UserRoleData"
        return None

    def parentItem(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._child.index(self)
        return None


class TestModel(QtCore.QAbstractItemModel):

    def __init__(self):
        super(TestModel, self).__init__()
        self._root = TestItem(["Type", "Name", "Version", "Notes"])
        data = list()
        data.append(["a", "kim", "001", "no"])
        data.append(["a", "kim", "002", "no"])
        data.append(["b", "han", "001", "no"])
        data.append(["c", "cho", "001", "no"])
        self.setupData(data)

    def index(self, row: int, column: int, parent: PySide2.QtCore.QModelIndex = ...) -> PySide2.QtCore.QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        parent_item = self._root if not parent.isValid() else parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index) -> PySide2.QtCore.QObject:
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parentItem()
        if parent_item == self._root:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self._root.columnCount()

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.UserRole:
            return index.internalPointer().data(index.column(), role)

    def flags(self, index: PySide2.QtCore.QModelIndex) -> PySide2.QtCore.Qt.ItemFlags:
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return super(TestModel, self).flags(index)

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._root.data(section, role)
        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0
        parent_item = self._root if not parent.isValid() else parent.internalPointer()
        return parent_item.childCount()

    def setupData(self, data):
        parent = self._root
        for i in range(4):
            parent = TestItem([i, i, i, i], parent)


def sel_item(self):
    print(self)
    print(self.data(role=QtCore.Qt.UserRole))


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    treeview = QtWidgets.QTreeView()
    model = TestModel()
    treeview.setModel(model)
    treeview.clicked.connect(sel_item)
    treeview.show()

    app.exec_()
