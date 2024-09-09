class dataInput:
    def __init__(self, sql):
        self.sql = sql

    def createTable(self, tableName, keys, primaryKey=None):
        self.sql.createTable(tableName, keys, primaryKey)
        self.tableName = tableName

    def toFilter(self,zip):
        list = []
        for one in zip:
            list.append(one[0] + "='" + one[1] + "'")
        result = " and ".join(list) + ";"
        return result

    def InputData(self, table, keys, value):
        if table == "":
            table = self.tableName
        for unit in value:
            for num in unit['next']:
                values = unit['previous'] + unit['content'] + num
                toFilter=zip(keys,values)
                Filter=self.toFilter(toFilter)
                exists=self.sql.selectByCon(table=table, where=Filter)
                if not exists:
                    self.sql.addData(table, keys, values)
                else:
                    pass

    def selectData(self):
        result = self.sql.select(self.tableName)
        return result

    def deleTable(self):
        self.sql.delTable(self.tableName)



