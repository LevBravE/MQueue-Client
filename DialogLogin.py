# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtGui
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogLogin
#**************************************************************************************************

class DialogLogin(QtGui.QDialog):
    """
    Диалоговое окно входа пользователя
    """
    def __init__(self, title, dataBase):
        QtGui.QDialog.__init__(self)
        self.__dataBase = dataBase
        self.__userId = None
        self.__userName = None
        self.__serviceId = None
        # LineEdit
        self.__loginLineEdit = QtGui.QLineEdit()
        self.__passwordLineEdit = QtGui.QLineEdit()
        self.__passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        # Button
        self.__dialogButtonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Логин пользователя')))
        self.__layoutVMain.addWidget(self.__loginLineEdit)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Пароль пользователя')))
        self.__layoutVMain.addWidget(self.__passwordLineEdit)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__dialogButtonBox.accepted.connect(self._verification)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)

    def _verification(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `user`.`id`, `user`.`login`, `user`.`password`, `user`.`service_id`, '
                       '`user`.`name`, `user`.`status`, `user`.`enable` '
                       'FROM `mqueuedb`.`user`')
        self.__dataBase.commit()
        lstUsers = cursor.fetchall()

        check = False

        for item in lstUsers:
            if self.__loginLineEdit.text() == item[1] and self.__passwordLineEdit.text() == item[2]:
                check = True

                if not int(item[6]):
                    QtGui.QMessageBox.information(self, self.tr('Ошибка входа'),
                        self.tr('Данный пользователь заблокирован'))
                elif not int(item[5]):
                    self.__userId = item[0]
                    self.__userName = item[4]
                    self.__serviceId = item[3]
                    cursor.execute('UPDATE `mqueuedb`.`user` SET `status`="1" '
                                   'WHERE `id`="%s"' % self.__userId)
                    self.__dataBase.commit()
                    self.accept()
                else:
                    QtGui.QMessageBox.information(self, self.tr('Ошибка входа'),
                        self.tr('Пользователь с таким логином уже находится в системе'))

        if not check:
            QtGui.QMessageBox.information(self, self.tr('Ошибка входа'),
                self.tr('Неверный логин или пароль'))

    # get and set (start)
    def _userId(self):
        return self.__userId

    def _userName(self):
        return self.__userName

    def _serviceId(self):
        return self.__serviceId