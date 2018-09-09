import json
import re


class Item:
    # data = []
    item = {}
    tree = ""
    ids = []
    tree_ar = ""

    def __init__(self, objectId, parentId, name, isActive, position, level, product_count, path, name_ar):
        self.objectID = objectId
        self.parent_id = parentId
        self.name = name
        self.isActive = isActive
        self.position = position
        self.level = level
        self.product_count = product_count
        self.path = path
        self.name_ar = name_ar

    def getitem(self):
        item = {}
        item['objectId'] = self.objectID;
        item['parent_id'] = self.parent_id;
        item['name'] = self.name;
        item['isActive'] = self.isActive;
        item['position'] = self.position;
        item['level'] = self.level;
        item['product_count'] = self.product_count;
        item['tree'] = self.tree;
        item['ids'] = self.ids;
        item['path'] = self.path;
        item['name_ar'] = self.name_ar;
        item['tree_ar'] = self.tree_ar;
        # n_item = self.item
        # del self.item
        return item

    def updateIds(self, Ids):
        self.ids = Ids

    def updateTree(self, tree):
        self.tree = tree

    def updateTree_ar(self, tree_ar):
        self.tree_ar = tree_ar


class Flatten:
    lst=[]
    parents={}
    tree={}
    tree_ar={}

    def __init__(self):
        self.lst = []
        self.parents = {}
        self.tree = {}
        self.tree_ar = {}

    def flat(self, data, no_of_attrs=10):
        # if list
        if isinstance(data, list):
            # print("list ", data['id'])
            # print("list", len(data))
            if len(data) == 0:
                return
            elif len(data) >= 1:
                # print(data[0])
                for i in data:
                    # print(i)
                    self.flat(i, no_of_attrs)
            else:
                return
        # if dictionary
        elif isinstance(data, dict):
            # print("dict ", data['id'])
            # print("dict", len(data), data)
            if len(data) == 10:
                print("10")
                if data['level'] < 2:
                    if len(data['children_data']) > 0:
                        for k in data['children_data']:
                            self.flat(k, no_of_attrs)

                # print(data['name_ar'], data['path'])
                if data['path'] not in ('Null', None) or data['name_ar'] not in ('Null', None):
                    # print("Not null")
                    n_item= Item(data['id'], data['parent_id'], data['name'], data['is_active'], data['position'],
                                  data['level'], data['product_count'], data['path'], data['name_ar'])
                    id_index = str(data['id'])
                    parentId_index = str(data['parent_id'])

                    self.parents[id_index] = []
                    if parentId_index in self.parents:
                        self.parents[id_index].extend(self.parents[parentId_index])
                        self.parents[id_index].append(data['id'])
                    else:
                        if id_index == '2':
                            self.parents[id_index] = []
                        elif parentId_index == '2':
                            # self.parents[id_index].append(data['parent_id'])
                            self.parents[id_index].append(data['id'])
                        else:
                            self.parents[id_index].append(data['parent_id'])
                            self.parents[id_index].append(data['id'])

                    if parentId_index in self.tree:
                        self.tree[id_index] = self.tree[parentId_index] + ">" + data['name']
                    else:
                        self.tree[id_index] = data['name']

                    print(data['name_ar'])
                    if parentId_index in self.tree_ar:
                        pattern_ar = re.compile("[^0-9\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc]")
                        # To check appending of arabic letters
                        # print(type(data['name_ar']))
                        if pattern_ar.match(data['name_ar']):
                            # print(data['name_ar'], type(data['name_ar']), type(self.tree_ar[parentId_index]))
                            self.tree_ar[id_index] = data['name_ar'] + "<" + self.tree_ar[parentId_index]
                        else:
                            # print("Arabic found")
                            self.tree_ar[id_index] = self.tree_ar[parentId_index] + ">" + data['name_ar']
                    else:
                        self.tree_ar[id_index] = data['name_ar']

                    n_item.updateIds(self.parents[id_index])
                    n_item.updateTree(self.tree[id_index])
                    n_item.updateTree_ar(self.tree_ar[id_index])
                    self.lst.append(n_item.getitem())
                    # print(data['id'])

                    # del n_item
                    if len(data['children_data']) > 1:
                        for l in data['children_data']:
                            self.flat(l,  no_of_attrs)
                else:
                    print(data['path'], data['name_ar'])
                    return
            else:
                return
        elif isinstance(data, str):
            # print("str ", data['id'])
            return
        else:
            # print("else-1 ", data['id'])
            return

    def returnList(self):
        return self.lst
