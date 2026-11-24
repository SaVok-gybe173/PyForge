from src.main import main
from PyForge import init

import os

if __name__ == '__main__':
    init()
    main(os.path.dirname(os.path.abspath(__file__)))