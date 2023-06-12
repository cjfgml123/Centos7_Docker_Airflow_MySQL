import pymysql

'''
MySQL 연결 클래스
'''
class MySql:
    def __init__(self, _dbName:str, _host:str, _port:int, _user:str, _pw:str):
        self._dbName =_dbName
        self._host = _host
        self._port = _port
        self._user = _user
        self._pw = _pw
        self._conn = None
        self._cur = None 
        
    def Connect(self):
        try:
            self._conn = pymysql.connect(host=self._host, port=self._port, db=self._dbName, 
                                          user=self._user, passwd=self._pw,charset="utf8")
            self._conn.autocommit = False
            self._cur = self._conn.cursor()
            if self._conn.open:
                print("MySQL Connection Successfully.")
                return True
            else:
                print("MySQL Connection Fail.")
                return False            
        except Exception as _ex:
            print("Connect() Error : ", _ex)
            return False
    
    def DisConnect(self):
        if self._conn.open:
            self._cur.close()
            self._conn.close()
            print("MySQL Connection End.")

    def Commit(self):
        self._conn.commit()
        #self.__Excute("COMMIT")

    def RollBack(self):
        self._conn.rollback()
        #self.__Excute("ROLLBACK")

    def Create(self, _query:str):
        self._cur.execute(_query)
        self._conn.commit()
    
    def Insert(self, _query:str):
        self._cur.execute(_query)

    # df를 Insert할때 사용
    def InsertBigData(self, _query:str, _data:list):
        self._cur.executemany(_query,_data)
        self._conn.commit()
        
    def Update(self, _query:str):
        self._cur.execute(_query)

    def Delete(self, _query:str):
        self._cur.execute(_query)

    def Select(self, _query:str):
        self._cur.execute(_query)
        return self._cur.fetchall()