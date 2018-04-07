import logging.config
from core import src
from  conf import setting

#
def login_auth(func):
    '''
    登录认证装饰器
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        if not src.user_data['is_auth']:
            print('没有登录')
            src.login()
        else:
            return func(*args, **kwargs)

    return wrapper

def get_logger(name):
    '''log日志
    '''
    logging.config.dictConfig(setting.LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(name)  # 生成一个log实例
    return logger


