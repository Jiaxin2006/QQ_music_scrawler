import os
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from scipy.stats import norm,t,lognorm, expon
def search_files(files, root):
    results = []
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            song_name = os.path.basename(file).replace('.txt', '')
            folder_name = os.path.basename(root)
            if song_name != folder_name:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    song_name = os.path.basename(file).replace('.txt', '')
                    singer_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
                    results.append({
                        'name': song_name,
                        'singer': singer_name,
                        'path': file_path,
                        'content': content,
                    })
    return results
results = []
folder_path = 'E:\\Python\\output'
with ThreadPoolExecutor() as executor:
    futures = []
    for root, dirs, files in os.walk(folder_path):
        futures.append(executor.submit(search_files,files, root))

    for future in futures:
        results.extend(future.result())
lyrics_lengths = [len(song['content']) for song in results]
font_path = 'c:\Windows\Fonts\MSYH.TTC'
mean, std_dev = norm.fit(lyrics_lengths)
x = np.linspace(min(lyrics_lengths), max(lyrics_lengths), 1000)  # 调整x的范围以匹配直方图数据
y = norm.pdf(x, mean, std_dev)  # 使用norm.pdf来计算概率密度
fitted_result = f"Mean (μ): {mean:.2f}, Standard Deviation (σ): {std_dev:.2f}"
print(fitted_result)
count, bins, ignored = plt.hist(lyrics_lengths, bins=50, color='orange', edgecolor='black', alpha=0.7)
# 绘制正态分布曲线
plt.plot(x, y * len(lyrics_lengths) * np.diff(bins)[0], color='blue', linewidth=2)  # 调整y值以匹配直方图的高度
s, loc, scale = lognorm.fit(lyrics_lengths, floc=0)  # floc=0确保数据始终为正
print(f"对数正态分布参数: s={s:.2f}, loc={loc:.2f}, scale={scale:.2f}")

# 绘制直方图和拟合曲线
plt.hist(lyrics_lengths, bins=50, density=True, alpha=0.6, color='g')

# 对数正态分布曲线
x = np.linspace(0, max(lyrics_lengths), 1000)
plt.plot(x, lognorm.pdf(x, s, loc, scale), 'r-', lw=2, label='lognorm pdf')
plt.legend()

plt.title('Lyrics Length Distribution')
plt.xlabel('Lyrics Length')
plt.ylabel('Number of Songs')
plt.show()

lyrics_nums = [len(song['content'].split("\n")) for song in results]
mean, std_dev = norm.fit(lyrics_nums)
x = np.linspace(min(lyrics_nums), max(lyrics_nums), 100)  # 调整x的范围以匹配直方图数据
y = norm.pdf(x, mean, std_dev)  # 使用norm.pdf来计算概率密度
fitted_result = f"Mean (μ): {mean:.2f}, Standard Deviation (σ): {std_dev:.2f}"
print(fitted_result)
count, bins, ignored = plt.hist(lyrics_nums, bins=50, color='orange', edgecolor='black', alpha=0.7)

# 绘制正态分布曲线
plt.plot(x, y * len(lyrics_nums) * np.diff(bins)[0], color='blue', linewidth=2,label='norm pdf')  # 调整y值以匹配直方图的高度
s, loc, scale = lognorm.fit(lyrics_nums, floc=0)

# 打印对数正态分布参数
print(f"对数正态分布参数: s={s:.2f}, loc={loc:.2f}, scale={scale:.2f}")

# 对数正态分布曲线
x_lognorm = np.linspace(0, max(lyrics_nums), 100)
y_lognorm = lognorm.pdf(x_lognorm, s, loc, scale) * len(lyrics_nums) * np.diff(bins)[0]  # 调整y值以匹配直方图的高度
plt.plot(x_lognorm, y_lognorm, 'r-', lw=2, label='lognorm pdf')

plt.legend()
plt.xlim(min(lyrics_nums), max(lyrics_nums))
plt.title('Lyrics Length Distribution')
plt.xlabel('Lyrics Length')
plt.ylabel('Number of Songs')
plt.show()
# 绘制歌词行数直方图
plt.hist(lyrics_nums, bins=50, color='blue', edgecolor='black')
plt.title('Lyrics Line Count Distribution')
plt.xlabel('Number of Lines per Lyric')
plt.ylabel('Number of Songs')
plt.show()


# 绘制相关性直方图
# 进行线性拟合
coefficients = np.polyfit(lyrics_nums, lyrics_lengths, 1)
linear_fit = np.poly1d(coefficients)
# 计算线性相关性
correlation_coefficient = np.corrcoef(lyrics_lengths, lyrics_nums)[0, 1]
print(f'Linear Fit: y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}')
print(f'Correlation Coefficient: {correlation_coefficient:.2f}')
# 绘制散点图
plt.scatter(lyrics_nums, lyrics_lengths, color='orange', edgecolor='black', label='Data Points')
# 绘制拟合线
plt.plot(lyrics_nums, linear_fit(lyrics_nums), color='blue', label='Linear Fit')
plt.title('Lyrics Length vs. Line Count')
plt.xlabel('Number of Lines')
plt.ylabel('Lyrics Length')
plt.legend()
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from deepthulac import LacModel	# 分词模型
import numpy as np
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
all_lyrics = ' '.join([' '.join(song['content'].split('\n')[4:]) for song in results])
import csv
from collections import Counter
import jieba
# 提取以“词”、“曲”、“编曲”结尾的行
ending_lines = []
for song in results:
    lines = song['content'].split('\n')
    for line in lines:
        if line.endswith('词') or line.endswith('曲') or line.endswith('编曲') or line.startswith('词') or line.startswith('曲') or line.startswith('编曲') or line.startswith('男：') or line.startswith('女：') or line.startswith('合：'):
            continue
        else:
            ending_lines.append(line)
stopwords = ["http", "https", "n", "ryqq", "y", "song", "却","还","会","对","监制",
             "Detail", "qq", "com", "制作人", "词", "曲", "编曲","song Detail","M","的","你","我","/","啦","很","到","才","它","把","谁",
              "songDetail",".","Studio","(",")","@",":","：","-","在","着","是","就","也","又" ,"说","啊","再","the","oh",
              "了","一","有","都","制作","混音","Oh","去","让","而","he","me","OP","也","那" ,"you","me","(",")","人",
              "I","'","t","有限公司","这","能","要","像","为","他","不","和","没有","想","吧","弦乐","录音师","录音","母带"]
with open('e:\大一\大一上\人文与社会科学计算导论\第四次作业 词云绘制\虚词表.txt', 'r', errors='ignore') as f:
    for line in f.readlines():
        stopwords.append(line.strip())
with open('e:\stop_words.txt', 'r', errors='ignore') as f:
    for line in f.readlines():
        stopwords.append(line.strip())        
# 使用jieba分词
segments = []
for line in ending_lines:
    segments.extend(jieba.cut(line))
counter = Counter(segments)
dict = {}

def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'
with open('word_frequencies.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Frequency'])
    for word, frequency in counter.items():
        if word not in stopwords and all(is_chinese_char(c) for c in word):
            writer.writerow([word, frequency])
            dict[word] = frequency


# 使用WordCloud生成词云
wordcloud = WordCloud(font_path=font_path, 
                      width=800, height=400, 
                      background_color='white', 
                      stopwords=stopwords).generate_from_frequencies(dict)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 词汇频率比较
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import jieba
folder_path = 'E:\\Python\\output\\陈奕迅'
with ThreadPoolExecutor() as executor:
    futures = []
    for root, dirs, files in os.walk(folder_path):
        futures.append(executor.submit(search_files,files, root))

    for future in futures:
        results.extend(future.result())
ending_lines_eason = []
for song in results:
    lines = song['content'].split('\n')
    for line in lines:
        if line.endswith('词') or line.endswith('曲') or line.endswith('编曲') or line.startswith('词') or line.startswith('曲') or line.startswith('编曲') or line.startswith('男：') or line.startswith('女：') or line.startswith('合：'):
            continue
        else:
            ending_lines_eason.append(line)
segments = []
for line in ending_lines:
    segments.extend(jieba.cut(line))
counter_eason = Counter(segments)
dict_eason = {}
def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'
for word, frequency in counter_eason.items():
    if word not in stopwords and all(is_chinese_char(c) for c in word):
        dict_eason[word] = frequency
folder_path = 'E:\\Python\\output\\周杰伦'
with ThreadPoolExecutor() as executor:
    futures = []
    for root, dirs, files in os.walk(folder_path):
        futures.append(executor.submit(search_files,files, root))

    for future in futures:
        results.extend(future.result())
ending_lines_jay = []
for song in results:
    lines = song['content'].split('\n')
    for line in lines:
        if line.endswith('词') or line.endswith('曲') or line.endswith('编曲') or line.startswith('词') or line.startswith('曲') or line.startswith('编曲') or line.startswith('男：') or line.startswith('女：') or line.startswith('合：'):
            continue
        else:
            ending_lines_jay.append(line)
segments = []
for line in ending_lines:
    segments.extend(jieba.cut(line))
counter_jay = Counter(segments)
dict_jay = {}
def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'
for word, frequency in counter_jay.items():
    if word not in stopwords and all(is_chinese_char(c) for c in word):
        dict_jay[word] = frequency

# 归一化词频
total_eason = sum(dict_eason.values())
total_jay = sum(dict_jay.values())
normalized_eason = {word: freq / total_eason for word, freq in dict_eason.items()}
normalized_jay = {word: freq / total_jay for word, freq in dict_jay.items()}

combined_freq = {}
for word in set(normalized_eason.keys()).union(normalized_jay.keys()):
    combined_freq[word] = (normalized_eason.get(word, 0), normalized_jay.get(word, 0))

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    eason_freq, jay_freq = combined_freq.get(word, (0, 0))
    if eason_freq > jay_freq:
        return "red"
    elif jay_freq > eason_freq:
        return "blue"
    else:
        return "gray"

# 生成词云
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white', color_func=color_func)
wordcloud.generate_from_frequencies({word: eason_freq + jay_freq for word, (eason_freq, jay_freq) in combined_freq.items()})

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('eason(red) vs jay(blue) wordcloud')
plt.show()

from snownlp import SnowNLP
import matplotlib.pyplot as plt

def analyze_sentiment(lyrics):
    sentiments = []
    for line in lyrics:
        if len(line) > 0:
            sentiments.append(SnowNLP(line).sentiments)
    return sentiments

sentiments_eason = analyze_sentiment(ending_lines_eason)
sentiments_jay = analyze_sentiment(ending_lines_jay)
# 绘制情感倾向图
plt.figure(figsize=(14, 7))

plt.hist(sentiments_eason, bins=20, alpha=0.5, color='red', label='陈奕迅')
plt.hist(sentiments_jay, bins=20, alpha=0.5, color='blue', label='周杰伦')
plt.xlabel('sentiment inclination')
plt.ylabel('frequency')
plt.title('eason\'s sentiment inclination analysis')
plt.legend(loc='upper right')

plt.show()
print(sum(sentiments_eason)/len(sentiments_eason))
print(sum(sentiments_jay)/len(sentiments_jay))
