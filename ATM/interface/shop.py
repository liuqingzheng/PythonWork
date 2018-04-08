from lib import common
from db import db_handle
from interface import user
from interface import bank

logger_shopping = common.get_logger('Shopoing')


def shopping_interface(name, shopping_cart, cost_money):
    '''
    购物接口
    :param name:
    :param shopping_cart:
    :param cost_money:
    :return:
    '''

    # 调用信用卡扣款接口付款
    if bank.consum_interface(name, cost_money):
        # 保存购物车
        user_dic = user.get_userinfo_by_name(name)
        user_dic['shopping_cart'] = shopping_cart
        db_handle.update(user_dic)
        logger_shopping.info('%s 花费 %s 购买了 %s' % (name, cost_money, shopping_cart))
        return True
    else:
        return False


def look_shoppingcart(name):
    '''
    查看购物车接口
    :param name:
    :return:
    '''
    user_dic = user.get_userinfo_by_name(name)
    logger_shopping.info('%s 查看了购物车' % name)
    return user_dic['shopping_cart']
