

import os, sys

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
from core import src

if __name__ == '__main__':
    src.run()
