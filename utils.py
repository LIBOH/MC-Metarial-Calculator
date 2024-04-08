import os
import json

blocks_registry: dict = dict()
# {
#     ('RedstoneGroup', ('红石粉', '红石块')),
#     (..., (...))
# }

STACK_16 = 16
STACK_64 = 64
IGNORES = [
    "铁锭", "铜锭", "金锭", "绿宝石", "红石粉", "青金石", "钻石", "煤炭",
    "铁块", "铜块", "金块", "绿宝石块", "红石块", "青金石块", "钻石块", "下届合金块", "煤炭块"
]
STACK_16_BLOCKS = { "盔甲架" }


def __utils_getRecipesBookPath( editor: str = "Pycharm" ) -> dict:
    """
    获取 recipes.json 中引用的具体配方书的路径
    Args:
        editor: 使用的开发工具

    Returns: 方块组及其配方书的映射
        Looks like: {'xxx': 'path/to/your/xxx.json',
                     'yyy': 'path/to/your/yyy.json'}
    """
    paths = {
        # This path is using at Pycharm
        "Pycharm": "static/recipesBook.json",
        # This path is using at VSCode
        "VSCode": "pythonProject/MC Material Calculation/static/recipesBook.json",
    }

    with open( paths[editor], "r", encoding="utf-8" ) as f:
        return json.load( f )


def __utils_getBlockGroup( groupDict: dict ):
    """
    获取方块组的内容
    Args:
        groupDict: 方块组及其配方书的映射

    Returns:
        yield 方块组名, 及其组内所有方块信息
        当没有配方书对应的文件 return None.
    """
    for _group_name, group_path in groupDict.items():
        if not os.path.exists( group_path ):
            return
        with open( group_path, "r", encoding="utf-8" ) as f:
            yield _group_name, json.load( f ).get( _group_name )


def __utils_regeditBlocks( _group_name, _group_info: dict[dict] ) -> None:
    """将组内方块的配方注册到 blocks_registry

    Args:
        _group_name:
        _group_info: 包含组内方块的配方的字典
    """
    data = list()
    for k, v in _group_info.items():
        data.append( k )
    blocks_registry.update( { _group_name: tuple( data ) } )


def utils_checkInRegistry( block_name: str ) -> bool:
    """验证方块是否已注册

    Args:
        block_name: 要查询配方的方块名

    Returns:
        True: 已注册, False: 未知方块或不支持参与查询的方块
    """
    # for item in blocks_registry:
    #
    #     if block_name in blocks_registry:
    #         return True
    #     return False

    for k, v in blocks_registry.items():
        if block_name in v:
            return True

    else:
        return False


def utils_checkStackCount( block_name: str ) -> int:
    """检查方块为 16堆叠 还是 64堆叠

    Args:
        block_name: 所查询的方块名

    Returns:
        16堆叠 return 16, 64堆叠 return 64
    """
    if block_name in STACK_16_BLOCKS:
        return STACK_16

    return STACK_64


def utils_checkIgnore( target_block ) -> bool:
    """判断材料是否在忽略列表内
    :param target_block: 方块名
    :return: True: 在忽略列表内 or False: 不在忽略列表内
    """
    return target_block in IGNORES


blocks_groups = { }
path_dict = __utils_getRecipesBookPath()
for group_name, group_info in __utils_getBlockGroup( path_dict ):
    __utils_regeditBlocks( group_name, group_info )
    blocks_groups.update( { group_name: group_info } )

