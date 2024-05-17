from utils import blocks_registry, blocks_groups, utils_checkInRegistry, utils_checkStackCount


class Block:
    def __init__(self, blockName: str, blockGroupName: str):
        self.__block_name = blockName
        self.__block_group_name = blockGroupName
        self.__stack = None
        self.__validate()

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}{{blockName="{self.block_name}", recipes={self.recipes}, '
                f'outputQty={self.outputQty}, desc="{self.desc}", stack={self.stack}}}')

    def __str__(self) -> str:
        return self.__repr__()

    def __validate(self):
        if not utils_checkInRegistry(self.__block_name):
            raise ValueError(f"无法创建名为 {self.__block_name} 的Block!")

        self._stack = utils_checkStackCount(self.__block_name)

    @property
    def block_name(self) -> str:
        return self.__block_name

    @property
    def recipes(self) -> list:
        return blocks_groups[self.__block_group_name][self.__block_name]["recipes"]

    # @property
    # def outputQty( self ) -> tuple:
    #     qty_list = []
    #     for i in range( len( self.recipes ) ):
    #         qty_list.append( self.recipes[i]['outputQty'] )
    #     return tuple( qty_list )

    @property
    def desc(self) -> str:
        return blocks_groups[self.__block_group_name][self.__block_name]['desc']

    @property
    def stack(self) -> int:
        return self._stack


def block_factory(block_name):
    for group_name, blocks in blocks_registry.items():
        if block_name in blocks:
            return Block(block_name, group_name)


if __name__ == '__main__':
    print(block_factory('红石中继器').__str__())
