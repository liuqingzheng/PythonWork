from lib import db_handle
from lib import common
from core import src

logger_user = common.get_logger('user')


# 登录功能
def login():
    print('请登录：')
    count = 0
    while True:
        name = input('please input username>>：').strip()
        if 'q' == name: break
        user_dic = db_handle.get_dic_by_name(name)
        if count >= 3:
            user_dic['locked']=True
            db_handle.update(user_dic)
            print('try too many，user locked')
            break
        if user_dic:
            passwrod = input('please input password>>:').strip()
            if user_dic['password'] == passwrod and not user_dic['locked']:
                print('login success')
                src.current_user = user_dic
                logger_user.info('%s 登录了' % src.current_user['name'])
                break
            else:
                print('password error or user locked')
                count += 1
                continue
        else:
            print('user do not exist')
            continue


# 注册功能
def register():
    print('注册：')
    while True:
        name = input('please input username>>').strip()
        if 'q' == name: break
        user_dic = db_handle.get_dic_by_name(name)
        if user_dic:
            print('user is exist')
            continue
        else:
            password = input('please input password>>').strip()
            password2 = input('please config password>>').strip()
            if password == password2:
                user_dic = {'name': name, 'password': password, 'locked': False, 'account': 15000, 'shopping_cart': {},'balance':[]}
                db_handle.update(user_dic)
                logger_user.info('%s 注册了' % name)
                break
            else:
                print('password not equles')
                continue
