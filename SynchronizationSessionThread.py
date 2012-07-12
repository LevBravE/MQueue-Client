# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore

#**************************************************************************************************
# class: SynchronizationSessionThread
#**************************************************************************************************

class SynchronizationSessionThread(QtCore.QThread):
    """
    Поток синхронизации с сервером баз данных
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__host = None
        self.__dataBase = None
        self.__response = None

    def _response(self):
        return self.__response

    def _setDataBase(self, dataBase):
        self.__dataBase = dataBase

    def run(self, *args, **kwargs):
        try:
            self.__response = None
            cursor = self.__dataBase.cursor()
            cursor.execute('SELECT `parameter_data`.`session` FROM `mqueuedb`.`parameter_data`')
            self.__dataBase.commit()
            self.__response = cursor.fetchone()[0]
        except Exception:
            pass