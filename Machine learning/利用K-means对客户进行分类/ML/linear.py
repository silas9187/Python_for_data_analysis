# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187
import numpy as np


# 一元线性回归
class SimpleLinearRegression():
    def __init__(self):
        self.a_ = None
        self.b_ = None

    # 1. 拟合训练数据
    def fit(self, x_train, y_train):
        assert len(x_train) == len(y_train), 'x_train与y_train长度相同'
        assert x_train.ndim == 1, "只支持一个特征"
        x_mean = np.mean(x_train)
        y_mean = np.mean((y_train))
        u, v = 0, 0
        for x_i ,y_i in zip (x_train, y_train):
            u += (x_i - x_mean)*(y_i - y_mean)
            v += (x_i - x_mean)**2
        self.a_ = u / v
        self.b_ = y_mean - self.a_ * x_mean
        return self

    # 预测数据
    def predict(self, x_predict):
        assert self.a_ is not  None, '请先调用fit函数'
        assert x_predict.ndim == 1, '只支持一个特征'
        return np.array([self.a_ * x + self.b_ for x in x_predict])


# 多元线性回归
class LinearRegression():
    def __init__(self):
        self._theta = None

    # 拟合训练数据
    def fit(self, X_train, y_train):
        assert X_train.shape[0] == y_train.shape[0], 'X_train与y_train的长度要相等'
        X = np.hstack([np.ones((len(X_train), 1)), X_train])  # 在原数据集上堆叠全为1的一列
        self._theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y_train)
        return self

    # 2.预测
    def predict(self, X_predict):
        assert self._theta is not None, '请先调用fit方法'
        assert X_predict.shape[1] == len(self._theta) - 1, 'X_predict的特征数量应与X_train的长度相等'

        X = np.vstack([np.ones((len(X_predict), 1)), X_predict])  # 在预测数据集上堆叠全为1的一列
        return X.dot(self._theta)

    # 3.准确率的判断
    def score(self,X_test, y_test):
        y_predict = self.predict(X_test)
        return r2_score(y_test, y_predict)


# MSE- 均方误差
def mean_squared_error(y_true, y_predict):
    assert len(y_true) == len(y_predict), 'y_true的长度需与y_predict相同'
    return np.sum(y_true - y_predict)**2 / len(y_true)


# R2
def r2_score(y_true, y_predict):
    return 1 - mean_squared_error(y_true, y_predict) / np.var(y_true)
