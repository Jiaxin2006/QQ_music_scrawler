import requests
import re
from collections import defaultdict
import os
from bs4 import BeautifulSoup
import json
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options

URL = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?"

headers = {
    "origin": "https://y.qq.com",
    "referer": "https://y.qq.com/n/yqq/song/004Z8Ihr0JIu5s.html",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

params = {
    "ct": "24",
    "qqmusic_ver": "1298",
    "remoteplace": "txt.yqq.lyric",
    "searchid": "103347689276433275",
    "aggr": "0",
    "catZhida": "1",
    "lossless": "0",
    "sem": "1",
    "t": "7",
    "p": "1",
    "n": "5",
    "w": "周杰伦",
    "g_tk_new_20200303": "5381",
    "g_tk": "5381",
    "loginUin": "0",
    "hostUin": "0",
    "format": "json",
    "inCharset": "utf8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "yqq.json",
    "needNewCode": "0",
}

cookie = "eas_sid=q1r6d8K9O2C5k1v1i0J70611i5; pgv_pvid=770260094; LW_sid=K1g6N8r9W2c626F9f4d6P9a3b0; LW_uid=P13668j962s696B9h4S6i9q3M3; RK=ACmph4WcZH; ptcz=b8f68a8b1cd02e00f8a41982ec08a8a874f8fe793d6a3c1a65b2d99a8217a130; _qpsvr_localtk=0.4529462453857105; pac_uid=0_aadf2ff8f9da5; iip=0; _qimei_fingerprint=2ad68f6a700ed64e704181180aaade3e; _qimei_q36=; _qimei_h38=594e86616c9822ea581e5d9302000002b17a14; suid=0_aadf2ff8f9da5; fqm_pvqid=c62f5a82-cd13-4b14-ad2d-77b21dacf2c5; fqm_sessionid=2ebdfe0d-2b5e-45ec-a436-0123176c3e96; pgv_info=ssid=s7014208560; ts_refer=www.bing.com/; ts_uid=753482120; login_type=2; euin=oK6kowEAoK4z7eE57ioqNenkNn**; wxuin=1152921504917398058; wxopenid=opCFJw_r_x8NhsLtdL4uW7t-YoT8; psrf_qqaccess_token=; psrf_qqopenid=; wxuin=1152921504917398058; psrf_qqunionid=; wxunionid=oqFLxsnbupI23ZLZqeQOWPpZYHiU; psrf_qqrefresh_token=; tmeLoginType=1; qqmusic_key=W_X_63B0aIg1Ii4f33Hp8Gk0mhUz2TMv4bWm41SeqlygTs6ZAPPVtW5XQS6ot6I-Avew0uDPhoodE2MJHRlqxAWIdgSdn; qm_keyst=W_X_63B0aIg1Ii4f33Hp8Gk0mhUz2TMv4bWm41SeqlygTs6ZAPPVtW5XQS6ot6I-Avew0uDPhoodE2MJHRlqxAWIdgSdn; qm_keyst=W_X_63B0aIg1Ii4f33Hp8Gk0mhUz2TMv4bWm41SeqlygTs6ZAPPVtW5XQS6ot6I-Avew0uDPhoodE2MJHRlqxAWIdgSdn; wxrefresh_token=82_WCVw5wkeR_JHa5XljbCl5kvwWD07NbYcuM7V1IT7MGDRGmAOnNLa5Z3Z9riv5q9Gj7OyPvR5jW_u9ud5RQCfzrtQ91Nf42M0NCs-CbmsTy4; ts_last=y.qq.com/n/ryqq/albumDetail/004Z85XP1c25b7"
def sanitize_filename(filename):
    pattern = re.compile(r'[^\w]')
    sanitized_filename = pattern.sub('_', filename)    
    return sanitized_filename
def main():
    # singer = input("请输入歌手名：")

    '''
    area：歌手的地域(内地、港台、欧美等)。-100:全部、200:内地、2:港台、5:欧美、4:日本、3:韩国、6:其他
    genre：歌手风格(流行、嘻哈等)。-100：全部、1：流行、6：嘻哈、2：摇滚、4：电子、3：民谣、8：R&B、10：民歌、9：轻音乐、5：爵士、14：古典、25：乡村、20：蓝调
    cur_page：当前歌手列表的页码
    index：cur_page*page_size(index表示当前页的起始index，page_size表示每一页歌手的数量)
    cur_page=n，index=80(n-1)
    '''

    url1 = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genre%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A0%2C%22cur_page%22%3A1%7D%7D%7D"
    area = -100
    genre = -100
    count = 0
    singers = []
    for i in range(1, 3): # 设置需要访问的歌手范围——这里只爬取前两页歌手
        cur_page = i
        index = (cur_page - 1) * 80
        singer_list_url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A{}%2C%22sex%22%3A-100%2C%22genre%22%3A{}%2C%22index%22%3A-100%2C%22sin%22%3A{}%2C%22cur_page%22%3A{}%7D%7D%7D"
        formatted_url = singer_list_url.format(area, genre, index, cur_page)
        url_singer = requests.get(formatted_url).json()
        singerlist = url_singer["singerList"]["data"]["singerlist"]
        
        
        for j in singerlist:
            singer_name = j["singer_name"]
            singers.append(singer_name)
            count +=1
        print("count:", count)
        time.sleep(random.uniform(0.5, 1.5))

    # print(singers)
    

    def check(songname, albumname):
        if singer not in songname or "-" not in songname:
            return False

        if albumname in album_dic:
            for song in album_dic[albumname]:
                if songname in song[0]:
                    return False

        if singer == "周杰伦":
            if "范特西PLUS" in albumname:
                return True
            if "周大侠" in songname:
                return True

        song_remove = ["Live", "醇享版", "纯音乐", "暂无歌词"]
        album_remove = ["Live", "演唱会", "音乐会"]
        for sn in song_remove:
            if sn in songname:
                return False
        for an in album_remove:
            if an in albumname:
                return False
        return True


    # 初始化webdriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://y.qq.com/n/ryqq/singer/003Nz2So3XXYek")
    input()
    n = 0
    music_count = 0
    # current_tabs = 0
    # print(singers)
    for singer in singers:
        n+=1
        print(music_count)
        params["w"] = singer
        params["p"] = 1
        time.sleep(1)
        res = requests.get(URL, headers=headers, params=params).json()
        print(singer)

        if "zhida" in res["data"] and "zhida_singer" in res["data"]["zhida"]:
            singer_mid = res["data"]["zhida"]["zhida_singer"]["singerMID"]
            print(singer_mid)
        else:
            print(res)
            continue
        
        singer_mid = res["data"]["zhida"]["zhida_singer"]["singerMID"]
        singer_pic = res["data"]["zhida"]["zhida_singer"]["singerPic"]
        singer_url = "https://y.qq.com/n/ryqq/singer/" + singer_mid
        singer = singer
        singer_dir = os.path.join("output", sanitize_filename(singer))
        os.makedirs(singer_dir, exist_ok=True)
        # 打开歌手的个人网页
        driver.execute_script(f"window.open('{singer_url}');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        singer_desc = soup.find('div', class_="data__desc_txt").text.strip() if soup.find('div', class_="data__desc_txt") else ""
        # 写入歌手信息
        with open(os.path.join(singer_dir, "{}.txt".format(sanitize_filename(singer))), "w",encoding="utf-8") as f_singer:
            f_singer.write("singer's name: {}\n".format(singer))
            f_singer.write("singer's url: {}\n".format(singer_url))
            f_singer.write("singer's Picture:\n")
            f_singer.write("{}\n".format(singer_pic))
            f_singer.write("singer's Description:\n")
            f_singer.write("{}\n".format(singer_desc))
        singer_img_data = requests.get(singer_pic).content
        with open(os.path.join(singer_dir, 'singer_image.jpg'), 'wb') as handler_1:
            handler_1.write(singer_img_data)    

        album_mids = []
        album_dic = defaultdict(list)
        # 创建专辑集，分页获取专辑及歌曲信息
        for p in range(1, 100):
            params["p"] = p
            res = requests.get(URL, headers=headers, params=params).json()
            time.sleep(0.3)
            list_lyric = res["data"]["lyric"]["list"]
            
            if len(list_lyric) == 0:
                counts = sum(len(albums) for albums in album_dic.values())
                print("总共下载{}首歌词！".format(counts))
                music_count += counts
                break
            
            for lyric in list_lyric:
                content = re.sub(r"\\n ", "\n", lyric["content"]).strip()
                song_mid = lyric["songmid"]
                song_url = "https://y.qq.com/n/ryqq/songDetail/" + song_mid
                content += "\n\n" + song_url
                songname = content.split("\n")[0].strip()
                albumname = lyric["albumname"].strip()
                if check(songname, albumname):
                    if len(albumname) == 0:
                        albumname = "其它"
                    album_dic[albumname].append((songname, content))
                    if len(album_dic[albumname]) == 1:
                        album_dic[albumname].append(("album_name", lyric["albummid"]))
            if p == 2:
                counts = sum(len(albums) for albums in album_dic.values())
                print("总共下载{}首歌词！".format(counts))
                music_count += counts
            time.sleep(0.1)
        

        for index, (album_name, songs) in enumerate(album_dic.items()):
            album_dir = os.path.join(singer_dir, sanitize_filename(album_name))
            os.makedirs(album_dir, exist_ok=True)
            img_url = ""
            for song in songs:                
                if song[0] == "album_name":  # 如果是专辑名，则song[1]是albummid，访问网页查询albumpic                    
                    album_url = "https://y.qq.com/n/ryqq/albumDetail/" + song[1]
                    driver.execute_script(f"window.open('{album_url}');")
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(random.uniform(0.8, 2))
                    html_content = driver.page_source
                    soup = BeautifulSoup(html_content, 'html.parser')
                    img_tag = soup.find('img', class_='data__photo')
                    if img_tag:
                        img_url = "https:" + img_tag.get('src')
                        img_data = requests.get(img_url).content
                        with open(os.path.join(album_dir, 'album_image.jpg'), 'wb') as handler:                            
                            handler.write(img_data)
                else:
                    with open(os.path.join(album_dir, "{}.txt".format(sanitize_filename(album_name))), "w", encoding="utf-8") as f_album:
                        f_album.write("  " + song[0] + "\n")
                    song_path = os.path.join(album_dir, "{}.txt".format(sanitize_filename(song[0])))
                    with open(song_path, "w", encoding="utf-8") as f_lyric:
                        f_lyric.write(song[1])

                


    driver.quit()

if __name__ == "__main__":
    main()