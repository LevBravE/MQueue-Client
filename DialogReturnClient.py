# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtGui
from FrameSeparator import FrameSeparator

#**************************************************************************************************
# class: DialogReturnClient
#**************************************************************************************************

class DialogReturnClient(QtGui.QDialog):
    """
    Диалоговое окно возвращения клиента очереди
    """
    def __init__(self, title, dataBase):
        QtGui.QDialog.__init__(self)
        self.__dataBase = dataBase
        self.__clientId = None
        self.__userId = None
        self.__serviceId = None
        # ComboBox
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `service`.`id`, `service`.`name` FROM `mqueuedb`.`service`')
        self.__dataBase.commit()
        lstService = cursor.fetchall()

        self.__serviceComboBox = QtGui.QComboBox()
        for index, item in enumerate(lstService):
            self.__serviceComboBox.insertItem(index, self.tr(item[1]), item[0])

        self.__userComboBox = QtGui.QComboBox()
        # Button
        strStyleSheetMePushButton = 'QPushButton { '\
                                    'border: 1px solid silver; '\
                                    'border-radius: 3px; '\
                                    'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde); '\
                                    'min-width: 80px; '\
                                    'padding: 3px;} '\
                                    'QPushButton:enabled { '\
                                    'font: bold; '\
                                    'color: green;} '\
                                    'QPushButton:hover { '\
                                    'border: 1px solid #3CB371;} '\
                                    'QPushButton:pressed { '\
                                    'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}'

        self.__meReturnClientPushButton = QtGui.QPushButton(self.tr('Ко мне в очередь'))
        self.__meReturnClientPushButton.setStyleSheet(strStyleSheetMePushButton)

        self.__dialogButtonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.__dialogButtonBox.addButton(self.__meReturnClientPushButton, QtGui.QDialogButtonBox.ActionRole)
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Выберите, если хотите перенаправить клиента по другой услуге:')))
        self.__layoutVMain.addWidget(self.__serviceComboBox)
        self.__layoutVMain.addWidget(QtGui.QLabel(self.tr('Выберите, если хотите перенаправить клиента к определенному сотруднику:')))
        self.__layoutVMain.addWidget(self.__userComboBox)
        self.__layoutVMain.addWidget(FrameSeparator(QtGui.QFrame.HLine, QtGui.QFrame.Sunken))
        self.__layoutVMain.addWidget(self.__dialogButtonBox)
        # Connect
        self.__serviceComboBox.currentIndexChanged.connect(self._serviceCurrentIndex)

        self.__meReturnClientPushButton.clicked.connect(self._meReturnClient)

        self.__dialogButtonBox.accepted.connect(self._accept)
        self.__dialogButtonBox.rejected.connect(self.reject)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)

    # set (start)
    def _setClientId(self, clientId):
        self.__clientId = clientId

    def _setUserId(self, userId):
        self.__userId = userId

    def _setServiceId(self, serviceId):
        self.__serviceId = serviceId
        currentIndex = self.__serviceComboBox.findData(self.__serviceId)
        self.__serviceComboBox.setCurrentIndex(currentIndex)

    def _serviceCurrentIndex(self, index):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `user`.`id`, `user`.`name` FROM `mqueuedb`.`user` '
                       'WHERE `user`.`service_id`="%s" '
                       'AND `user`.`id`<>"%s"' % (self.__serviceComboBox.itemData(index), self.__userId))
        self.__dataBase.commit()
        lstUser = cursor.fetchall()

        self.__userComboBox.clear()
        self.__userComboBox.insertItem(0, self.tr('.::все сотрудники::.'))

        for index, item in enumerate(lstUser):
            self.__userComboBox.insertItem(index + 1, self.tr(item[1]), item[0])

    def _meReturnClient(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('UPDATE `mqueuedb`.`client` SET `start_time`="0000-00-00 00:00:00", `call`="0", `voice`="0" '
                       'WHERE `id`="%s"' % self.__clientId)
        self.__dataBase.commit()

        self.accept()

    def _accept(self):
        self.__serviceId = self.__serviceComboBox.itemData(self.__serviceComboBox.currentIndex())

        if not self.__userComboBox.currentIndex():
            self.__userId = 'NULL'
        else:
            self.__userId = self.__userComboBox.itemData(self.__userComboBox.currentIndex())

        cursor = self.__dataBase.cursor()
        cursor.execute('UPDATE `mqueuedb`.`client` SET `start_time`="0000-00-00 00:00:00", `call`="0", `voice`="0", '
                       '`user_id` = %s, `service_id`="%s" '
                       'WHERE `id`="%s"' % (self.__userId, self.__serviceId, self.__clientId))
        self.__dataBase.commit()

        self.accept()
