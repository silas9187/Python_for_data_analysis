# -*- coding: utf-8 -*-
# @Author  : Silas9187
# @Email   : silas9187@gmail.com
# @blogsite  :https://blog.csdn.net/acarsar
# @GitHub    :https://github.com/silas9187
import pyecharts


# 1.好友性别比例
def friends_sex():
    sex = []
    with open('wechatfriends.txt', mode='r',encoding='utf-8') as f:
        rows = f.readlines()
        for i in rows:
            # if (i.split(',')[2]) == '':
            #     pass
            # print(i.split(','))
            sex.append(i.split(',')[2])
        labels = ['汉子', 'lady', '性别不明']
        value = [sex.count('1'), sex.count('2'), sex.count('0')]
        pie = pyecharts.Pie('好友性别比例', '好友总人数：%d'%len(sex), title_pos='center')
        pie.add('', labels, value, radius=[30, 75], is_label_show=True, legend_orient="vertical", legend_pos="left",)
        pie.render('微信好友性别比例.html')
# friends_sex()
# 2. 好友位置分析
from collections import Counter
from pyecharts import Geo, Bar
import json


def location():
    cities = []
    with open('wechatfriends.txt', mode='r',encoding='utf-8') as f:
        rows2 = f.readlines()
        for i in rows2:
            city = i.split(',')[3]
            if '\u4e00' <= city <= '\u9fa5':  # 获取好友地区为中文的城市
                cities.append(city)
    data = Counter(cities).most_common()
    # for i in range(len())
    print(data)
    geo = Geo('好友位置分布', '', title_color='#fff', title_pos='center', width=1400, height=800, background_color='#404a59')
    # geo.add_coordinate('江北', 106.57,29.60)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0,40],visual_text_color='#fff', symbol_size=10, is_visualmap=True, is_piecewise=True, visual_split_number=8)
    geo.render('好友位置分布.html')
    # 生成柱状图
    data_top20 = Counter(cities).most_common(20)
    bar = Bar('好友所在城市top20', '', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=True, visual_text_color='#fff', is_more_utils=True, is_label_show=True)
    bar.render('好友所在城市top20.html')


# location()
# 个性签名词云图
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS


def signatures_cloud():
    signatures = []
    with open('wechatfriends.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for i in rows:
            signature = i.split(',')[5]
            if signature != '':
                signatures.append(signature)
    f.close()
    split = jieba.cut(str(signatures), cut_all=False)
    words = ' '.join(split)
    stopwords = STOPWORDS.copy()
    stopwords.add('span')
    stopwords.add('span')
    stopwords.add('class')
    stopwords.add('emoji')
    stopwords.add('emoji1f334')
    stopwords.add('emoji1f388')
    stopwords.add('emoji1f33a')
    stopwords.add('emoji1f33c')
    stopwords.add('emoji1f633')
    bg_image = plt.imread('moon.jpeg')
    wc = WordCloud(width=1000, height=1000, background_color='white', mask=bg_image, font_path='simhei.ttf', stopwords=stopwords, max_font_size=400, random_state=50)
    wc.generate_from_text(words)
    # plt.imshow(wc)
    plt.axis('off')
    wc.to_file('个性签名云图.jpg')
# signatures_cloud()


# 拼接头像
import os,itchat
import math
from PIL import Image

# 获取微信头像
def get_iavatar():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)
    base_path = 'HeadImages'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    for friend in friends:
        username = friend['NickName']
        himage = itchat.get_head_img(userName=friend['UserName'])
        if friend['RemarkName'] != '':
            himage_name = friend['RemarkName']
        else:
            himage_name = friend['NickName']
        himage_file = os.path.join(base_path, himage_name + '.jpg')
        print(himage_file)
        try:
            with open(himage_file, 'wb') as f:
                f.write(himage)
        except:
            pass

def image_connect():
    base_path = 'HeadImages'
    files = os.listdir(base_path)
    each_size = int(math.sqrt(float(640*640)/len(files)))
    lines = int(640/each_size)
    image = Image.new("RGB", (640, 640))
    x = 0
    y = 0
    for file_name in files:
        img = Image.open(os.path.join(base_path, file_name))
        img = img.resize((each_size,each_size), Image.ANTIALIAS)
        image.paste(img,(x * each_size, y * each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1
    image.save('im.jpg')

# get_iavatar()
image_connect()