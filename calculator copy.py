import queue
from blocks_mro1 import Block, blockFactory
from utils1 import utils_checkStackCount


class Calculator:
    def __init__(self):
        self.__block_queue = queue.Queue()
        self.__block: Block | None = None
        self.__blockName: str = ''
        self.__blockQty: int = 0

    def calcTotalFormula(self):
        def multicalOutput(f: dict, outputCount: int):
            print(f)
            for k, v in f.items():
                count = self.blockQty // outputCount
                # print({k: v * count})

        def singleOutput():
            pass

        # print(self.__block.formula)
        for formula in self.__block.formula:
            if formula['outputQty'] == 1:
                return singleOutput()
            # print(formula['outputQty'])
            return multicalOutput(formula, formula['outputQty'])
        # for i in self.__block.outputQtys:
        #     return singleOutput() if i == 1 else multicalOutput(i)
        # pass

    @property
    def blockName(self) -> str:
        return self.__blockName

    @blockName.setter
    def blockName(self, value: str):
        self.__blockName = value
        self.__block = blockFactory(self.__blockName)

    @property
    def blockQty(self) -> int:
        return self.__blockQty

    @blockQty.setter
    def blockQty(self, value: int):
        self.__blockQty = value


if __name__ == '__main__':
    c = Calculator()
    c.blockName = '下界合金锭'
    c.blockQty = 64

    print(c.calcTotalFormula())
    # print(c.calcTotalStacks())
