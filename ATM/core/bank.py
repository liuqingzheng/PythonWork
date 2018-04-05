from lib import common
from lib import db_handle
from core import src
from lib import common

logger_bank = common.get_logger('Bnak')


@common.login_auth
def transfer():
    print('转账')
    while True:
        trans_name = input('please input transfer user(q to exit)>>').strip()
        if trans_name==src.current_user['name']:
            print('connot transfer to yourself')
            continue
        if 'q' == trans_name: break
        trans_dic = db_handle.get_dic_by_name(trans_name)
        if trans_dic:
            trans_money = input('please input transfer money>>:').strip()
            if trans_money.isdigit():
                trans_money = int(trans_money)
                if src.current_user['account'] >= trans_money:
                    src.current_user['account'] -= trans_money
                    trans_dic['account'] += trans_money
                    src.current_user['balance'].extend(
                        ['%s transfer %s yuan to %s ' % (src.current_user['name'],trans_money, trans_dic['name'] )])
                    db_handle.update(src.current_user)
                    db_handle.update(trans_dic)
                    logger_bank.info('%s 向 %s 转账 %s' % (src.current_user['name'], trans_name, trans_money))
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
            src.current_user['account'] += repay_money
            src.current_user['balance'].extend(['%s repay %s yuan' % (src.current_user['name'], repay_money)])
            db_handle.update(src.current_user)

            logger_bank.info('%s 还款 %s 元' % (src.current_user['name'], repay_money))
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
            if src.current_user['account'] >= withdraw_money * 1.05:
                src.current_user['account'] -= withdraw_money * 1.05
                src.current_user['balance'].extend(['%s withdraw %s yuan' % (src.current_user['name'], withdraw_money)])
                db_handle.update(src.current_user)

                logger_bank.info('%s 取款 %s 元' % (src.current_user['name'], withdraw_money))
                print('withdraw %s yuan success' % withdraw_money)
                break
            else:
                print('money not enough')
                continue
        else:
            print('please input numbers')
            continue


@common.login_auth
def check_balance():
    print('查看余额')
    print('您的余额为：%s' % src.current_user['account'])
    logger_bank.info('%s 查看了余额' % src.current_user['name'])


@common.login_auth
def check_record():
    print('您的银行流水为：')
    for balance in src.current_user['balance']:
        print(balance)
    logger_bank.info('%s 查看了银行流水' % src.current_user['name'])
