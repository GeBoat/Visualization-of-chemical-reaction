import re

class openFile:
    def __init__(self, path):
        self.filePath = path
        self.FatherUnitList = [{'previous': ['', ''], 'content': ['', ''], 'next': [['', '']]}]

    def getPieceContent(self, path=None):
        if path == None:
            path = self.filePath
        with open(path) as file:
            pieceContent = []
            content = file.readlines()
            for i in range(0, len(content), 6):
                pieceContent.append(content[i:i + 6])
        return pieceContent

    def getDataUnit(self, unit):
        unitId = re.search(': +( .*)', unit[3])[1]
        unitIdList = re.split(" *<>  ", unitId)[:-1:]

        unitStiatic = re.search(': +( .*)', unit[4])[1]
        unitStiaticList = re.split(" *<>  ", unitStiatic)[:-1:]

        unitList = dict(zip(unitIdList, unitStiaticList))
        return unitList

    def getRelation(self, unitList):
        FatherUnitList = self.FatherUnitList  # 获取反应父本分子列表（初始化）
        # print('FatherUnitList:',FatherUnitList)
        FatherUnitListNew = []  # 在对父本和子本进行是否反应的判断后用于更新下一个父本分子列表，因为不反应的分子父本数据和
        # 子本数据相同，所以选择直接获取子本数据以避免不必要的if判断
        for FatherUnit in FatherUnitList:
            FatherUnit['next'] = [['', '']]
        for key, value in unitList.items():
            checkOne = re.split(" ", key)[1]  # 对原子进行检索，取原子序列中的一个原子进行父本判断
            for Father in FatherUnitList:  # 将原子与父本分子列表使用search进行相似查询，如果一父本分子中存在子本原子id
                # 则判断为父子关系，进行链化处理
                FatherKey, FatherValue = Father['content']
                if re.search(checkOne, FatherKey) or FatherKey == "":
                    if key == FatherKey and value == FatherValue:
                        FatherUnitListNew.append(Father)
                        continue
                    if Father['next'][0] == ['', '']:
                        Father['next'].pop(0)
                    Father['next'].append([key, value])
                    FatherUnitNew = {'previous': [FatherKey, FatherValue], 'content': [key, value], 'next': [['', '']]}
                    FatherUnitListNew.append(FatherUnitNew)
        self.FatherUnitList = FatherUnitListNew
        outputList = []
        for unit in FatherUnitList:
            if unit['next'] != [['', '']]:
                outputList.append(unit)
        return outputList

    def outputLastData(self):
        return self.FatherUnitList
