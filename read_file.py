import os

# 指定文件夹路径
folder_path = '你的文件夹路径\\output'

# 存储歌手、专辑和歌曲的列表
artists = []
albums = []
songs = []

# 遍历文件夹
for root, dirs, files in os.walk(folder_path):
    if os.path.basename(root) == 'output':
        # 提取专辑名
        for dir in dirs:            
            artists.append(dir)

    else:
        for dir in dirs:
            albums.append(dir)
        # 提取歌曲名
        os = os.path.join(root, dir)
        for file in files:
            if file.endswith('.txt'):
                song_name = file.split('.txt')[0]
                songs.append(song_name)

# 写入文件
with open('artists.txt', 'w', encoding='utf-8') as artist_file:
    for artist in artists:
        artist_file.write(artist + '\n')

with open('albums.txt', 'w', encoding='utf-8') as album_file:
    for album in albums:
        if album not in artists and album != "其它":
            album_file.write(album + '\n')


with open('songs.txt', 'w', encoding='utf-8') as song_file:
    for song in songs:
        if song not in albums and song not in artists and song != "其它":
            song_file.write(song + '\n')

print("完成！")
