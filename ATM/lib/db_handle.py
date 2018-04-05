import json
import os
from conf import setting


def update(update_dic):
    path = r'%s/%s.json' % (setting.BASE_DB_LOCAL, update_dic['name'])
    with open(path, 'w', encoding='utf-8') as f:
        j = json.dump(update_dic, f)
        f.flush()


def get_dic_by_name(name):
    path = r'%s/%s.json' % (setting.BASE_DB_LOCAL, name)
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return False
