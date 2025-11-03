"""Запускает cli интерфейс"""

import sys
import os
# from src.cli.cli import main

if not __package__:
    #  Сделать CLI запускаемым из исходного дерева с помощью
    # python src/pakage
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

if __name__ == "__main__":
    from src.cli.cli import main

    main()
