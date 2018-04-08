from interface import bank
from interface import user
from interface import shop
from lib import common

user_data = {
    'name': None,
    'is_auth': False,
}

def login():
    '''
    登录函数，密码输错三次锁定，用户名输错可以一直输入
    :return:
    '''
    print('请登录：')
    count = 0
    while True:
        name = input('please input username>>：').strip()
        if 'q' == name: break
        user_dic = user.get_userinfo_by_name(name)
        if count >= 3:
            # 锁定用户
            user.lock_user(name)
            print('try too many，user locked')
            break
        if user_dic:
            passwrod = input('please input password>>:').strip()
            if user_dic['password'] == passwrod and not user_dic['locked']:
                user_data['name'] = name
                user_data['is_auth'] = True
                print('login success')
                break
            else:
                print('password error or user locked')
                count += 1
                continue
        else:
            print('user do not exist')
            continue


def register():
    '''
    注册函数，登录了不能继续注册，已存在的用户不能再次注册
    :return:
    '''
    if user_data['is_auth']:
        print('you is login')
        return
    print('注册：')
    while True:
        name = input('please input username>>').strip()
        if 'q' == name: break
        user_dic = user.get_userinfo_by_name(name)
        if user_dic:
            print('user is exist')
            continue
        else:
            password = input('please input password>>').strip()
            password2 = input('please config password>>').strip()
            if password == password2:
                user.register_user(name, password)
                break
            else:
                print('password not equles')
                continue


@common.login_auth
def check_balance():
    balance = bank.get_balance_interface(user_data['name'])
    print('查看余额')
    print('您的余额为：%s' % balance)


@common.login_auth
def transfer():
    print('转账')
    while True:
        trans_name = input('please input transfer user(q to exit)>>').strip()
        if trans_name == user_data['name']:
            print('connot transfer to yourself')
            continue
        if 'q' == trans_name: break
        trans_dic = user.get_userinfo_by_name(trans_name)
        if trans_dic:
            trans_money = input('please input transfer money>>:').strip()
            if trans_money.isdigit():
                trans_money = int(trans_money)
                user_balance = bank.get_balance_interface(user_data['name'])
                if user_balance >= trans_money:
                    bank.transfer_interface(user_data['name'], trans_name, trans_money)
                    break
                else:
                    print('money not enough')
                    continue
            else:
                print('please input numbers')
                continue
        else:
            print('user do not exist')
            continue


@common.login_auth
def repay():
    print('还款')
    while True:
        repay_money = input('please input repay money(q to exit)>>:').strip()
        if 'q' == repay_money: break
        if repay_money.isdigit():
            repay_money = int(repay_money)
            bank.repay_interface(user_data['name'], repay_money)
            print('repay success')
            break
        else:
            print('please input number')
            continue


@common.login_auth
def withdraw():
    print('取款')
    while True:
        withdraw_money = input('please input withdraw money(q to exit)>>:').strip()
        if 'q' == withdraw_money: break
        if withdraw_money.isdigit():
            withdraw_money = int(withdraw_money)
            if bank.withdraw_interface(user_data['name'], withdraw_money):
                print('withdraw %s yuan success' % withdraw_money)
                break
            else:
                print('money not enough')
                continue
        else:
            print('please input numbers')
            continue


@common.login_auth
def check_record():
    print('您的银行流水为：')
    for record in bank.check_record(user_data['name']):
        print(record)


@common.login_auth
def shopping():
    print('购物')
    goods_list = [
        ['coffe', 30],
        ['chicken', 20],
        ['iPhone', 8000],
        ['macBook', 12000],
        ['car', 100000]
    ]
    shopping_cart = {}
    user_money = bank.get_balance_interface(user_data['name'])
    cost_money = 0
    while True:
        for i, item in enumerate(goods_list):
            print(i, item)
        choice = input('please choice goods or exit(q)>>:').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice < 0 or choice >= len(goods_list): continue
            goods_name = goods_list[choice][0]
            goods_price = goods_list[choice][1]
            if user_money >= goods_price:
                if goods_name in shopping_cart:  # 原来已经购买过
                    shopping_cart[goods_name]['count'] += 1
                else:
                    shopping_cart[goods_name] = {'price': goods_price, 'count': 1}
                user_money -= goods_price
                cost_money += goods_price
                print('%s add to shopping cart' % goods_name)
            else:
                print('money not enough')
                continue
        elif choice == 'q':
            print(shopping_cart)
            buy = input('buy or not (y/n)>>:').strip()
            if buy == 'y':
                #正常需要加密码验证
                if cost_money==0:break
                if shop.shopping_interface(user_data['name'], shopping_cart, cost_money):
                    print('buy success ')
                    break
                else:
                    print('buy error')
                    break

            else:
                print('you  buy nothing')
                break
        else:
            print('illegal input')
            continue


@common.login_auth
def look_shoppingcart():
    print('查看购物车')
    print(shop.look_shoppingcart(user_data['name']))
    # 此处可以详细拼接购物车


func_dic = {
    '1': login,
    '2': register,
    '3': check_balance,
    '4': transfer,
    '5': repay,
    '6': withdraw,
    '7': check_record,
    '8': shopping,
    '9': look_shoppingcart,
}


def run():
    while True:
        print('''
        1、登录
        2、注册
        3、查看余额
        4、转账
        5、还款
        6、取款
        7、查看流水
        8、购物
        9、查看购买商品
        ''')
        choose = input('choice>>:').strip()
        if choose not in func_dic: continue
        func_dic[choose]()
