from utils import formula_data


class Block:
    def __init__(self, group, name):
        self.__group = group
        self.__name = name

    def __repr__(self):
        return f'Block{{group={self.__group!r}, name={self.__name!r}}}'

    def __str__(self):
        return self.__repr__()

    @property
    def group(self):
        return self.__group

    @property
    def name(self):
        return self.__name

    @property
    def blockData(self) -> dict:
        return formula_data[self.__group][self.__name]

    @property
    def desc(self) -> str:
        return self.blockData['desc']

    @property
    def formula(self) -> list:
        return self.blockData['formula']

    @property
    def outputQtys(self):
        s = []
        for i in self.formula:
            s.append(i['outputQty'])
        return s


def blockFactory(blockName) -> Block:
    for k, v in formula_data.items():
        if blockName in v:
            return Block(k, blockName)
