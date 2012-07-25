# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore

#**************************************************************************************************
# class: SynchronizationStatusThread
#**************************************************************************************************

class SynchronizationStatusThread(QtCore.QThread):
    """
    Поток синхронизации статуса пользователя
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__dataBase = None
        self.__userId = None

    def _setDataBase(self, dataBase):
        self.__dataBase = dataBase

    def _setUserId(self, userId):
        self.__userId = userId

    def run(self, *args, **kwargs):
        try:
            cursor = self.__dataBase.cursor()
            cursor.execute('SELECT `user`.`status` FROM `mqueuedb`.`user` '
                           'WHERE `user`.`id` = %s' % self.__userId)
            self.__dataBase.commit()

            if not cursor.fetchone()[0]:
                cursor.execute('UPDATE `mqueuedb`.`user` SET `status`="1" '
                               'WHERE `id`="%s"' % self.__userId)
                self.__dataBase.commit()
        except Exception:
            pass