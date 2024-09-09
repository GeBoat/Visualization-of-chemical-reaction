import random
from function.environment.python_getData import DataSelect
import json
import pyecharts.options as opts
from pyecharts.charts import Sankey, Sunburst
from pyecharts.charts import Tree
from pyecharts.charts import Graph

class toSpecificForm:
    keys = ['previousId', 'previousAtom', 'contentId', 'contentAtom', 'nextId', 'nextAtom']
    not_repeate = []
    haveCheck = []

    def __init__(self, sql):
        self.dataSelect = DataSelect.dataSelect(sql)

    def toReactChain(self, DataLists=None):
        if DataLists is None:
            DataLists = [("", "", "", "")]
        not_repeate = []
        totalresult = ()
        for DataList in DataLists:
            FatherAtom = DataList[3]
            test = dict()
            zipped = zip(self.keys[:4], DataList)
            Fileter = DataSelect.toFilter(zipped)
            result = self.dataSelect.selectData(table='asq', condition=Fileter)
            totalresult += (result)
        haveCheck = []
        for branch in totalresult:
            branchAtom = branch[3]
            if branch[-1] == '' and branch[-2] == '':
                if branch not in self.haveCheck and branchAtom not in haveCheck:
                    num = 0
                    for i in totalresult:
                        if i[3] == branchAtom and i[-1] == '' and i[-2] == '':
                            num += 1
                    haveCheck.append(branchAtom)
                    self.haveCheck.append(branch)
                    if test == {}:
                        test.update({f"{branchAtom}": {"$count": num}})
                    else:
                        test[branchAtom].update({"$count": num})
                else:
                    continue
            else:
                if branch not in self.not_repeate:
                    NextDataLists = []
                    for i in totalresult:
                        if branch[1] == i[1] and branch[3] == i[3] and branch[5] == i[5]:
                            NextDataLists.append(i[2:6])
                    self.not_repeate.append(branch)
                    childtest = self.toReactChain(NextDataLists)
                    if childtest != {}:
                        if not test.__contains__(f'{FatherAtom}'):
                            test = {f'{FatherAtom}': {}}
                        (key, value), = childtest.items()
                        if test[FatherAtom].__contains__(key):
                            test[FatherAtom][key].update(value)
                        else:
                            test[FatherAtom].update({key: value})
                    else:
                        continue
                else:
                    continue
        return test

def sun(path, rawDataPath=None, name="sun"):
    def extract_reactions(data, path=None, result=None):
        if path is None:
            path = []
        if result is None:
            result = []
        for key, value in data.items():
            new_path = path + [key]
            if isinstance(value, dict):
                extract_reactions(value, new_path, result)
            elif key == "$count":
                reaction = " -> ".join(new_path[:-1])
                result.extend([reaction] * value)
        return result

    def generate_sunburst_data(reactions):
        sunburst_data = []
        for reaction in reactions:
            # 删除第一个节点 "C6H6"
            reaction_path = reaction.split(" -> ")[1:]
            current_level = sunburst_data
            for i, step in enumerate(reaction_path):
                found_step = False
                for item in current_level:
                    if item["name"] == step:
                        current_level = item.setdefault("children", [])
                        found_step = True
                        break
                if not found_step:
                    new_step = {"name": step}
                    if i == len(reaction_path) - 1:
                        new_step["value"] = 1  # Leaf node
                    current_level.append(new_step)
                    current_level = new_step.setdefault("children", [])
        return sunburst_data

    with open(rawDataPath, 'r', encoding='UTF-8') as dataFile:
        data = dataFile.read()
        obj = data[data.find('{'): data.rfind('}') + 1]
        raw_data = json.loads(obj, strict=False)
    reaction_paths = extract_reactions(raw_data)
    for reaction in reaction_paths:
        print(reaction)
    sunburst_data = generate_sunburst_data(reaction_paths)
    print(sunburst_data)
    level_count = 25  # 总共的层级数
    radius_step = 100 / level_count  # 设置每个级别的半径增量
    level_opts = []
    for i in range(level_count):
        level_opts.append({
            "r0": f"{i * radius_step}%",
            "r": f"{(i + 1) * radius_step}%",
            "itemStyle": {"borderWidth": 2}
        })
    for i, level in enumerate(level_opts):
        level["label"] = {
            "rotate": 0,  # 统一设置标签旋转角度为-45度
            "align": "left" if i % 2 == 1 else "right",  # 奇数层级左对齐，偶数层级右对齐
            "verticalAlign": "top" if i % 2 == 0 else "bottom",  # 根据层级奇偶性交替上下对齐
            "padding": 5,  # 适当增加标签内边距，避免文字重叠
        }
    c = (
        Sunburst(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(
            "",
            data_pair=sunburst_data,
            highlight_policy="ancestor",
            radius=["10%", "80%"],  # 调整整体半径范围，使图形更集中
            sort_="null",
            levels=level_opts,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Sunburst-官方示例"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
        .render(f"{path}/{name}.html")
    )

def treeall(path, rawData=None, rawDataPath=None, name="treeall"):
    def _getTree_(dict, parent_color=None):
        tree = []
        totalIndex = 0
        for i in dict:
            index = 0
            node = {}
            if i != '$count':
                subIndex, subtree = _getTree_(dict[i], parent_color)
                index += subIndex
                node.update({"name": i})
                node.update({"value": index})
                if subtree:  # 存在子节点时添加
                    node.update({"children": subtree})
                tree.append(node)
                pass
            else:
                index += dict[i]
                if len(dict) != 1:
                    node.update({"name": parent_color})
                    node.update({"value": index})
                    tree.append(node)
            totalIndex += index
        return totalIndex, tree

    with open(rawDataPath, 'r', encoding='UTF-8') as dataFile:
        data = dataFile.read()
        obj = data[data.find('{'): data.rfind('}') + 1]
        rawData = json.loads(obj, strict=False)
    rawData = {"": rawData}
    _, tree = _getTree_(rawData)
    color_dict = {}  # 用于存储每一个父节点的颜色

    def set_node_color(node, parent_color):
        nonlocal color_dict
        if parent_color not in color_dict:
            color_dict[parent_color] = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # 随机生成颜色
        node.update({"itemStyle": {"color": color_dict[parent_color]}})
        if "children" in node:
            children_count = len(node["children"])
            if children_count > 1:
                # 子节点数量超过阈值，重新设置颜色
                new_parent_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            else:
                new_parent_color = parent_color
            for child in node["children"]:
                set_node_color(child, new_parent_color)
    for node in tree:
        set_node_color(node, None)
    c = (
        Tree(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(
            "",
            tree,
            initial_tree_depth=-1,
            orient="BT",  # 设置方向为下上
            label_opts=opts.LabelOpts(
                position="top",
                horizontal_align="right",
                vertical_align="middle",
                rotate=0,
                font_size=15,
            ),
            leaves_label_opts=opts.LabelOpts(
                position="bottom",
                horizontal_align="left",
                vertical_align="middle",
                rotate=0,
                font_size=15,
            )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree树图"))
        .render(f"{path}/{name}.html")
    )

def treesome(path, rawData=None, rawDataPath=None, name="treesome"):
    def _getTree_(dict, parent_color=None):
        tree = []
        totalIndex = 0
        for i in dict:
            index = 0
            node = {}
            if i != '$count':
                subIndex, subtree = _getTree_(dict[i], parent_color)
                index += subIndex
                node.update({"name": i})
                node.update({"value": index})
                if subtree:  # 存在子节点时添加
                    node.update({"children": subtree})
                tree.append(node)
                pass
            else:
                index += dict[i]
                if len(dict) != 1:
                    node.update({"name": parent_color})
                    node.update({"value": index})
                    tree.append(node)
            totalIndex += index
        return totalIndex, tree

    with open(rawDataPath, 'r', encoding='UTF-8') as dataFile:
        data = dataFile.read()
        obj = data[data.find('{'): data.rfind('}') + 1]
        rawData = json.loads(obj, strict=False)
    rawData = {"": rawData}
    _, tree = _getTree_(rawData)

    color_dict = {}  # 用于存储每一个父节点的颜色

    def set_node_color(node, parent_color):
        nonlocal color_dict
        if parent_color not in color_dict:
            color_dict[parent_color] = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # 随机生成颜色
        node.update({"itemStyle": {"color": color_dict[parent_color]}})
        if "children" in node:
            children_count = len(node["children"])
            if children_count > 1:
                # 子节点数量超过阈值，重新设置颜色
                new_parent_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            else:
                new_parent_color = parent_color
            for child in node["children"]:
                set_node_color(child, new_parent_color)

    for node in tree:
        set_node_color(node, None)

    c = (
        Tree(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(
            "",
            tree,
            initial_tree_depth=3,
            orient="BT",  # 设置方向为下上
            label_opts=opts.LabelOpts(
                position="top",
                horizontal_align="right",
                vertical_align="middle",
                rotate=0,
                font_size=20,
            ),
            leaves_label_opts=opts.LabelOpts(
                position="bottom",
                horizontal_align="left",
                vertical_align="middle",
                rotate=0,
                font_size=15,
            )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree树图"))
        .render(f"{path}/{name}.html")
    )

def graph(path, rawData=None, rawDataPath=None, name="graph"):
    with open(rawDataPath, 'r', encoding='UTF-8') as dataFile:
        data = dataFile.read()
        obj = data[data.find('{'): data.rfind('}') + 1]
        raw_data = json.loads(obj, strict=False)

    def process_data(data):
        nodes = []
        links = []
        categories = []

        def add_node(name, color, category):
            for node in nodes:
                if node["name"] == name:
                    return
            nodes.append({"name": name, "symbolSize": 10, "itemStyle": {"color": color},
                          "label": {"show": True, "position": "right"}, "category": category})

        def add_link(source, target, linecolor):
            links.append({"source": source, "target": target, "lineStyle": {"color": linecolor}})

        def traverse(data, parent=None):
            for key, value in data.items():
                if key == "$count":
                    continue
                if parent:
                    linecolor = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                    add_link(parent, key, linecolor)
                color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                add_node(key, color, key)  # 将类别名设为节点名
                categories.append({"name": key})  # 每个节点都是一个独立的类别
                if isinstance(value, dict):
                    traverse(value, key)

        traverse(data)
        return nodes, links, categories  # 返回类别信息

    # 调用函数处理数据
    nodes, links, categories = process_data(raw_data)
    print("Nodes:", nodes)
    print("Links:", links)
    print("Categories:", categories)

    # 生成图表
    c = (
        Graph(init_opts=opts.InitOpts(width="1500px", height="700px"))
        .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="circular",
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Graph-Les Miserables"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="1%", pos_top='10%',
                                        textstyle_opts=opts.TextStyleOpts(font_size=8), ),
        )

        .render(f"{path}/{name}.html")
    )