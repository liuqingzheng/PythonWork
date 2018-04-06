import logging.config
from core import src
from  conf import setting

# 登录认证装饰器
def login_auth(func):
    def wrapper(*args, **kwargs):
        if src.user_data['is_auth']:
            return func(*args, **kwargs)
        else:
            print('没有登录')

    return wrapper

def get_logger(name):

    logging.config.dictConfig(setting.LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(name)  # 生成一个log实例
    return logger


