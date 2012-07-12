# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore
from DataSql import DataSql

#**************************************************************************************************
# class: SynchronizationServerThread
#**************************************************************************************************

class SynchronizationServerThread(QtCore.QThread):
    """
    Поток синхронизации с сервером баз данных
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__host = None
        self.__user = None
        self.__password = None
        self.__port = None
        self.__response = None

    def _response(self):
        return self.__response

    def _setHost(self, host):
        self.__host = host

    def _setUser(self, user):
        self.__user = user

    def _setPassword(self, password):
        self.__password = password

    def _setPort(self, port):
        self.__port = port

    def run(self, *args, **kwargs):
        try:
            self.__response = None
            self.__response = DataSql()._connectDataBase(
                hostName=self.__host,
                userName=self.__user,
                password=self.__password,
                port=int(self.__port),
            )
        except Exception:
            pass