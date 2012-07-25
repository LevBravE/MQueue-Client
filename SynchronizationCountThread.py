# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore

#**************************************************************************************************
# class: SynchronizationCountThread
#**************************************************************************************************

class SynchronizationCountThread(QtCore.QThread):
    """
    Поток синхронизации с кол-ва пользователей
    """
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__dataBase = None
        self.__response = None
        self.__serviceId = None
        self.__userId = None

    def _response(self):
        return self.__response

    def _setDataBase(self, dataBase):
        self.__dataBase = dataBase

    def _setServiceId(self, serviceId):
        self.__serviceId = serviceId

    def _setUserId(self, userId):
        self.__userId = userId

    def run(self, *args, **kwargs):
        try:
            self.__response = []
            cursor = self.__dataBase.cursor()
            cursor.execute('SELECT `client`.`id`, `client`.`number` FROM `mqueuedb`.`client` '
                           'WHERE `client`.`served` = 0 AND `client`.`call` = 0 AND `client`.`service_id` = %s '
                           'AND ( `client`.`user_id` = %s OR `client`.`user_id` IS NULL )' % (self.__serviceId, self.__userId))
            self.__dataBase.commit()
            self.__response.append(cursor.fetchall())

            cursor.execute('SELECT `client`.`id`, `client`.`number` FROM `mqueuedb`.`client` '
                           'WHERE `client`.`served` = 0 AND `client`.`call` = 0 AND `client`.`service_id` = %s '
                           'AND `client`.`user_id` = %s' % (self.__serviceId, self.__userId))
            self.__dataBase.commit()
            self.__response.append(cursor.fetchall())
        except Exception:
            pass