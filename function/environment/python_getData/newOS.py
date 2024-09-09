import os
import copy
import json

from function.environment.python_getData import ToSpecificForm, mysql, sqlInput, openFile

absPath = os.path.abspath('../test/')
print(absPath)

def folderCheck(path, modern=False):
    if not os.path.exists(path):
        os.mkdir(path)

def Datainput(sqlport, FileOpen, fileIndex, filesPath):
    keys = ['previousId', 'previousAtom', 'contentId', 'contentAtom', 'nextId', 'nextAtom']
    file = fileIndex
    filePath = os.path.join(filesPath, file, 'result.txt')
    openfile = FileOpen.openFile(filePath)
    pieceContent = openfile.getPieceContent()
    for piece in pieceContent:
        unitList = openfile.getDataUnit(piece)
        relationshopList = openfile.getRelation(unitList)
        sqlport.InputData(table='asq', keys=keys, value=relationshopList)
    lastData = openfile.outputLastData()
    sqlport.InputData(table='asq', keys=keys, value=lastData)

def dicCheck(dicOne, dicTwo):
    for key, value in dicTwo.items():
        print("dicOne", dicOne)
        print("dicTwo", dicTwo)
        # input()
        if dicOne.__contains__(key):
            if key == '$count':
                dicOne[key] = dicOne[key] + 1
            else:
                NewDic = dicCheck(dicOne[key], dicTwo[key])
                dicOne[key] = NewDic
        else:
            dicOne.update(dicTwo)
        return dicOne

def dataCombine(filesPath):
    fileList = os.listdir(filesPath)
    dicList = []
    for file in fileList:
        filePath = os.path.join(filesPath, file)
        with open(filePath, 'r', encoding="UTF-8") as f:
            dic = json.load(f)
            dicList.append(dic)
    motherDic = dicList.pop(0)
    MotherPoint = motherDic
    for dic in dicList:
        if dic:
            MotherPoint = dicCheck(MotherPoint, dic)
    return MotherPoint

class staticlist:
    def __init__(self, length):
        self.length = length
        self.backUp = {}
        self.memory = []
        self.index = 0
        self.dict = {}
        self.firstNode = None  # 重复处的后一个结点（在多支链时的链式追踪功能，对单链没有用处）
        self.fatherNode = None
        self.foundRepeat = False

    def addMemory(self, one):
        if len(self.memory) == self.length:
            self.memory.pop(0)
            self.memory.append(one)
        else:
            self.memory.append(one)
        return self

    def setDict(self, dict):
        self.dict = dict

    def setBackup(self, dict):
        self.backUp = dict

    def setIndex(self, index):
        self.index = index

    def subIndex(self):
        self.index -= 1

    def setFatherNode(self, fatherNode):
        self.fatherNode = fatherNode

def mutichain(dic, updateOne):  # 处理多条链中不同链式出现的父节点的数据
    # input()
    print('12' * 20)
    updateDict = updateOne.dict
    print(updateDict)
    print('dicBefore', dic)
    newdic = dic
    dic.pop(updateOne.firstNode)
    print("dicAfter=", dic)
    while True:

        for key in updateDict.keys():
            # print(key)
            updateOneKey = key
        if newdic.__contains__(updateOneKey):
            if updateDict.__contains__('$count'):
                newdic['$count'] += updateDict['$count']
                break
            else:
                newdic = newdic[updateOneKey]
                updateDict = updateDict[updateOneKey]
        else:
            print("need help")
            newdic.update(updateDict)
            break
    print("dic", dic)
    return dic

def Data_clip(dict, layerMemory=None):
    sl = staticlist(length=100) if layerMemory == None else layerMemory
    sl.setDict(dict)
    dic = copy.deepcopy(dict)
    ThisDict = dict
    backup = {}
    finalBackup = []
    item = copy.deepcopy(sl)  # 网状图中单个叶子的记忆
    if len(dic) != 1:
        sl.memory = [sl.fatherNode]
        print(sl.memory)
    for key, value in dic.items():
        if type(value) == int:
            item.setIndex(0)
            item.setBackup(dict)
            item.foundRepeat = False
        else:
            childsl = copy.deepcopy(sl)
            childsl.addMemory(key)
            childsl.setFatherNode(key)
            Children = Data_clip(value, layerMemory=childsl)
            for Child in Children:
                havachecked = False
                if Child.index == -1:
                    if Child.foundRepeat:
                        pass
                    if len(value) != 1:
                        for itemkey, itemvalue in value.items():
                            print(key)
                            print("ChildfirstNode", Child.firstNode)
                            if itemkey == Child.firstNode:
                                Child1 = copy.copy(Child)
                                Child1.dict = Child1.dict[key]

                                subchainUpdate = mutichain(item.dict[key], Child1)
                                print("beforeitem", item.dict)
                                print(key)
                                print(subchainUpdate)
                                print("itemdict", item.dict)
                                havachecked = True
                            elif not havachecked:
                                print("waywayway2", item.dict)
                                print("before item dict", item.dict[key])
                                print('key', key)
                                print('itemvalue', itemvalue)
                                print('itemkey', itemkey)
                                if type(itemvalue) != int and itemvalue.__contains__(itemkey):
                                    item.dict[key].update(itemvalue)
                                    print("1")
                                else:
                                    print("2")
                                    continue
                                    pass
                                print("after item dict", item.dict)
                                print(itemkey, itemvalue)
                                # item.dict[key].update({itemkey:itemvalue})
                                print(item.dict)
                                print("+" * 20)
                    if key in sl.memory:  # 阐述该判断中是否出现了可裁剪片段
                        item.setBackup(item.dict)
                        item.setIndex(len(sl.memory) - sl.memory.index(key) - 1)
                        print(sl.memory)
                        print("len=", len(sl.memory) - item.index, len(sl.memory))
                        if item.index == 0:
                            item.firstNode = key
                            print("wayway1")
                        else:
                            print("wayway2")
                            item.firstNode = sl.memory[len(sl.memory) - item.index]
                        print(item.firstNode)
                        item.foundRepeat = True
                        print("not exist")
                        print(item.index)
                        print(key)
                        print(item.dict)
                        print(Child.memory)
                        print(Child.dict)
                        if Child.dict.__contains__(key):
                            item.dict = Child.dict
                        else:
                            item.dict.update({key: Child.dict})
                        print(item.dict)
                        print("/" * 10)
                        pass
                    elif not havachecked:
                        print(Child.memory)
                        print(Child.dict)
                        print(Child.backUp)
                        print("before", item.dict)
                        print(key)
                        if Child.backUp:
                            print("way 1")
                            if Child.dict.__contains__(key):
                                print("same")
                                item.dict.update(Child.dict)
                            else:
                                item.dict.update({key: Child.dict})
                                print("differ")
                            item.backUp = item.dict
                        else:

                            print("way 2")
                            if Child.dict.__contains__(key):
                                item.dict.update(Child.dict)
                            else:
                                item.dict.update({key: Child.dict})
                        print("after", item.dict)
                        print("!")
                else:
                    print(item.memory)
                    print(Child.index)
                    print(item.dict)
                    print(Child.dict)
                    print("test")
                    item.firstNode = Child.firstNode
                    item.foundRepeat = True
                    item.index = Child.index
                    if len(item.dict) == 1:
                        item.dict = Child.dict
                    else:
                        item.dict.pop(key)
                        item.dict.update(Child.dict)
                        print(Child.dict)
                    print("after", item.dict)
                print("-" * 10)
                dic = item.dict
    item.subIndex()
    finalBackup.append(item)
    return finalBackup

class feedBack:
    class aimdic:
        aimdict = {}
        index = -2

        def __init__(self, aimdic, index=-2):
            self.aimdict = aimdic
            self.index = index

    def __init__(self):
        self.previousdic = {}
        self.memory = []
        self.aimdiclist = []

    def addaimdic(self, dic, index=-2):
        self.aimdiclist.append(self.aimdic(dic, index))

    def add(self, aimdic):
        self.aimdiclist.append(aimdic)

def doubleCheck(dict, layerMemory=None):
    sl = staticlist(length=20) if layerMemory == None else layerMemory
    fb = feedBack()
    sl.setDict(dict)
    dic = copy.deepcopy(dict)
    ThisDict = dict
    backup = {}
    finalBackup = []
    item = copy.deepcopy(sl)  # 网状图中单个叶子的记忆
    for key, value in dic.items():
        if type(value) == int:
            fb.addaimdic(dict)
            fb.memory = sl.memory
        else:
            childsl = copy.deepcopy(sl)
            childsl.addMemory(key)
            feedbackLists = doubleCheck(value, childsl)
            for feedback in feedbackLists.aimdiclist:
                print('fb.aimdic', feedback.aimdict)
                print('fb.memory', feedbackLists.memory)
                print(key)
                print(feedbackLists.memory[:-1:])
                if feedback.index == -1:
                    item.dict.update(feedback.dictt)
    fb.previousdic = dict
    fb.memory = sl.memory
    return fb
    pass

def resulrOutput(sql, dataInput, fileIndex, resultPath):
    resultFile = os.path.join(resultPath, fileIndex + 'result.json')
    result = dataInput.selectData()
    for one in result:
        print(one)
        pass
    toForm = ToSpecificForm
    Form = toForm.toSpecificForm(sql)
    chain = Form.toReactChain()
    rawform = Data_clip(chain)
    with open(resultFile, 'w') as f:
        test = json.dump(rawform[0].dict, f, ensure_ascii=False)

def main(sqllist, filepath, chartlist):
    # absPath = os.path.abspath('../')
    list = os.listdir(absPath)
    datapiecePath = os.path.join(absPath, 'datapiece')
    filesPath = os.path.join(absPath, "reference", 'ben id')
    resultPath = os.path.join(absPath, "reference", 'datapiece')
    aimPath = os.path.join(absPath, "function", 'environment', 'flask', 'static', 'result')
    folderCheck(aimPath, True)
    folderCheck(resultPath)
    folderCheck(datapiecePath)
    # =========================================
    # =            数据注入                     =
    # =========================================
    keys = ['previousId', 'previousAtom', 'contentId', 'contentAtom', 'nextId', 'nextAtom']
    user = sqllist["user"]
    password = sqllist["password"]
    sql = mysql.mysqlLink(user=user, password=password)
    sqlport = sqlInput.dataInput(sql)
    FileOpen = openFile
    fileList = os.listdir(filesPath)
    for file in fileList:
        print(file)
        sqlport.createTable('asq', keys)
        Datainput(sqlport, FileOpen, file, filesPath)
        resulrOutput(sql, sqlport, file, resultPath)
        sqlport.deleTable()
    one = os.path.join(resultPath, "ben1result.json")
    # =================================
    # =         化学反应路径合并         =
    # =================================
    NewDic = dataCombine(resultPath)
    NewDic1 = NewDic
    b = copy.deepcopy(NewDic)
    # =================================
    # =         裁剪策略                =
    # =================================
    NewDic1 = Data_clip(b)
    NewDic1 = NewDic1[0].dict
    aimFile = os.path.join(aimPath, 'rawData.js')
    with open(aimFile, "w", encoding="UTF-8") as f:
        test = "const rawData="
        f.write(test)
        test = json.dump(NewDic1[""], f, ensure_ascii=False)
    dataFile = os.path.join(aimPath, 'rawdata.js')
    for i in chartlist:
        if i == "graph":
            ToSpecificForm.graph(rawDataPath=dataFile, path=aimPath)
        elif i == "treeall":
            ToSpecificForm.treeall(rawDataPath=dataFile, path=aimPath)
        elif i == "treesome":
            ToSpecificForm.treesome(rawDataPath=dataFile, path=aimPath)
        elif i == "sun":
            ToSpecificForm.sun(rawDataPath=dataFile, path=aimPath)

    print("程序运行结束")

