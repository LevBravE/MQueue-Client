# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogSettings
#**************************************************************************************************

class DialogSettings(QtGui.QDialog):
    """
    Диалоговое окно настройки приложения
    """
    def __init__(self, title):
        QtGui.QDialog.__init__(self)
        # LineEdit
        self.__hostLineEdit = QtGui.QLineEdit()
        self.__userLineEdit = QtGui.QLineEdit()
        self.__passwordLineEdit = QtGui.QLineEdit()
        self.__passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.__portLineEdit = QtGui.QLineEdit()
        # Button
        self.__dialogButtonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.RestoreDefaults | QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Адрес сервера - MySQL')))
        self.__layoutVMain.addWidget(self.__hostLineEdit)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Имя пользователя - MySQL')))
        self.__layoutVMain.addWidget(self.__userLineEdit)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Пароль пользователя - MySQL')))
        self.__layoutVMain.addWidget(self.__passwordLineEdit)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Порт сервера - MySQL')))
        self.__layoutVMain.addWidget(self.__portLineEdit)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__dialogButtonBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(self._reset)
        self.__dialogButtonBox.accepted.connect(self.accept)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)

    def _reset(self):
        self.__hostLineEdit.setText('127.0.0.1')
        self.__userLineEdit.setText('mqueueclient')
        self.__passwordLineEdit.setText('mfc1002dog')
        self.__portLineEdit.setText('3306')

    # get and set (start)
    def _hostLineEdit(self):
        return self.__hostLineEdit.text()

    def _userLineEdit(self):
        return self.__userLineEdit.text()

    def _passwordLineEdit(self):
        return self.__passwordLineEdit.text()

    def _portLineEdit(self):
        return self.__portLineEdit.text()

    def _setHostLineEdit(self, host):
        self.__hostLineEdit.setText(host)

    def _setUserLineEdit(self, user):
        self.__userLineEdit.setText(user)

    def _setPasswordLineEdit(self, password):
        self.__passwordLineEdit.setText(password)

    def _setPortLineEdit(self, port):
        self.__portLineEdit.setText(port)
    # get and set (end)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
    dialogSettings = DialogSettings(app.tr('Настройки'))
    sys.exit(dialogSettings.exec_())