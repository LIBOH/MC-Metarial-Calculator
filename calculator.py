from decimal import Decimal, getcontext

from colorama import init, Fore

from blocks_mro import Block, block_factory
from utils import blocks_registry, utils_checkIgnore

getcontext().rounding = "ROUND_DOWN"
custom_exp = getcontext().exp( Decimal( "0" ) )


# class Calculator:
#     STACK_COUNT = Decimal( 64 )
#
#     def __init__( self, block: Block, quantity: int ) -> None:
#         self.block = block
#         self.quantity = quantity
#         init()
#
#     def __repr__( self ) -> str:
#         return f"Calculator{{ Block={self.block.block_name}, Quantity={self.quantity}, Total_Recipes={self.d_tr}, Total_To_Recipes={self.d_tts}, Inner_Recipes={self.d_ir} }}"
#
#     def __str__( self ) -> str:
#         return self.__repr__()
#
#     def __getChange( self, total, flag=False ) -> Decimal:
#         """计算材料找零
#
#         Args:
#             total: 从 get_total_recipe 计算得到的所需材料的总数
#             flag: 表示 self.block.outputQty 的值不等于一. Defaults to False.
#
#         Returns:
#             材料的找零  例如: 制作77个红石粉需要 红石块: (0 x 64 + 8) + {5} 个红石粉, 其中 {} 中的值为通过该方法得到
#         """
#
#         if flag:
#             return Decimal( self.quantity - total )
#
#         return Decimal( self.quantity - total * self.block.outputQty )
#
#     def __getTextLength( self, text: str ) -> int:
#         """计算文本长度
#
#         Args:
#             text: 需要计算长度的文本
#
#         Returns:
#             计算过的最长的文本
#         """
#         text_length = len( text )
#         text_length = max( len( text ), text_length )
#         return text_length
#
#     def __calculateOutput(
#             self,
#             total_recipe: dict[str:int],
#             total_to_stacks: dict[str:str],
#             inner_recipe: list[dict],
#             output_color: str,
#             inner_output_color: str,
#             beautify: bool,
#     ) -> None:
#         """打印材料的计算结果
#
#         Args:
#             total_recipe: 用户所查询的方块的总配方
#             total_to_stacks: 总配方按组显示
#             inner_recipe: 总配方中需另外制作的方块的配方
#             output_color: 用于更改本方法所打印内容的颜色
#             inner_output_color: 用于更改打印需另外制作的配方的颜色
#             beautify: 需另外制作的方块的配方是否启用美化输出
#         """
#         t_l = self.__getTextLength( str( total_to_stacks ) )
#         self.d_tr = total_recipe
#         self.d_tts = total_to_stacks
#         self.d_ir = inner_recipe
#
#         print( f"{output_color if output_color else Fore.RESET}", end="" )
#         print( total_recipe )
#         print( total_to_stacks )
#
#         output_dividing_line = "-" * (t_l + 8)
#         is_ignore = utils_checkIgnore( self.block.block_name )
#
#         if not is_ignore:
#             print( output_dividing_line )
#             if beautify:
#                 self.__innerOutput( inner_output_color )
#             else:
#                 print( inner_recipe )
#
#         else:
#             print( f"{output_dividing_line}\n" )
#
#     def __innerOutput( self, output_color=None ) -> None:
#         """需另外制作的方块的配方
#
#         Args:
#             output_color: 用于更改本方法所打印内容的颜色. Defaults to None.
#         """
#         t_len = 0
#         for result in self.result_list:
#             t_len = self.__getTextLength( str( result ) ) + 3
#
#         inner_output_dividing_line = "-" * t_len
#         for recipe in self.inner_recipe:
#             print( f"{output_color if output_color else Fore.RESET}", end="" )
#             print( f"其中制作 {recipe[1]} 个{recipe[0]}需要:" )
#             print( recipe[2] )
#             print( inner_output_dividing_line )
#
#         print( "\n" )
#
#     def getTotalRecipe( self ) -> dict[str:int]:
#         """计算用户所查询的方块的总配方
#
#         Returns:
#             包含配方的字典 -> {'红石粉': 90, ...}
#         """
#         # 此方法计算 self.block.outputQty != 1 的 block 是不准确的，可能会少不足一组的数量
#         # 而 get_total_to_stacks 方法获取的是准确的
#         total_recipe = { }
#         if self.block.outputQty == 1:
#             for recipe in self.block.recipes:
#                 for k, v in recipe.items():
#                     # @k: 制作 self.block 的配方中的材料名
#                     # @v: 制作 self.block 的配方中材料所需要的数量
#                     total_recipe.update( { k: v * self.quantity } )
#
#         else:
#             for recipe in self.block.recipes:
#                 for k, v in recipe.items():
#                     # @k: 制作 self.block 的配方中的材料名
#                     num = Decimal(
#                         Decimal( self.quantity ) / Decimal( self.block.outputQty )
#                     ).quantize( custom_exp )
#                     total = num * v
#
#                     total_recipe.update( { k: int( total ) } )
#
#         return total_recipe
#
#     def getTotalToStacks( self ) -> dict[str:str]:
#         """计算总配方按组显示
#
#         Returns:
#             包含按组显示的配方的字典 -> {'红石粉': '90 = (1 x 64 + 26)', ...}
#         """
#         total_to_stacks = dict()
#         recipe = self.getTotalRecipe()
#         for k, v in recipe.items():
#             # @k: 制作 self.block 的材料名
#             # @v: 制作 self.block 对应的材料所需要的总数
#             total = Decimal( v )  # 所需材料的组数
#             stacks = Decimal( total / self.STACK_COUNT ).quantize( custom_exp )  # 所需材料的组数
#             amount = Decimal( total - stacks * self.STACK_COUNT ).quantize( custom_exp )  # 所需材料不足一组的找零
#
#             # !
#             print( k, total, stacks, amount, self.block.outputQty )
#
#             # 计算找零
#             change = 0
#             if self.block.outputQty == 1:
#                 if (v * self.block.outputQty) < self.quantity:
#                     change = self.__getChange( v )
#             else:
#
#                 for v2 in self.block.recipes.values():
#                     total = v / v2 * self.block.outputQty
#                     if total < self.quantity:
#                         change = self.__getChange( total, flag=True )
#
#                         # !
#                         # print(change)
#
#             text = f"{v} = ({stacks} x {self.STACK_COUNT} + {amount})"
#             if change != 0 and not utils_checkIgnore( k ):
#                 text += f" + {change} 个{self.block.block_name}"
#
#             total_to_stacks.update( { k: text } )
#
#         return total_to_stacks
#
#     def getInnerRecipe( self ) -> list[dict[str:str]]:
#         """计算总配方中需另外制作的方块的配方
#
#         Returns:
#             包含总配方中需另外制作的方块的配方的列表 -> [{'红石粉': '90 = (1 x 64 + 26)'}, {...}, ...]
#         """
#         self.inner_recipe = []
#         self.result_list = []
#         origin_recipe = self.getTotalRecipe()
#         for k, v in origin_recipe.items():
#             # @k: 制作 self.block 的配方中的材料所需要的配方的材料名
#             # @v: 制作 self.block 的配方中的材料所需要的配方的数量
#             if k in blocks_registry:
#                 self.inner_recipe.append( [k, v] )
#
#         for index, i_recipe in enumerate( self.inner_recipe ):
#             inner_block = Block( i_recipe[0] )
#             inner_calculator = Calculator( inner_block, i_recipe[1] )
#
#             result = inner_calculator.getTotalToStacks()
#             self.result_list.append( result )
#
#             for k, v in result.items():
#                 self.inner_recipe[index].append( f"{k}: {v}" )
#
#         return self.result_list
#
#     def calculate(
#             self, /, beautify=False, output_color=None, inner_output_color=None
#     ) -> None:
#         """计算用户所查询的方块的配方
#
#         Args:
#             beautify: 是否启用美化输出. Defaults to False.
#             output_color: 用于更改打印输出的颜色. Defaults to None.
#             inner_output_color: 用于更改打印输出需另外制作的配方的颜色. Defaults to None.
#         """
#         d_total_recipe = self.getTotalRecipe()
#         d_total_to_stacks = self.getTotalToStacks()
#         d_inner_recipe = self.getInnerRecipe()
#         self.__calculateOutput( d_total_recipe, d_total_to_stacks, d_inner_recipe, output_color, inner_output_color,
#                                 beautify )


# def main():
#     while True:
#         print( f"{Fore.GREEN}", end="" )
#         blockName = input( 'Enter block name (Enter "q" to quit): ' )
#         if blockName == "q":
#             exit( 0 )
#         try:
#             block = Block( blockName )
#         except ValueError as e:
#             print( f"{Fore.RED}!请重试输入, {e}" )
#             continue
#
#         blockQuantity = input( "Enter block quantity: " )
#         if blockQuantity.isdigit():
#             blockQuantity = int( blockQuantity )
#         else:
#             print( f"{Fore.RED}!请输入一个阿拉伯数字!" )
#             continue
#
#         print( "-" * 50 )
#         calculator = Calculator( block, blockQuantity )
#         calculator.calculate(
#             beautify=True, output_color=Fore.CYAN, inner_output_color=Fore.YELLOW
#         )


class Calculator:
    def __init__( self, block: Block, qty: int ):
        self.block = block
        self.qty = qty

    def getTotalRecipe( self ) -> dict[str:int]:
        """计算用户所查询的方块的总配方

        Returns:
            包含配方的字典 -> {'红石粉': 90, ...}
        """
        # 此方法计算 self.block.outputQty != 1 的 block 是不准确的，可能会少不足一组的数量
        # 而 get_total_to_stacks 方法获取的是准确的
        total_recipe = { }
        print(self.block.outputQty)

        if self.block.outputQty == 1:
            for recipe in self.block.recipes:
                for k, v in recipe.items():
                    # @k: 制作 self.block 的配方中的材料名
                    # @v: 制作 self.block 的配方中材料所需要的数量
                    total_recipe.update( { k: v * self.qty } )

        else:
            pass
            # for recipe in self.block.recipes:
            #     for k, v in recipe.items():
            #         # @k: 制作 self.block 的配方中的材料名
            #         num = Decimal(
            #             Decimal( self.qty ) / Decimal( self.block.outputQty )
            #         ).quantize( custom_exp )
            #         total = num * v
            #
            #         total_recipe.update( { k: int( total ) } )

        return total_recipe


if __name__ == "__main__":
    pass
    # main()
    b = block_factory( '红石中继器' )
    calc = Calculator( b, 10 )
    print( calc.getTotalRecipe() )
    # calc.calculate( beautify=True, output_color=Fore.CYAN, inner_output_color=Fore.YELLOW )
