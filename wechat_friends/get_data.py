# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187
import itchat


# 获取微信数据
def get():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)
    return friends
# get()


# 处理数据
def parse(data):
    friends = []
    for item in data[1:]:
        friend = {
            'NickName': item['NickName'],
            'RemarkName': item['RemarkName'],
            'Sex': item['Sex'],
            'Province': item['Province'],
            'City': item['City'],
            'Signature': item['Signature'].replace(' ', '').replace('\n', ';').replace('，', '？'),
            'StarFriend': item['StarFriend'],
            'ContactFlag': item['ContactFlag']
        }
        print(friend)
        friends.append(friend)
    return friends


# 储存数据
def save():
    friends = parse(get())
    for item in friends:
        with open('wechatfriends.txt', mode='a', encoding='utf-8') as f:
            f.write('%s,%s,%d,%s,%s,%s,%d,%d'%(item['NickName'],item['RemarkName'],item['Sex'],item['Province'],item['City'],item['Signature'],item['StarFriend'], item['ContactFlag']))
            f.write('\n')


save()