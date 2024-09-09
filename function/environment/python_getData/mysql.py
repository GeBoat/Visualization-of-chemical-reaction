import pymysql

class mysqlLink:
    cursor = ""
    config = ""

    # 打开数据库连接
    def __init__(self, user="root", password="#theroc-16", databaseName="test", port=3306):
        config = pymysql.connect(
            port=port,
            host="localhost",
            user=f"{user}",
            passwd=f'{password}',
            charset='utf8',
        )
        cursor = config.cursor()
        cursor.execute(f"create database if not exists {databaseName}")
        cursor.execute(f"use {databaseName}")
        self.config = config
        self.cursor = cursor

    def createAndUseDatabase(self, databaseName):
        cursor = self.cursor
        cursor.execute(f"create database if not exists {databaseName}")
        cursor.execute(f"use {databaseName}")

    def createTable(self, table, keys, primaryKey=None):
        cursor = self.cursor
        createTable = f""" CREATE TABLE IF NOT EXISTS {table}( """
        # for key in keys[:-1:2]:
        #     createTable+=f""" {key} VARCHAR(100),"""
        createTable += f""" VARCHAR(30),""".join(keys)
        createTable += f""" VARCHAR(30)"""
        if primaryKey:
            createTable += f""" ,PRIMARY KEY  ({primaryKey}) """
        createTable += """ )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        cursor.execute(createTable)  # 创建数据表

    def addData(self, table, keys, values):
        cursor = self.cursor
        InsertData = f"""INSERT INTO {table} ( {",".join(keys)} )
                       VALUES
                       ( '{"', '".join(values)}' );
                       """
        cursor.execute(InsertData)
        self.config.commit()
        pass

    def delTable(self, table):
        cursor = self.cursor
        delDatabase = f"""DROP TABLE IF EXISTS `{table}`
        """
        cursor.execute(delDatabase)
        self.config.commit()

    def delDatabase(self, table):
        cursor = self.cursor
        delDatabase = f"""DROP DATABASE IF EXISTS `{table}`
            """
        cursor.execute(delDatabase)
        self.config.commit()

    def select(self, table, columnName="*"):
        cursor = self.cursor
        select = f"""SELECT {columnName}
                    FROM {table}
                    """
        cursor.execute(select)
        return cursor.fetchall()

    def selectByCon(self, table, columnName="*", where=""):
        cursor = self.cursor
        select = f"""SELECT {columnName}
                    FROM {table} 
                    WHERE {where}
                    """
        cursor.execute(select)
        return cursor.fetchall()

def datebaseCheck(user, password, port):
    try:
        port = int(port)
        con = mysqlLink(user, password, port=port)
        return "success"

    except Exception as e:
        errorid = e.args[0]
        if errorid == 2003:
            return "端口错误"
        if errorid == 1045:
            return "账号或密码错误"