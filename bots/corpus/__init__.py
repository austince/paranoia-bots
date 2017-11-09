from __future__ import unicode_literals

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def load_corpus(filename):
    """

    :param filename:
    :return:
    """
    corp = []
    with open(os.path.join(dir_path, filename + ".txt")) as word_file:
        for line in word_file:
            line = line.decode('utf-8')
            if not line.startswith('#') and line != '\n' and len(line) > 0:
                corp.append(line.strip())
        if 'books' in filename:
            corp = " ".join(corp)
    return corp
