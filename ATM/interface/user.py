
from db import db_handle
from lib import common

logger_user = common.get_logger('user')


def get_userinfo_by_name(name):
    '''
    通过用户名获取用户信息接口
    :param name:
    :return:
    '''
    return db_handle.select(name)


def lock_user(name):
    '''
    锁定用户接口
    :param name:
    :return:
    '''
    user_dic = db_handle.select(name)
    user_dic['locked'] = True
    db_handle.update(user_dic)
    logger_user.info('%s 被锁定了' % name)


def unlock_user(name):
    '''
    解锁用户接口
    :param name:
    :return:
    '''
    user_dic = get_userinfo_by_name(name)
    user_dic['locked'] = False
    db_handle.update(user_dic)
    logger_user.info('%s 被解锁了' % name)


def register_user(name, password, balance=15000):
    '''
    注册用户接口
    :param name:
    :param password:
    :param banlance:
    :return:
    '''
    user_dic = {'name': name, 'password': password, 'locked': False, 'account': balance, 'credit': balance,
                'shopping_cart': {}, 'bankflow': []}
    db_handle.update(user_dic)
    logger_user.info('%s 注册了' % name)
