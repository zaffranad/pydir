import os

import fire
from directory_tree import display_tree


class MainClass(object):
    """A simple class"""

    @staticmethod
    def process(name):
        print(f'Hi, {name}')

        display_tree(name)
        # walk = os.walk(name)
        # for (dir_path, dir_names, file_names) in walk:
        #     print(dir_path + ':')
        #     print(dir_names)
        #     print(file_names)


if __name__ == '__main__':
    fire.Fire(MainClass)
