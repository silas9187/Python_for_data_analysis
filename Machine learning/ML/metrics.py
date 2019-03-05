# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187


def accuracy_score(y, y_predict):
    '''计算准确率'''

    assert y.shape[0] == y_predict.shape[0], \
        'y与y_predict长度需要相同'

    return sum(y == y_predict) / len(y)