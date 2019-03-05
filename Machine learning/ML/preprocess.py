# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187
import numpy as np


"""对数据进行标准化"""


class StandardScaler:
    def __init__(self):
        self.mean_ = None  # 均值
        self.scale_ = None  # 标准差

    # 1.先拟合训练数据
    def fit(self, X):
        self.mean_ = np.mean(X, axis=0)  # 平均值
        self.scale_ = np.std(X, axis=0)  # 标准差
        return self  # 返回一个类的实例

    # 2. 标准化处理
    def transform(self, X):
        assert self.mean_ is not None and self.scale_ is not None, '请先调用fit（）方法'
        assert X.shape[1] == len(self.mean_), 'X的特征数量需要与fit时传入的数据相同'
        temp = np.empty(shape=X.shape[1], dtype=float)
        for col in range(X.shape[1]):
            temp[:, col] = (X[:, col] - self.mean_[col]) / self.scale_[col]
        return temp