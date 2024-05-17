from decimal import Decimal, getcontext

from colorama import init, Fore

from blocks_mro import Block, block_factory
from utils import blocks_registry, utils_isIgnore

getcontext().rounding = "ROUND_HALF_UP"
cus_exp = getcontext().exp(Decimal("0"))


class Calculator:
    def __init__(self, block: Block, qty: int):
        self.block = block
        self.qty = qty
        init()

    def __recipesParser(self):
        for recipe in self.block.recipes:
            fields = list(recipe.keys())
            nums = list(recipe.values())

            yield nums[0], fields, nums

    def __isSingleQty(self, r: tuple) -> bool:
        return True if r[0] == 1 else False

    def getTotalRecipe(self) -> list:
        """计算用户所查询的方块的总配方

        Returns:
            包含配方的字典 -> {'outputQty': 10, '红石粉': 90, ...}
        """

        # 当此方法计算产量不等于1的方块时，其计算结果会多出一些.
        # When this method calculates the number of blocks produced that is not equal to 1,
        #   -the result it's going to add up a little bit.

        # 但 getTotalToStacks 方法获取的是准确的
        # But the getTotalToStacks method is accurate

        def getSingleQtyRecipe(parsedRecipe: tuple) -> dict:
            count = parsedRecipe[0]
            recipe_fields = parsedRecipe[1]
            recipe_qty = parsedRecipe[2]

            recipe_fields.insert(0, "count")

            total_nums = [count]
            for i in recipe_qty:
                total_nums.append(self.qty * i)

            return dict(zip(recipe_fields, total_nums))

        def getMultiQtyRecipe(parsedRecipe: tuple) -> dict:
            count = parsedRecipe[0]
            recipe_fields = parsedRecipe[1]
            recipe_qty = parsedRecipe[2]

            recipe_fields.insert(0, "count")

            countOfRecipes = Decimal(self.qty / count).quantize(cus_exp)

            multi_total_nums = [count]
            for i in recipe_qty:
                multi_total_nums.append(int(i * countOfRecipes))

            return dict(zip(recipe_fields, multi_total_nums))

        result_list = []
        for i in self.__recipesParser():
            if self.__isSingleQty(i):
                result_list.insert(0, getSingleQtyRecipe(i))
            else:
                result_list.append(getMultiQtyRecipe(i))

        return result_list

    def getTotalToStacks(self):

        def wrapper(recipe: dict) -> list:
            data = dict()
            for k, v in recipe.items():
                if k in ['count', 'outputQty']:
                    continue
                stacks = Decimal(v / self.block.stack).quantize(cus_exp)
                amount = Decimal(v - stacks * self.block.stack).quantize(cus_exp)

                data.update({k: {"outputQty": recipe['count'], "stacks": int(stacks), "amount": int(amount)}})
            
            return data

        def getChange(source: dict):
            # print( source )
            # fields = list( source.keys() )
            # qty = list(source.values())
            # a = []
            # if source["count"] != 1:
            #     pass
            
            # for i in qty[2:]:
            #     # print( i )
            #     Decimal(  )
            for block_name, data in source.items():
                a = Decimal(self.qty - data['stacks'] * data['outputQty'])
                print( a )

        total_recipes = self.getTotalRecipe()
        print( total_recipes )
        for i in total_recipes:
            print( wrapper(i) )
            
            
        pass


if __name__ == "__main__":
    pass
    # main()
    b = block_factory("下界合金锭")
    calc = Calculator(b, 100)
    # print(calc.getTotalRecipe())
    calc.getTotalToStacks()
    # calc.calculate( beautify=True, output_color=Fore.CYAN, inner_output_color=Fore.YELLOW )
