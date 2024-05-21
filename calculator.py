from decimal import Decimal, getcontext
from collections import namedtuple

from colorama import Fore

from blocks_mro import Block, blockFactory
from utils import util_checkStackCount, util_checkRegistered, util_isIgnore

Material = namedtuple('Material', ['name', 'count', 'outputCount'])
getcontext().rounding = 'ROUND_UP'


class Calculator:
    def __init__(self):
        self.__block: Block | None = None
        self.__blockName: str = ''
        self.__blockQty: int = 0

    def __output(self, outputType: str, _material: Material, stack_count: int, stack_num: int, ):
        match outputType:
            case 'single':
                print(f'<{_material.name}: {_material.count} '
                      f'= {stack_count} x {stack_num} + {_material.count - (stack_count * stack_num)}>')

            case 'multical':
                print(f'<{_material.name}: {_material.count} '
                      f'= {stack_count} x {stack_num} + {_material.count}>')

            case _:
                print('Unknown Output Type!')

    def calcTotalFormula(self, block: Block = None, blockQty: int = 0):
        def singleOutput(f: dict):
            outputQty = 0
            single_result = []
            for k, v in f.items():
                if k == 'outputQty':
                    outputQty = v
                    continue

                single_result.append(Material(k, blockQty if blockQty else self.blockQty * v, outputQty))
            return single_result

        def multicalOutput(f: dict):
            count = 0
            outputQty = 0
            multical_result = []
            for k, v in f.items():
                if k == 'outputQty':
                    count = Decimal((blockQty if blockQty else self.__blockQty) / v).quantize(Decimal('0'), 'ROUND_UP')
                    outputQty = v
                    continue

                multical_result.append(Material(k, v * count, outputQty))
            return multical_result

        for formula in (block.formula if block else self.__block.formula):
            if formula['outputQty'] == 1:
                yield singleOutput(formula)
                continue
            yield multicalOutput(formula)

    def calcTotalToStacks(self, isInner: bool = False):
        print(Fore.LIGHTYELLOW_EX + '-' * 30) if isInner else print(Fore.LIGHTCYAN_EX + '-' * 30)
        print(f'制作{self.blockQty}个{self.blockName}需要:')

        def singleOutput(_material: Material, _stack_num: int, _stack_count: int):
            self.__output('single', material, _stack_count, stack_num)

        def multicalOutput(_material: Material, _stack_num: int, _stack_count: int):
            material_total_count = _material.count * _material.outputCount
            if material_total_count < self.blockQty:
                self.__output('multical', _material, _stack_count, stack_num)
                return
            self.__output('multical', _material, _stack_count, stack_num)

        for i in self.calcTotalFormula():
            for material in i:
                stack_num = util_checkStackCount(material.name)
                stack_count = material.count // stack_num
                if material.outputCount == 1:
                    singleOutput(material, stack_num, stack_count)
                else:
                    multicalOutput(material, stack_num, stack_count)

    def calcInnerFormula(self):
        for formulas in self.calcTotalFormula():
            for material in formulas:
                if util_isIgnore(material.name):
                    continue
                if not util_checkRegistered(material.name):
                    continue
                self.blockName = material.name
                self.blockQty = material.count
                self.calcTotalToStacks(isInner=True)

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


def main(_calculator):
    print()
    while True:
        while True:
            print(Fore.LIGHTGREEN_EX, end='')
            print('-' * 40)
            block_name = input('要制作的方块名(输入q或Q退出)：')
            if block_name in ['q', 'Q']:
                exit(0)
            if util_checkRegistered(block_name):
                _calculator.blockName = block_name
                print(_calculator.blockName)
                break

        while True:
            block_qty = input('要制作的数量：')
            if block_qty.isdigit():
                _calculator.blockQty = int(block_qty)
                break
        _calculator.calcTotalToStacks()
        _calculator.calcInnerFormula()


if __name__ == '__main__':
    calculator = Calculator()
    main(calculator)
