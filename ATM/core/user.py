import json
import os

from lib import db_handle
from lib import common
from conf import setting

logger_user = common.get_logger('user')


# 通过用户名获取用户信息接口
def get_userinfo_by_name(name):
    return db_handle.select(name)


# 锁定用户接口
def lock_user(name):
    user_dic = db_handle.select(name)
    user_dic['locked'] = True
    db_handle.update(user_dic)
    logger_user.info('%s 被锁定了' % name)


# 解锁用户接口
def unlock_user(name):
    user_dic = get_userinfo_by_name(name)
    user_dic['locked'] = False
    db_handle.update(user_dic)
    logger_user.info('%s 被解锁了' % name)


# 注册用户接口
def register_user(name, password, banlance=15000):
    user_dic = {'name': name, 'password': password, 'locked': False, 'account': banlance, 'credit': banlance,
                'shopping_cart': {}, 'bankflow': []}
    db_handle.update(user_dic)
    logger_user.info('%s 注册了' % name)
