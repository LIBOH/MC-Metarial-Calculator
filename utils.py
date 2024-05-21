import json

FORMULA_PTAH = 'static/recipesBook.json'
STACK_16 = 16
STACK_64 = 64
STACK_16_BLOCKS = {"盔甲架"}
IGNORES = [
    "铁锭", "铜锭", "金锭", "绿宝石", "红石粉", "青金石", "钻石", "煤炭",
    "铁块", "铜块", "金块", "绿宝石块", "红石块", "青金石块", "钻石块", "下届合金块", "煤炭块"
]

formula_data = {}
blocks_registry: dict = {}


def __util_getRecipesBook(filePath: str):
    data = []

    def getBlockGroup(groupPath):
        for k, v in groupPath.items():
            with open(v, 'r', encoding='utf-8') as f:
                formula_data.update(json.load(f))

    with open(filePath, 'r', encoding='utf-8') as f:
        getBlockGroup(json.load(f))


def __util_registerBlocks():
    for groupName, formula in formula_data.items():
        data = []
        for blockName in formula:
            data.append(blockName)
        blocks_registry.update({groupName: set(data)})


def util_checkRegistered(blockName: str) -> bool:
    for v in blocks_registry.values():
        return blockName in v


def util_isIgnore(target_block: str) -> bool:
    """判断材料是否在忽略列表内
    :param target_block: 方块名
    :return: True: 在忽略列表内 or False: 不在忽略列表内
    """
    return target_block in IGNORES


def util_checkStackCount(block_name: str) -> int:
    """检查方块为 16堆叠 还是 64堆叠

    Args:
        block_name: 所查询的方块名

    Returns:
        16堆叠 return 16, 64堆叠 return 64
    """
    if block_name in STACK_16_BLOCKS:
        return STACK_16

    return STACK_64


__util_getRecipesBook(FORMULA_PTAH)
__util_registerBlocks()
