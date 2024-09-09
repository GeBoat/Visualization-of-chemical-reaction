from environment.python_getData import DataSelect
import os


class toSpecificForm:
    # dataSelect = DataSelect.dataSelect(user="root", password='Zhilong155732282', )
    keys = ['previousId', 'previousAtom', 'contentId', 'contentAtom', 'nextId', 'nextAtom']
    not_repeate = []
    def __init__(self,sql):
        self.dataSelect = DataSelect.dataSelect(sql)
        # dataSelect = DataSelect.dataSelect(user="root", password='Zhilong155732282', )
    def toReactChain(self, DataList=("", "", "", "")):
        not_repeate = []
        FatherAtom = DataList[3]
        test = dict()
        zipped = zip(self.keys[:4], DataList)
        Fileter = DataSelect.toFilter(zipped)
        result = self.dataSelect.selectData(table='asq', condition=Fileter)
        print("research result",result)
        # print(result)
        haveCheck = []
        # input()
        for branch in result:
            # 123123123123123print(branch)
            branchAtom = branch[3]
            # test.update({branchAtom:{}})
            # print(test)
            if branch[-1] == '' and branch[-2] == '':
                if branchAtom not in haveCheck:
                    num = 0
                    input()
                    for i in result:
                        if i[3] == branchAtom and i[-1] == '' and i[-2] == '':
                            num += 1
                            print("test")
                    haveCheck.append(branchAtom)
                    # test.update({f"{branchAtom}":  '{' + f'"$count":{num}' + '}'})
                    print(result)
                    test.update({f"{branchAtom}": {"$count": num}})
                    print(test)
                    input()
                    # print(test)
                else:
                    continue
            else:
                # print(branch[2:6])
                # if [branch[0:2], branch[4:6]] not in self.not_repeate:
                if branch not in self.not_repeate:
                    # print(branch[2:4], branch[4:6])
                    # print('thats not repeate')
                    # self.not_repeate.append([branch[4:6], branch[0:2]])
                    # print(branch)
                    self.not_repeate.append(branch)

                    childtest = self.toReactChain(branch[2:6])
                    # print(childtest,'child')
                    if childtest != {}:
                        if not test.__contains__(f'{FatherAtom}'):
                            test = {f'{FatherAtom}': {}}
                        # print(childtest)
                        # input()
                        # test.update({f"{branchAtom}": '{' + f'"{childtest}' + '}'})
                        # print(test)
                        (key, value), = childtest.items()
                        # print(key,value)
                        # print('Father',FatherAtom)
                        if test[FatherAtom].__contains__(key):
                            test[FatherAtom][key].update(value)
                        else:
                            test[FatherAtom].update({key: value})
                        # print(test)
                        # print('\n')

                        # test += f'"{branchAtom}":' + '{' + f'{childtest}' + '}'
                    else:
                        # test += ''
                        continue
                else:
                    # test+=''
                    continue
            # test += '}'
            # if branch != result[-1] and test != '':
            #     test += ','
            # input()
        # print(test)
        # input()
        return test


if __name__ == '__main__':
    absPath = os.path.abspath('../../../')
    filePath = os.path.join(absPath, 'reference', 'ben id', 'ben1', 'test.txt')
    toForm = toSpecificForm()
    test = 'const rawData='
    test += str(toForm.toReactChain()[''])
    print(test)
    file = open(filePath, 'w')
    file.write(test)
    file.close()
    # print(test)
