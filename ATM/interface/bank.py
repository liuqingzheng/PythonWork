from db import db_handle
from lib import common
from interface import user

logger_bank = common.get_logger('Bnak')


def transfer_interface(from_name, to_name, account):
    '''
    转账接口
    :param from_name:
    :param to_name:
    :param account:
    :return:
    '''
    from_user_dic = user.get_userinfo_by_name(from_name)
    to_user_dic = user.get_userinfo_by_name(to_name)
    if from_user_dic['account']>=account:
        from_user_dic['account'] -= account
        to_user_dic['account'] += account
        # 记录流水
        from_user_dic['bankflow'].extend(['%s transfer %s yuan to %s' % (from_name, account, to_name)])
        to_user_dic['bankflow'].extend(['%s accept %s yuan from %s' % (to_name, account, from_name)])
        db_handle.update(from_user_dic)
        db_handle.update(to_user_dic)
        logger_bank.info('%s 向 %s 转账 %s' % (from_name, to_name, account))
        return True
    else:
        return False


def repay_interface(name, account):
    '''
    还款接口
    :param name:
    :param account:
    :return:
    '''
    user_dic = user.get_userinfo_by_name(name)
    user_dic['account'] += account
    # 记录流水
    user_dic['bankflow'].extend(['%s repay %s yuan' % (name, account)])
    db_handle.update(user_dic)
    logger_bank.info('%s 还款 %s 元' % (name, account))


def get_balance_interface(name):
    '''
    查看余额接口
    :param name:
    :return:
    '''
    # user_dic=user.get_userinfo_by_name(name)
    # return user_dic['account']
    # logger_bank.info('%s 查看了余额' % (name))
    return user.get_userinfo_by_name(name)['account']


def consum_interface(name, account):
    '''
    消费接口
    :param name:
    :param account:
    :return:
    '''
    user_dic = user.get_userinfo_by_name(name)
    if user_dic['account']>=account:
        user_dic['account'] -= account
        # 记录流水
        user_dic['bankflow'].extend(['%s consum %s yuan' % (name, account)])
        db_handle.update(user_dic)
        logger_bank.info('%s 消费 %s 元' % (name, account))
        return True
    else:
        return False


def withdraw_interface(name, account):
    '''
    取款接口（扣手续费）
    :param name:
    :param account:
    :return:
    '''
    user_dic = user.get_userinfo_by_name(name)
    if user_dic['account']>=account * 1.05:
        user_dic['account'] -= account * 1.05
        # 记录流水
        user_dic['bankflow'].extend(['%s withdraw %s yuan' % (name, account)])
        db_handle.update(user_dic)
        logger_bank.info('%s 取款 %s 元' % (name, account))
        return True
    else:
        return False

def check_record(name):
    '''
    查看流水接口
    :param name:
    :return:
    '''
    current_user = user.get_userinfo_by_name(name)
    logger_bank.info('%s 查看了银行流水' % name)
    return current_user['bankflow']

