"""
Courtesy of:

http://stackoverflow.com/questions/1458450/python-serializable-objects-json
"""

import json


class Tree(object):
    def __init__(self, name, childTrees=None):
        self.name = name
        if childTrees is None:
            childTrees = []
        self.childTrees = childTrees


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if not isinstance(obj, Tree):
        #     return super(MyEncoder, self).default(obj)
        return obj.__dict__

# if __name__ == '__main__':
#     c1 = Tree("c1")
#     c2 = Tree("c2")
#     t = Tree("t",[c1,c2])

#     print (json.dumps(t, cls=MyEncoder))
