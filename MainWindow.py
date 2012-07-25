# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from DialogSettings import DialogSettings
from DialogLogin import DialogLogin
from DialogReturnClient import DialogReturnClient
from TimeLateLCDNumber import TimeLateLCDNumber
from SynchronizationServerThread import SynchronizationServerThread
from SynchronizationSessionThread import SynchronizationSessionThread
from SynchronizationCountThread import SynchronizationCountThread
from SynchronizationStatusThread import SynchronizationStatusThread

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
        self.__VERSION = '2.1'
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
        self.__synchronizationStatusThread = SynchronizationStatusThread()
        # Timer
        self.__synchronizationTimer = QtCore.QTimer()
        self.__synchronizationCountTimer = QtCore.QTimer()
        self.__synchronizationStatusTimer = QtCore.QTimer()
        # Label
        self.__userNameLabel = QtGui.QLabel()

        self.__imageCentralLabel = QtGui.QLabel()
        self.__imageCentralLabel.setPixmap('img/MQClientApp.png')

        self.__imageUserLabel = QtGui.QLabel()
        self.__imageUserLabel.setPixmap('img/user32x32.png')
        self.__imageUserLabel.setStatusTip(self.tr('Пользователь'))

        self.__imageClientLabel = QtGui.QLabel()
        self.__imageClientLabel.setPixmap('img/client32x32.png')
        self.__imageClientLabel.setStatusTip(self.tr('Номер клиента'))

        self.__imageClockLabel = QtGui.QLabel()
        self.__imageClockLabel.setPixmap('img/clock32x32.png')
        self.__imageClockLabel.setStatusTip(self.tr('Время обслуживания клиента'))

        self.__imageQueueLabel = QtGui.QLabel()
        self.__imageQueueLabel.setPixmap('img/queue32x32.png')
        self.__imageQueueLabel.setStatusTip(self.tr('Количество людей в очереди'))

        self.__statusMQueueDataBase = QtGui.QLabel()
        self.__statusMQueueDataBase.setAlignment(QtCore.Qt.AlignHCenter)

        self.__statusMQueueSession = QtGui.QLabel()
        self.__statusMQueueSession.setAlignment(QtCore.Qt.AlignHCenter)
        # Palette
        self.__paletteRed = QtGui.QPalette()
        self.__paletteRed.setBrush(QtGui.QPalette.Light, QtCore.Qt.red)

        self.__paletteGreen = QtGui.QPalette()
        self.__paletteGreen.setBrush(QtGui.QPalette.Light, QtCore.Qt.green)
        # LCDNumber
        self.__clientLCDNumber = QtGui.QLCDNumber(3)
        self.__clientLCDNumber.setFrameStyle(QtGui.QFrame.NoFrame)
        self.__clientLCDNumber.display('000')
        self.__clientLCDNumber.setPalette(self.__paletteRed)
        self.__clientLCDNumber.setStatusTip(self.tr('Номер клиента'))

        self.__countLCDNumber = QtGui.QLCDNumber(2)
        self.__countLCDNumber.setFrameStyle(QtGui.QFrame.NoFrame)
        self.__countLCDNumber.display(0)
        self.__countLCDNumber.setPalette(self.__paletteRed)
        self.__countLCDNumber.setStatusTip(self.tr('Количество людей в очереди'))
        # TimeLateLCDNumber
        self.__timeLateLCDNumber = TimeLateLCDNumber()
        self.__timeLateLCDNumber.setFrameStyle(QtGui.QFrame.NoFrame)
        self.__timeLateLCDNumber.display('00:00:00')
        self.__timeLateLCDNumber.setPalette(self.__paletteRed)
        self.__timeLateLCDNumber.setStatusTip(self.tr('Время обслуживания клиента'))
        # PushButton
        strStyleSheetLog = 'QPushButton { '\
                             'border: 1px solid #FFFACD; '\
                             'border-radius: 3px; '\
                             'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #E0FFFF); '\
                             'min-width: 30px; '\
                             'padding: 3px;} '\
                             'QPushButton:hover { '\
                             'border: 1px solid #FFFF00;} '\
                             'QPushButton:pressed { '\
                             'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}'

        strStyleSheetMePushButton = 'QPushButton { '\
                                  'border: 1px solid silver; '\
                                  'border-radius: 3px; '\
                                  'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde); '\
                                  'min-width: 80px; '\
                                  'min-height: 38px; '\
                                  'padding: 3px;} '\
                                  'QPushButton:enabled { '\
                                  'font: bold; '\
                                  'color: green;} '\
                                  'QPushButton:hover { '\
                                  'border: 1px solid #3CB371;} '\
                                  'QPushButton:pressed { '\
                                  'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}'

        strStyleSheetPushButton = 'QPushButton { ' \
                                  'border: 1px solid silver; ' \
                                  'border-radius: 3px; ' \
                                  'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde); ' \
                                  'min-width: 80px; ' \
                                  'min-height: 38px; ' \
                                  'padding: 3px;} ' \
                                  'QPushButton:hover { ' \
                                  'border: 1px solid #3CB371;} ' \
                                  'QPushButton:pressed { ' \
                                  'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}'

        self.__loginPushButton = QtGui.QPushButton()
        self.__loginPushButton.setIcon(QtGui.QIcon('img/login32x32.png'))
        self.__loginPushButton.setStyleSheet(strStyleSheetLog)
        self.__loginPushButton.setToolTip(self.tr('Войти'))
        self.__loginPushButton.setVisible(False)

        self.__logoutPushButton = QtGui.QPushButton()
        self.__logoutPushButton.setIcon(QtGui.QIcon('img/logout32x32.png'))
        self.__logoutPushButton.setStyleSheet(strStyleSheetLog)
        self.__logoutPushButton.setToolTip(self.tr('Выйти'))
        self.__logoutPushButton.setVisible(False)

        self.__nextClientMePushButton = QtGui.QPushButton(self.tr('Следующий ко мне'))
        self.__nextClientMePushButton.setStyleSheet(strStyleSheetMePushButton)
        self.__nextClientMePushButton.setEnabled(False)

        self.__nextClientPushButton = QtGui.QPushButton(self.tr('Следующий'))
        self.__nextClientPushButton.setStyleSheet(strStyleSheetPushButton)
        self.__nextClientPushButton.setEnabled(False)

        self.__returnClientPushButton = QtGui.QPushButton(self.tr('Вернуть в очередь'))
        self.__returnClientPushButton.setStyleSheet(strStyleSheetPushButton)
        self.__returnClientPushButton.setEnabled(False)

        self.__finishClientPushButton = QtGui.QPushButton(self.tr('Завершить'))
        self.__finishClientPushButton.setStyleSheet(strStyleSheetPushButton)
        self.__finishClientPushButton.setEnabled(False)
        # SystemTrayIcon
        self.__systemTrayIcon = QtGui.QSystemTrayIcon()
        self.__systemTrayIcon.setIcon(QtGui.QIcon('img/MQLogo.png'))
        self.__systemTrayIcon.show()
        # Layout
        self.__layoutVButton = QtGui.QVBoxLayout()
        self.__layoutVButton.addWidget(self.__nextClientMePushButton)
        self.__layoutVButton.addWidget(self.__nextClientPushButton)
        self.__layoutVButton.addWidget(self.__returnClientPushButton)
        self.__layoutVButton.addWidget(self.__finishClientPushButton)
        self.__layoutVButton.setAlignment(QtCore.Qt.AlignTop)

        self.__layoutHQueue = QtGui.QHBoxLayout()
        self.__layoutHQueue.addWidget(self.__imageClientLabel)
        self.__layoutHQueue.addWidget(self.__clientLCDNumber)
        self.__layoutHQueue.addStretch(10)
        self.__layoutHQueue.addWidget(self.__imageClockLabel)
        self.__layoutHQueue.addWidget(self.__timeLateLCDNumber)
        self.__layoutHQueue.addStretch(10)
        self.__layoutHQueue.addWidget(self.__imageQueueLabel)
        self.__layoutHQueue.addWidget(self.__countLCDNumber)
        self.__layoutHQueue.setAlignment(QtCore.Qt.AlignCenter)

        self.__layoutHUser = QtGui.QHBoxLayout()
        self.__layoutHUser.addWidget(self.__imageUserLabel)
        self.__layoutHUser.addWidget(self.__userNameLabel)
        self.__layoutHUser.addStretch(10)
        self.__layoutHUser.addWidget(self.__loginPushButton)
        self.__layoutHUser.addWidget(self.__logoutPushButton)

        self.__layoutVContent = QtGui.QVBoxLayout()
        self.__layoutVContent.addWidget(self.__imageCentralLabel)
        self.__layoutVContent.addLayout(self.__layoutHQueue)

        self.__layoutHContent = QtGui.QHBoxLayout()
        self.__layoutHContent.addLayout(self.__layoutVContent)
        self.__layoutHContent.addLayout(self.__layoutVButton)

        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addLayout(self.__layoutHUser)
        self.__layoutVMain.addLayout(self.__layoutHContent)
        self.__layoutVMain.setContentsMargins(3, 3, 5, 3)
        # Widget
        self.__centralWidget = QtGui.QWidget()
        self.__centralWidget.setLayout(self.__layoutVMain)
        # Functions
        self._createActions()
        self._createToolBars()
        self._createMenus()
        self._createStatusBar()
        self._synchronizationAutoServer()
        self._windowMoveToCenter()
        # Connect
        self.__synchronizationServerThread.finished.connect(self._checkAvailabilityServer)
        self.__synchronizationServerThread.finished.connect(self._userLogin)
        self.__synchronizationSessionThread.finished.connect(self._checkAvailabilitySession)
        self.__synchronizationCountThread.finished.connect(self._checkCount)

        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoServer)
        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoSession)
        self.__synchronizationCountTimer.timeout.connect(self._synchronizationAutoCount)
        self.__synchronizationStatusTimer.timeout.connect(self._synchronizationAutoStatus)

        self.__loginPushButton.clicked.connect(self._userClickedLogin)
        self.__logoutPushButton.clicked.connect(self._userClickedLogout)

        self.__nextClientMePushButton.clicked.connect(self._nextClientMe)
        self.__nextClientPushButton.clicked.connect(self._nextClient)
        self.__returnClientPushButton.clicked.connect(self._returnClient)
        self.__finishClientPushButton.clicked.connect(self._finishClient)
        # Timer every 5 sec
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
        self.__actionFileNextClient.setEnabled(False)

        self.__actionFileReturnClient = QtGui.QAction(QtGui.QIcon('img/black/png/export_icon&16.png'),
            self.tr('&Вернуть в очередь'), self, shortcut='Ctrl+Alt+R',
            statusTip=self.tr('Вернуть в очередь клиента'), triggered=self._returnClient)
        self.__actionFileReturnClient.setEnabled(False)

        self.__actionFileFinishClient = QtGui.QAction(QtGui.QIcon('img/black/png/flag_icon&16.png'),
            self.tr('&Завершить'), self, shortcut='Ctrl+Alt+Q',
            statusTip=self.tr('Завершить работу с клиентом'), triggered=self._finishClient)
        self.__actionFileFinishClient.setEnabled(False)

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

    def _createToolBars(self):
        self.__toolBar = self.addToolBar(self.tr('Панель инструментов'))
        self.__toolBar.setMovable(False)
        self.__toolBar.addAction(self.__actionFileNextClient)
        self.__toolBar.addAction(self.__actionFileReturnClient)
        self.__toolBar.addAction(self.__actionFileFinishClient)
        self.__toolBar.addSeparator()
        self.__toolBar.addAction(self.__actionFileSettingClient)

    def _createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('&Файл'))
        fileMenu.addAction(self.__actionFileNextClient)
        fileMenu.addAction(self.__actionFileReturnClient)
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

    def _windowMoveToCenter(self):
        rect = self.frameGeometry()
        rect.moveCenter(QtGui.QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())

    def _userLogin(self):
        self.__synchronizationServerThread.finished.disconnect(self._userLogin)

        if self.__dataBase:
            dialogLogin = DialogLogin(self.tr('Вход'), self.__dataBase)
            if dialogLogin.exec_() == QtGui.QDialog.Accepted:
                self.__userId = dialogLogin._userId()
                self.__userNameLabel.setText(self.tr('<b style="font-size: 11pt;">%s</b>' % dialogLogin._userName()))
                self.__serviceId = dialogLogin._serviceId()
                self.__synchronizationCountTimer.start(5000)
                self.__synchronizationStatusTimer.start(1000)

                self.__logoutPushButton.setVisible(True)

                cursor = self.__dataBase.cursor()
                cursor.execute('SELECT `client`.`id`, `client`.`number`, `client`.`start_time` FROM `mqueuedb`.`client` '
                               'WHERE `client`.`served` = 0 AND `client`.`call` = 1 AND `client`.`service_id` = %s '
                               'AND `client`.`user_id` = %s' % (self.__serviceId, self.__userId))
                self.__dataBase.commit()
                client = cursor.fetchone()
                if client:
                    self.__clientId = client[0]
                    clientNumber = client[1]
                    startDataTime = unicode(client[2])

                    cursor.execute('SELECT NOW()')
                    self.__dataBase.commit()
                    currentDataTime = unicode(cursor.fetchone()[0])

                    self.__clientLCDNumber.display(clientNumber)
                    self.__clientLCDNumber.setPalette(self.__paletteGreen)

                    self.__timeLateLCDNumber._setStartDataTime(startDataTime, currentDataTime)
                    self.__timeLateLCDNumber.setPalette(self.__paletteGreen)
                    self.__timeLateLCDNumber._start()

                    self.__sessionClient = True
                    self.__actionFileNextClient.setEnabled(False)
                    self.__actionFileReturnClient.setEnabled(True)
                    self.__actionFileFinishClient.setEnabled(True)
                    self.__nextClientMePushButton.setEnabled(False)
                    self.__nextClientPushButton.setEnabled(False)
                    self.__returnClientPushButton.setEnabled(True)
                    self.__finishClientPushButton.setEnabled(True)
            else:
                self.__loginPushButton.setVisible(True)
        else:
            QtGui.QMessageBox.warning(self, self.tr('Предупреждение'),
                self.tr('Сервер базы данных, недоступен'))
            self.__loginPushButton.setVisible(True)

    def _userClickedLogin(self):
        dialogLogin = DialogLogin(self.tr('Вход'), self.__dataBase)
        if dialogLogin.exec_() == QtGui.QDialog.Accepted:
            self.__userId = dialogLogin._userId()
            self.__userNameLabel.setText(self.tr('<b style="font-size: 11pt;">%s</b>' % dialogLogin._userName()))
            self.__serviceId = dialogLogin._serviceId()
            self.__synchronizationCountTimer.start(5000)
            self.__synchronizationStatusTimer.start(1000)

            self.__loginPushButton.setVisible(False)
            self.__logoutPushButton.setVisible(True)

            cursor = self.__dataBase.cursor()
            cursor.execute('SELECT `client`.`id`, `client`.`number`, `client`.`start_time` FROM `mqueuedb`.`client` '
                           'WHERE `client`.`served` = 0 AND `client`.`call` = 1 AND `client`.`service_id` = %s '
                           'AND `client`.`user_id` = %s' % (self.__serviceId, self.__userId))
            self.__dataBase.commit()
            client = cursor.fetchone()
            if client:
                self.__clientId = client[0]
                clientNumber = client[1]
                startDataTime = unicode(client[2])

                cursor.execute('SELECT NOW()')
                self.__dataBase.commit()
                currentDataTime = unicode(cursor.fetchone()[0])

                self.__clientLCDNumber.display(clientNumber)
                self.__clientLCDNumber.setPalette(self.__paletteGreen)

                self.__timeLateLCDNumber._setStartDataTime(startDataTime, currentDataTime)
                self.__timeLateLCDNumber.setPalette(self.__paletteGreen)
                self.__timeLateLCDNumber._start()

                self.__sessionClient = True
                self.__actionFileNextClient.setEnabled(False)
                self.__actionFileReturnClient.setEnabled(True)
                self.__actionFileFinishClient.setEnabled(True)
                self.__nextClientMePushButton.setEnabled(False)
                self.__nextClientPushButton.setEnabled(False)
                self.__returnClientPushButton.setEnabled(True)
                self.__finishClientPushButton.setEnabled(True)

    def _userClickedLogout(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('UPDATE `mqueuedb`.`user` SET `status`="0" '
                       'WHERE `id`="%s"' % self.__userId)
        self.__dataBase.commit()

        self.__loginPushButton.setVisible(True)
        self.__logoutPushButton.setVisible(False)

        self.__userId = None
        self.__userNameLabel.setText('')
        self.__serviceId = None
        self.__synchronizationCountTimer.stop()
        self.__synchronizationStatusTimer.stop()

        self.__clientLCDNumber.display('000')
        self.__clientLCDNumber.setPalette(self.__paletteRed)

        self.__timeLateLCDNumber.display('00:00:00')
        self.__timeLateLCDNumber.setPalette(self.__paletteRed)
        self.__timeLateLCDNumber._stop()

        self.__countLCDNumber.display(0)
        self.__countLCDNumber.setPalette(self.__paletteRed)

        self.__sessionClient = False
        self.__actionFileNextClient.setEnabled(False)
        self.__actionFileReturnClient.setEnabled(False)
        self.__actionFileFinishClient.setEnabled(False)
        self.__nextClientMePushButton.setEnabled(False)
        self.__nextClientPushButton.setEnabled(False)
        self.__returnClientPushButton.setEnabled(False)
        self.__finishClientPushButton.setEnabled(False)

    def _nextClientMe(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `client`.`id`, `client`.`number` FROM `mqueuedb`.`client` '
                       'WHERE `client`.`served` = 0 AND `client`.`call` = 0 AND `client`.`service_id` = %s '
                       'AND `client`.`user_id` = %s' % (self.__serviceId, self.__userId))
        self.__dataBase.commit()
        client = cursor.fetchone()
        if client:
            self.__clientId = client[0]
            clientNumber = client[1]

            cursor.execute('SELECT NOW()')
            self.__dataBase.commit()
            startDataTime = unicode(cursor.fetchone()[0])

            cursor.execute('UPDATE `mqueuedb`.`client` SET `start_time`="%s", `call`="1", `user_id`="%s" '
                           'WHERE `id`="%s"' % (startDataTime, self.__userId, self.__clientId))
            self.__dataBase.commit()

            self.__clientLCDNumber.display(clientNumber)
            self.__clientLCDNumber.setPalette(self.__paletteGreen)

            self.__timeLateLCDNumber._setStartDataTime(startDataTime, startDataTime)
            self.__timeLateLCDNumber.setPalette(self.__paletteGreen)
            self.__timeLateLCDNumber._start()

            self.__sessionClient = True
            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileReturnClient.setEnabled(True)
            self.__actionFileFinishClient.setEnabled(True)
            self.__nextClientMePushButton.setEnabled(False)
            self.__nextClientPushButton.setEnabled(False)
            self.__returnClientPushButton.setEnabled(True)
            self.__finishClientPushButton.setEnabled(True)

    def _nextClient(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `client`.`id`, `client`.`number` FROM `mqueuedb`.`client` '
                       'WHERE `client`.`served` = 0 AND `client`.`call` = 0 AND `client`.`service_id` = %s '
                       'AND ( `client`.`user_id` = %s OR `client`.`user_id` IS NULL )' % (self.__serviceId, self.__userId))
        self.__dataBase.commit()
        client = cursor.fetchone()
        if client:
            self.__clientId = client[0]
            clientNumber = client[1]

            cursor.execute('SELECT NOW()')
            self.__dataBase.commit()
            startDataTime = unicode(cursor.fetchone()[0])

            cursor.execute('UPDATE `mqueuedb`.`client` SET `start_time`="%s", `call`="1", `user_id`="%s" '
                           'WHERE `id`="%s"' % (startDataTime, self.__userId, self.__clientId))
            self.__dataBase.commit()

            self.__clientLCDNumber.display(clientNumber)
            self.__clientLCDNumber.setPalette(self.__paletteGreen)

            self.__timeLateLCDNumber._setStartDataTime(startDataTime, startDataTime)
            self.__timeLateLCDNumber.setPalette(self.__paletteGreen)
            self.__timeLateLCDNumber._start()

            self.__sessionClient = True
            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileReturnClient.setEnabled(True)
            self.__actionFileFinishClient.setEnabled(True)
            self.__nextClientMePushButton.setEnabled(False)
            self.__nextClientPushButton.setEnabled(False)
            self.__returnClientPushButton.setEnabled(True)
            self.__finishClientPushButton.setEnabled(True)

    def _returnClient(self):
        dialogReturnClient = DialogReturnClient(self.tr('Вход'), self.__dataBase)
        dialogReturnClient._setClientId(self.__clientId)
        dialogReturnClient._setUserId(self.__userId)
        dialogReturnClient._setServiceId(self.__serviceId)

        if dialogReturnClient.exec_() == QtGui.QDialog.Accepted:
            self.__clientLCDNumber.display('000')
            self.__clientLCDNumber.setPalette(self.__paletteRed)

            self.__timeLateLCDNumber.display('00:00:00')
            self.__timeLateLCDNumber.setPalette(self.__paletteRed)
            self.__timeLateLCDNumber._stop()

            self.__sessionClient = False
            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileReturnClient.setEnabled(False)
            self.__actionFileFinishClient.setEnabled(False)
            self.__nextClientMePushButton.setEnabled(False)
            self.__nextClientPushButton.setEnabled(False)
            self.__returnClientPushButton.setEnabled(False)
            self.__finishClientPushButton.setEnabled(False)

    def _finishClient(self):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT NOW()')
        self.__dataBase.commit()
        finishDataTime = unicode(cursor.fetchone()[0])

        cursor.execute('UPDATE `mqueuedb`.`client` SET `finish_time`="%s", `served`="1" '
                       'WHERE `id`="%s"' % (finishDataTime, self.__clientId))
        self.__dataBase.commit()

        self.__clientLCDNumber.display('000')
        self.__clientLCDNumber.setPalette(self.__paletteRed)

        self.__timeLateLCDNumber.display('00:00:00')
        self.__timeLateLCDNumber.setPalette(self.__paletteRed)
        self.__timeLateLCDNumber._stop()

        self.__sessionClient = False
        self.__actionFileNextClient.setEnabled(False)
        self.__actionFileReturnClient.setEnabled(False)
        self.__actionFileFinishClient.setEnabled(False)
        self.__nextClientMePushButton.setEnabled(False)
        self.__nextClientPushButton.setEnabled(False)
        self.__returnClientPushButton.setEnabled(False)
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
            cursor = self.__dataBase.cursor()
            cursor.execute('UPDATE `mqueuedb`.`user` SET `status`="0" '
                           'WHERE `id`="%s"' % self.__userId)
            self.__dataBase.commit()

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

            if lstClients[0]:
                self.__countLCDNumber.display(len(lstClients[0]))
                self.__countLCDNumber.setPalette(self.__paletteGreen)
                if not self.__sessionClient and not self.isActiveWindow():
                    QtGui.QApplication.alert(self)
                    self.__systemTrayIcon.showMessage(
                        self.tr('Внимание! Очередь...'),
                        self.tr('Количество людей в очереди - %s') % len(lstClients[0]))

                if self.__sessionClient:
                    self.__actionFileNextClient.setEnabled(False)
                    self.__actionFileReturnClient.setEnabled(True)
                    self.__actionFileFinishClient.setEnabled(True)
                    self.__nextClientMePushButton.setEnabled(False)
                    self.__nextClientPushButton.setEnabled(False)
                    self.__returnClientPushButton.setEnabled(True)
                    self.__finishClientPushButton.setEnabled(True)
                else:
                    self.__actionFileNextClient.setEnabled(True)
                    self.__actionFileReturnClient.setEnabled(False)
                    self.__actionFileFinishClient.setEnabled(False)
                    self.__nextClientPushButton.setEnabled(True)
                    self.__returnClientPushButton.setEnabled(False)
                    self.__finishClientPushButton.setEnabled(False)

                    if lstClients[1]:
                        self.__nextClientMePushButton.setEnabled(True)

            elif not self.__sessionClient:
                self.__countLCDNumber.display(0)
                self.__countLCDNumber.setPalette(self.__paletteRed)
                self.__actionFileNextClient.setEnabled(False)
                self.__actionFileReturnClient.setEnabled(False)
                self.__actionFileFinishClient.setEnabled(False)
                self.__nextClientMePushButton.setEnabled(False)
                self.__nextClientPushButton.setEnabled(False)
                self.__returnClientPushButton.setEnabled(False)
                self.__finishClientPushButton.setEnabled(False)
            elif self.__sessionClient:
                self.__countLCDNumber.display(0)
                self.__countLCDNumber.setPalette(self.__paletteRed)
                self.__actionFileNextClient.setEnabled(False)
                self.__actionFileReturnClient.setEnabled(True)
                self.__actionFileFinishClient.setEnabled(True)
                self.__nextClientMePushButton.setEnabled(False)
                self.__nextClientPushButton.setEnabled(False)
                self.__returnClientPushButton.setEnabled(True)
                self.__finishClientPushButton.setEnabled(True)
        else:
            self.__countLCDNumber.display(0)
            self.__countLCDNumber.setPalette(self.__paletteRed)

            self.__clientLCDNumber.display('000')
            self.__clientLCDNumber.setPalette(self.__paletteRed)

            self.__timeLateLCDNumber.display('00:00:00')
            self.__timeLateLCDNumber.setPalette(self.__paletteRed)
            self.__timeLateLCDNumber._stop()

            self.__actionFileNextClient.setEnabled(False)
            self.__actionFileReturnClient.setEnabled(False)
            self.__actionFileFinishClient.setEnabled(False)
            self.__nextClientMePushButton.setEnabled(False)
            self.__nextClientPushButton.setEnabled(False)
            self.__returnClientPushButton.setEnabled(False)
            self.__finishClientPushButton.setEnabled(False)

    def _synchronizationAutoStatus(self):
        self.__synchronizationStatusThread._setDataBase(self.__dataBase)
        self.__synchronizationStatusThread._setUserId(self.__userId)
        self.__synchronizationStatusThread.start()


