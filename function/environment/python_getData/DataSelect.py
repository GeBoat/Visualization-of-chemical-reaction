class dataSelect:

    def __init__(self, mysql):
        self.sql = mysql

    def selectData(self, condition, table=''):
        result = self.sql.selectByCon(table=table, where=condition)
        return result
        pass


def toFilter(zip):
    list = []
    for one in zip:
        list.append(one[0] + "='" + one[1] + "'")
    result = " and ".join(list)+";"
    return result




