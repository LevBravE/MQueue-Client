# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

import MySQLdb

#**************************************************************************************************
# class: DataSql
#**************************************************************************************************

class DataSql(object):
    """
    API Database
    """
    def _connectDataBase(self,
                         hostName='localhost',
                         dataBaseName='mqueuedb',
                         userName='newuser',
                         password='wwww',
                         port=3306):
        """
        Соединение с базой данных
        """
        try:
            dataBase = MySQLdb.connect(
                host=hostName,
                db=dataBaseName,
                user=userName,
                passwd=password,
                port=port,
            )
        except Exception:
            return False

        dataBase.set_character_set('utf8')

        return dataBase



if __name__ == '__main__':

    dataSql = DataSql()
    if not dataSql._connectDataBase():
        print 'Error: Not connect database'


