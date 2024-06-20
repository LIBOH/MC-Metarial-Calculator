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
    def getBlockGroup(groupPath):
        for v in groupPath.values():
            with open(v, 'r', encoding='utf-8') as f:
                formula_data.update(json.load(f))

    with open(filePath, 'r', encoding='utf-8') as f:
        getBlockGroup(json.load(f))


def __util_registerBlocks():
    for group_name, formula in formula_data.items():
        data = []
        for block_name in formula:
            data.append(block_name)
        blocks_registry.update({group_name: set(data)})


def util_checkRegistered(blockName: str) -> bool:
    """判断方块是否被注册

    Args:
        blockName (str): 受检测的方块名

    Returns:
        bool: True -> 已注册; 
              False -> 未注册
    """
    for v in blocks_registry.values():
        return blockName in v


def util_isIgnore(targetBlock: str) -> bool:
    """判断材料是否在忽略列表内

    Args:
        target_block (str): 受检测的方块名

    Returns:
        bool: True -> 已忽略; 
              False -> 未忽略
    """    
    return targetBlock in IGNORES

def util_checkStackCount(blockName: str) -> int:
    """检查方块为 16堆叠 还是 64堆叠

    Args:
        blockName (str): 所查询的方块名

    Returns:
        int: 最大堆叠数量: 16 or 64 
    """
    return STACK_16 if blockName in STACK_16_BLOCKS else STACK_64


__util_getRecipesBook(FORMULA_PTAH)
__util_registerBlocks()
