import jieba
import wordcloud as wc
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def make_word_cloud_map(content):
    content = content.encode('utf-8')
    # 词云图的形状mask
    mask = np.array(Image.open('util\\background.png'))
    # 设置停用词
    stopwords = set()
    with open('util\\hit_stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            stopwords.add(line.strip())
    text = ' '.join(jieba.lcut(content))
    wcobj = wc.WordCloud(
        font_path='util\\simkai.ttf',
        background_color='white',
        width=800,
        height=500,
        mask=mask,
        max_words=100,
        stopwords=stopwords
    )
    wcobj.generate(text)
    plt.imshow(wcobj, interpolation='bilinear')
    plt.axis('off')
    wcobj.to_file('media\\word_cloud_map.png')
