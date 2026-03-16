from src.{developer}.{name}.Main import Main
from PyForge import init

import os

if __name__ == '__main__':
    init()
    Main(os.path.dirname(os.path.abspath(__file__))).start()