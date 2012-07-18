# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore, QtGui

#**************************************************************************************************
# class: TimeLateLCDNumber
#**************************************************************************************************

class TimeLateLCDNumber(QtGui.QLCDNumber):
    """
    Цифровые часы пройденного времени
    """
    def __init__(self):
        QtGui.QLCDNumber.__init__(self)
        self.__lastSecs = 0
        # Timer
        self.__timer = QtCore.QTimer()
        # Connect
        self.__timer.timeout.connect(self._showTime)
        # <<<Self>>>
        self.setDigitCount(8)

    def _setStartDataTime(self, strStartDataTime, strCurrentDataTime):
        startDataTime = QtCore.QDateTime().fromString(strStartDataTime, QtCore.Qt.ISODate)
        currentDataTime = QtCore.QDateTime().fromString(strCurrentDataTime, QtCore.Qt.ISODate)
        self.__lastSecs = startDataTime.secsTo(currentDataTime) #- 1755826387

    def _start(self):
        self.__timer.start(1000)

    def _stop(self):
        self.__timer.stop()

    def _showTime(self):
        self.__lastSecs += 1
        displayTime = QtCore.QTime((self.__lastSecs / 3600) % 60, (self.__lastSecs / 60) % 60, (self.__lastSecs / 1) % 60)
        strDisplayTime = displayTime.toString('hh:mm:ss')

        if not displayTime.second() % 2:
            strDisplayTime = strDisplayTime.replace(':', ' ')

        self.display(strDisplayTime)

