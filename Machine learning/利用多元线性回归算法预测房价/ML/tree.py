# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187
import  numpy as np
from collections import Counter
from .metrics import accuracy_score


# 计算基尼系数
# 传入特征数据
def gini(y):
    counter = Counter(y)
    result = 0
    for v in counter.values():
        result += (v/len(y))**2
    return 1- result


# 根据计算相应维度值之间的平均值拆分训练数据
def cut(X, y, d, v):
    ind_left = (X[:, d] <= v)
    ind_right = (X[:, d] > v)
    return X[ind_left],X[ind_right], y[ind_left], y[ind_right]


# 划分训练数据，找出最优的整体基尼系数
def try_split(X, y, min_samples_leaf):

    best_g = 1
    best_d = -1
    best_v = -1
    for d in range(X.shape[1]):
        sorted_index = np.argsort(X[:, d])
        # 划分次数
        for i in range(len(X)-1):
            if X[sorted_index[i], d] == X[sorted_index[i+1], d]:
                continue
            v = (X[sorted_index[i], d] + X[sorted_index[i+1],d])/2
            X_left, X_right, y_left, y_right = cut(X, y,d, v)
            g_all = gini(y_left) + gini(y_right)
#             print('d={} v ={} g={}'.format(d, v, g_all))
            if g_all < best_g and len(y_left) >= min_samples_leaf and len(y_right) >= min_samples_leaf:
                best_g = g_all
                best_d = d
                best_v = v
    return best_d, best_v, best_g


# 定义节点类
class Node():
    def __init__(self, d=None, v=None, g=None, l=None):
        self.dim = d
        self.value = v
        self.gini = g
        self.label = l

        self.left = None
        self.right = None

    def __repr__(self):
        return 'Node(d={},v={},g={},l={})'.format(self.dim, self.value, self.gini, self.label)


class DecisionTreeClassifier():
    def __init__(self,  max_depth=2, min_samples_leaf=1):
        self.tree_ = None
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

    # 拟合训练数据的方法
    def fit(self, X, y):
        self.tree_ = self.create_tree(X, y)
        return self

    # 定义树类
    def create_tree(self, X, y, current_depth=1):
        if current_depth > self.max_depth:
            return None
        d, v, g = try_split(X, y, self.min_samples_leaf)

        if d == -1 or g == 0:
            return None
        node = Node(d, v, g)
        X_left, X_right, y_left, y_right = cut(X, y, d, v)
        node.left = self.create_tree(X_left, y_left, current_depth+1)
        if node.left is None:
            # 返回 分类的标签值
            label = Counter(y_left).most_common(1)[0][0]
            node.left = Node(l=label)
        node.right = self.create_tree(X_right, y_right, current_depth+1)
        if node.right is None:
            # 返回 分类的标签值
            label = Counter(y_right).most_common(1)[0][0]
            node.right = Node(l=label)
        return node

    # 预测
    def predict(self, X):
        assert self.tree_ is not None, '请先调用fit(方法'
        return np.array([self._predict(x, self.tree_) for x in X])

    # 预测一个数据
    def _predict(self, x, node):
        if node.label is not None:
            return node.label
        if x[node.dim] < node.value:
            # left
            return self._predict(x, node.left)
        else:
            # right
            return self._predict(x, node.right)

    # 准确率
    def score(self, X_test, y_test):
        y_predict = self.predict(X_test)
        return accuracy_score(y_test, y_predict)


