from core import bank
from core import user
from core import shop

current_user = None
func_dic = {
    '1': user.login,
    '2': user.register,
    '3': bank.check_balance,
    '4': bank.transfer,
    '5': bank.repay,
    '6': bank.withdraw,
    '7': bank.check_record,
    '8': shop.shopping,
    '9': shop.look_shoppingcart
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
