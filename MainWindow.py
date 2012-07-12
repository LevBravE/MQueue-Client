# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import sys

from PySide import QtCore, QtGui
from DialogSettings import DialogSettings
from DialogLogin import DialogLogin
from SynchronizationServerThread import SynchronizationServerThread
from SynchronizationSessionThread import SynchronizationSessionThread
from SynchronizationCountThread import SynchronizationCountThread

#**************************************************************************************************
# class: MainWindow
#**************************************************************************************************

class MainWindow(QtGui.QMainWindow):
    """
    Главное окно
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.__APPLICATION_CORP = 'LevCorp'
        self.__APPLICATION_NAME = 'MQueue-Client'
        self.__VERSION = '1.0'
        self.__dataBase = None
        self.__session = None
        self.__sessionClient = False
        self.__userId = None
        self.__serviceId = None
        self.__clientId = None
        self.__flagSession = False
        self.__lastSession = None
        # Thread
        self.__synchronizationServerThread = SynchronizationServerThread()
        self.__synchronizationSessionThread = SynchronizationSessionThread()
        self.__synchronizationCountThread = SynchronizationCountThread()
        # Timer
        self.__synchronizationTimer = QtCore.QTimer()
        self.__synchronizationCountTimer = QtCore.QTimer()
        # Label
        self.__userLabel = QtGui.QLabel()

        self.__infoLabel = QtGui.QLabel()

        self.__imageCentralLabel = QtGui.QLabel()
        self.__imageCentralLabel.setPixmap('img/MQClientApp.png')

        self.__statusMQueueDataBase = QtGui.QLabel()
        self.__statusMQueueDataBase.setAlignment(QtCore.Qt.AlignHCenter)

        self.__statusMQueueSession = QtGui.QLabel()
        self.__statusMQueueSession.setAlignment(QtCore.Qt.AlignHCenter)
        # PushButton
        self.__nextClientPushButton = QtGui.QPushButton(self.tr('Следующий'))
        self.__finishClientPushButton = QtGui.QPushButton(self.tr('Завершить'))
        # SystemTrayIcon
        self.__systemTrayIcon = QtGui.QSystemTrayIcon()
        self.__systemTrayIcon.setIcon(QtGui.QIcon('img/MQLogo.png'))
        self.__systemTrayIcon.show()
        # Layout
        self.__layoutHButton = QtGui.QHBoxLayout()
        self.__layoutHButton.addWidget(self.__nextClientPushButton)
        self.__layoutHButton.addWidget(self.__finishClientPushButton)

        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(self.__userLabel)
        self.__layoutVMain.addWidget(self.__infoLabel)
        self.__layoutVMain.addWidget(self.__imageCentralLabel)
        self.__layoutVMain.addLayout(self.__layoutHButton)
        # Widget
        self.__centralWidget = QtGui.QWidget()
        self.__centralWidget.setLayout(self.__layoutVMain)
        # Functions
        self._createActions()
        self._createToolBars()
        self._createMenus()
        self._createStatusBar()
        self._synchronizationAutoServer()
        self._readSettings()
        # Connect
        self.__synchronizationServerThread.finished.connect(self._checkAvailabilityServer)
        self.__synchronizationServerThread.finished.connect(self._userLogin)
        self.__synchronizationSessionThread.finished.connect(self._checkAvailabilitySession)
        self.__synchronizationCountThread.finished.connect(self._checkCount)

        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoServer)
        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoSession)
        self.__synchronizationCountTimer.timeout.connect(self._synchronizationAutoCount)

        self.__nextClientPushButton.clicked.connect(self._nextClient)
        self.__finishClientPushButton.clicked.connect(self._finishClient)
        # Timer every 0.2 sec
        self.__synchronizationTimer.start(5000)
        # <<<Self>>>
        self.setWindowTitle('%s %s' % (self.__APPLICATION_NAME, self.__VERSION))
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setCentralWidget(self.__centralWidget)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

    def _createActions(self):
        # Action File
        self.__actionFileNextClient = QtGui.QAction(QtGui.QIcon('img/black/png/arrow_right_icon&16.png'),
            self.tr('&Следующий'), self, shortcut='Ctrl+Alt+N',
            statusTip=self.tr('Принять следующего клиента'), triggered=self._nextClient)

        self.__actionFileFinishClient = QtGui.QAction(QtGui.QIcon('img/black/png/flag_icon&16.png'),
            self.tr('&Завершить'), self, shortcut='Ctrl+Alt+Q',
            statusTip=self.tr('Завершить работу с клиентом'), triggered=self._finishClient)

        self.__actionFileSettingClient = QtGui.QAction(QtGui.QIcon('img/black/png/wrench_plus_2_icon&16.png'),
            self.tr('&Настройки'), self, shortcut='Ctrl+Alt+S',
            statusTip=self.tr('Настройки терминала'), triggered=self._settingTerminal)

        self.__actionFileExit = QtGui.QAction(
            self.tr('В&ыход'), self, shortcut=QtGui.QKeySequence.Quit,
            statusTip=self.tr('Выйти из программы'), triggered=self.close)
        # Action Help
        self.__actionHelpAbout = QtGui.QAction(
            self.tr('&О программе'), self,
            statusTip=self.tr('Показать информацию о программе'), triggered=self._about)

        self.__actionFileNextClient.setEnabled(False)
        self.__actionFileFinishClient.setEnabled(False)
        self.__nextClientPushButton.setEnabled(False)
        self.__finishClientPushButton.setEnabled(False)

    def _createToolBars(self):
        self.__toolBar = self.addToolBar(self.tr('Панель инструментов'))
        self.__toolBar.setMovable(False)
        self.__toolBar.addAction(self.__actionFileNextClient)
        self.__toolBar.addAction(self.__actionFileFinishClient)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionFileSettingClient)

    def _createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('&Файл'))
        fileMenu.addAction(self.__actionFileNextClient)
        fileMenu.addAction(self.__actionFileFinishClient)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileSettingClient)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileExit)

        helpMenu = self.menuBar().addMenu(self.tr('&Помощь'))
        helpMenu.addAction(self.__actionHelpAbout)

    def _createStatusBar(self):
        self.statusBar().showMessage(self.tr('Готово'))
        self.statusBar().addPermanentWidget(self.__statusMQueueSession)
        self.statusBar().addPermanentWidget(self.__statusMQueueDataBase)

    def _readSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        pos = settings.value('pos', QtCore.QPoint(200, 100))
        size = settings.value('size', QtCore.QSize(400, 200))

        self.resize(size)
        self.move(pos)

    def _writeSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def _userLogin(self):
        self.__synchronizationServerThread.finished.disconnect(self._userLogin)

        if self.__dataBase:
            dialogLogin = DialogLogin(self.tr('Вход'), self.__dataBase)
            if dialogLogin.exec_() == QtGui.QDialog.Accepted:
                self.__userId = dialogLogin._userId()
                self.__userLabel.setText(self.tr('Сотрудник: %s' % dialogLogin._userName()))
                self.__serviceId = dialogLogin._serviceId()
                self.__synchronizationCountTimer.start(5000)

                cursor = self.__dataBase.cursor()
                cursor.execute('SELECT `client`.`id`, `client`.`number` FROM `mqueuedb`.`client` '
                               'WHERE `client`.`served` = 0 AND `client`.`call` = 1 AND `client`.`service_id` = %s '
                               'AND `client`.`user_id` = %s' % (self.__serviceId, self.__userId))
                self.__dataBase.commit()
                client = cursor.fetchone()
                if client:
                    self.__synchronizationCountTimer.stop()

                    self.__clientId = client[0]
                    clientNumber = client[1]

                    self.__infoLabel.setText(self.tr('Обслуживание клиента - %s') % clientNumber)

                    self.__sessionClient = True
                    self.__actionFileNextClient.setEnabled(False)
                    self.__actionFileFinishClient.setEnabled(True)
                    self.__nextClientPushButton.setEnabled(False)
                    self.__finishClientPushButton.setEnabled(True)
            else:
                sys.exit(1)
        else:
            QtGui.QMessageBox.warning(self, self.tr('Предупреждение'),
                self.tr('Сервер базы данных, недоступен'))


    def _nextClient(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT client.id, client.number FROM mqueuedb.client '
                       'WHERE client.served = 0 AND client.call = 0 AND client.service_id = %s '
                       'AND ( client.user_id = %s OR client.user_id IS NULL )' % (self.__serviceId, self.__userId))
        self.__dataBase.commit()
        client = cursor.fetchone()
        if client:
            self.__synchronizationCountTimer.stop()
            self.__clientId = client[0]
            clientNumber = client[1]

            dateTime = QtCore.QDateTime().currentDateTime().toString(QtCore.Qt.ISODate)

            cursor.execute('UPDATE `mqueuedb`.`client` SET `start_time`="%s", `call`="1", `user_id`="%s" '
                           'WHERE `id`="%s"' % (dateTime, self.__userId, self.__clientId))
            self.__dataBase.commit()

            self.__infoLabel.setText(self.tr('Обслуживание клиента - %s') % clientNumber)

            self.__sessionClient = True
            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileFinishClient.setEnabled(True)
            self.__nextClientPushButton.setEnabled(False)
            self.__finishClientPushButton.setEnabled(True)

    def _finishClient(self):
        self.__synchronizationCountTimer.start(3000)

        cursor = self.__dataBase.cursor()

        dateTime = QtCore.QDateTime().currentDateTime().toString(QtCore.Qt.ISODate)

        cursor.execute('UPDATE `mqueuedb`.`client` SET `finish_time`="%s", `served`="1" WHERE `id`="%s"' % (dateTime, self.__clientId))
        self.__dataBase.commit()

        self.__sessionClient = False
        self.__actionFileNextClient.setEnabled(False)
        self.__actionFileFinishClient.setEnabled(False)
        self.__nextClientPushButton.setEnabled(False)
        self.__finishClientPushButton.setEnabled(False)

    def _settingTerminal(self):
        """
        Настройки приложения
        """
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        host = settings.value('address', '127.0.0.1')
        user = settings.value('user', 'mqueueclient')
        password = settings.value('password', 'mfc1002dog')
        port = settings.value('port', '3306')

        dialogSettings = DialogSettings(self.tr('Настройки'))
        dialogSettings._setHostLineEdit(host)
        dialogSettings._setUserLineEdit(user)
        dialogSettings._setPasswordLineEdit(password)
        dialogSettings._setPortLineEdit(port)

        if dialogSettings.exec_() == QtGui.QDialog.Accepted:
            settings.setValue('address', dialogSettings._hostLineEdit())
            settings.setValue('user', dialogSettings._userLineEdit())
            settings.setValue('password', dialogSettings._passwordLineEdit())
            settings.setValue('port', dialogSettings._portLineEdit())
            dialogSettings.close()

    def closeEvent(self, event):
        """
        Обработка события выхода из программы
        """
        ok = QtGui.QMessageBox.question(self, self.tr('Завершение программы'),
            self.tr('Завершить программу %s?' % self.__APPLICATION_NAME),
            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)

        if ok == QtGui.QMessageBox.Ok:
            #self._writeSettings()
            event.accept()
        else:
            event.ignore()

    def _about(self):
        """
        О программе
        """
        QtGui.QMessageBox.about(self, self.tr('О программе'),
            self.tr('Программа <u>MQueue-Client</u> является частью '
                    'системы MQueue. Предназначенна для выполнения '
                    'функции клиента.\n'
                    '<p><b><i>LevBravE</i></b> специально для МФЦ'))

    def _synchronizationAutoServer(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        host = settings.value('address', '127.0.0.1')
        user = settings.value('user', 'mqueueclient')
        password = settings.value('password', 'mfc1002dog')
        port = settings.value('port', '3306')

        self.__synchronizationServerThread._setHost(host)
        self.__synchronizationServerThread._setUser(user)
        self.__synchronizationServerThread._setPassword(password)
        self.__synchronizationServerThread._setPort(port)
        self.__synchronizationServerThread.start()

    def _checkAvailabilityServer(self):
        self.__dataBase = self.__synchronizationServerThread._response()

        if self.__dataBase:
            strStatusMQueueDataBase = self.tr('<p style="font-size: 12px"> '
                                              '<img width="11" height="11" src="img/circle_green.png"> База данных</p>')
            self.__statusMQueueDataBase.setText(strStatusMQueueDataBase)
            self.__statusMQueueDataBase.setToolTip(self.tr('Сервер базы данных, доступен'))

            return True
        else:
            strStatusMQueueDataBase = self.tr('<p style="font-size: 12px"> '
                                              '<img width="11" height="11" src="img/circle_red.png"> База данных</p>')
            self.__statusMQueueDataBase.setText(strStatusMQueueDataBase)
            self.__statusMQueueDataBase.setToolTip(self.tr('Сервер базы данных, недоступен'))

            return False

    def _synchronizationAutoSession(self):
        self.__synchronizationSessionThread._setDataBase(self.__dataBase)
        self.__synchronizationSessionThread.start()

    def _checkAvailabilitySession(self):
        self.__session = self.__synchronizationSessionThread._response()

        if self.__lastSession != self.__session:
            self.__lastSession = self.__session
            self.__flagSession = False


        if self.__session:
            strStatusMQueueSession = self.tr('<p style="font-size: 12px"> '
                                             '<img width="11" height="11" src="img/circle_green.png"> Сессия</p>')
            self.__statusMQueueSession.setText(strStatusMQueueSession)
            self.__statusMQueueSession.setToolTip(self.tr('Сессия начата'))

            return True
        else:
            strStatusMQueueSession = self.tr('<p style="font-size: 12px"> '
                                             '<img width="11" height="11" src="img/circle_red.png"> Сессия</p>')
            self.__statusMQueueSession.setText(strStatusMQueueSession)
            self.__statusMQueueSession.setToolTip(self.tr('Сессия завершена'))

            return False

    def _synchronizationAutoCount(self):
        self.__synchronizationCountThread._setDataBase(self.__dataBase)
        self.__synchronizationCountThread._setServiceId(self.__serviceId)
        self.__synchronizationCountThread._setUserId(self.__userId)
        self.__synchronizationCountThread.start()

    def _checkCount(self):
        if self.__session:
            lstClients = self.__synchronizationCountThread._response()

            if lstClients:
                self.__infoLabel.setText(self.tr('Количество людей в очереди - %s') % len(lstClients))
                if not self.__sessionClient and not self.isActiveWindow():
                    QtGui.QApplication.alert(self)
                    self.__systemTrayIcon.showMessage(
                        self.tr('Внимание! Очередь...'),
                        self.tr('Количество людей в очереди - %s') % len(lstClients))
                else:
                    self.__actionFileNextClient.setEnabled(False)
                    self.__actionFileFinishClient.setEnabled(True)
                    self.__nextClientPushButton.setEnabled(False)
                    self.__finishClientPushButton.setEnabled(True)

            elif not self.__sessionClient:
                self.__infoLabel.setText(self.tr('Количество людей в очереди - .:пусто:. '))
                self.__actionFileNextClient.setEnabled(False)
                self.__actionFileFinishClient.setEnabled(False)
                self.__nextClientPushButton.setEnabled(False)
                self.__finishClientPushButton.setEnabled(False)

            if lstClients and not self.__sessionClient:
                self.__actionFileNextClient.setEnabled(True)
                self.__actionFileFinishClient.setEnabled(False)
                self.__nextClientPushButton.setEnabled(True)
                self.__finishClientPushButton.setEnabled(False)
        else:
            self.__infoLabel.setText(self.tr('Сессия не начата...'))
            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileFinishClient.setEnabled(False)
            self.__nextClientPushButton.setEnabled(False)
            self.__finishClientPushButton.setEnabled(False)


