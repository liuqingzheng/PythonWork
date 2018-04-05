from lib import common
from core import src
from lib import db_handle

logger_shopping = common.get_logger('Shopoing')
goods_list = [
    ['coffe', 30],
    ['chicken', 20],
    ['iPhone', 8000],
    ['macBook', 12000],
    ['car', 100000]
]


@common.login_auth
def shopping():
    print('购物')
    shopping_cart = src.current_user['shopping_cart']
    user_money = src.current_user['account']
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
                print('%s add to shopping cart' % goods_name)
            else:
                print('money not enough')
                continue
        elif choice == 'q':
            print(shopping_cart)
            buy = input('buy or not (y/n)>>:').strip()
            if buy == 'y':
                src.current_user['shopping_cart'] = shopping_cart
                src.current_user['account'] = user_money
                db_handle.update(src.current_user)
                logger_shopping.info('%s 购买了 %s' % (src.current_user['name'], src.current_user['shopping_cart']))
                print(src.current_user['shopping_cart'])
                print('buy success ')
                break
            else:
                print('you not buy goods')
                break
        else:
            print('illegal input')
            continue


@common.login_auth
def look_shoppingcart():
    print('查看购买商品')
    print(src.current_user['shopping_cart'])
    logger_shopping.info('%s 查看了购物车' % src.current_user['name'])
