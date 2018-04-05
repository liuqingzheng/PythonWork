import os
import logging.config
from core import src
from  conf import setting

# 登录认证装饰器
def login_auth(func):
    def wrapper(*args, **kwargs):
        if not src.current_user:
            print('没有登录')
        else:
            return func(*args, **kwargs)

    return wrapper

def get_logger(name):

    logging.config.dictConfig(setting.LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(name)  # 生成一个log实例
    return logger


