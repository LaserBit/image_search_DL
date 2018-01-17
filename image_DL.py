# -*- coding: utf_8 -*-

import os.path
import sys
import requests
from time import sleep
from urllib.parse import quote
from bs4 import BeautifulSoup

save_dir = './data'
image_pages = 1


def main():
    word = sys.argv[1]
    print(word)
    if os.path.isdir(save_dir):
        print("Dir Exists")
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    fetch_and_save_img(word)


# 画像をダウンロードする
# def download_image(url, timeout = 10):

#     return response.content


# 画像のファイル名を決める
def make_filename(base_dir, number, url):
    ext = os.path.splitext(url)[1] # 拡張子を取得
    filename = str(number) + ext        # 番号に拡張子をつけてファイル名にする

    fullpath = os.path.join(base_dir, filename)
    return fullpath


# 画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)


def fetch_and_save_img(word, timeout = 10):
    for i in range(image_pages):
        sleep(0.5)
        for j, img_url in enumerate(img_url_list(word, i * 20 + 1)):
            sleep(0.1)

            response = requests.get(img_url, timeout=timeout)
            if response.status_code != 200:
                e = Exception("HTTP status: " + response.status_code)
                raise e
            content_type = response.headers["content-type"]
            if 'image' not in content_type:
                e = Exception("Content-Type: " + content_type)
                raise e
            redirect_url = response.url

            filename = make_filename(save_dir, i * 20 + j, redirect_url)
            try:
                image = response.content
                save_image(filename, image)
            except KeyboardInterrupt:
                break
            except Exception as err:
                print(err)


def img_url_list(word, num):
    """
    using yahoo (this script can't use at google)
    """
    url = 'http://search.yahoo.co.jp/image/search?p={}&ei=UTF-8&b={}'.format(quote(word), num)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    img_link_elems = soup.find_all('a', attrs={'target': 'imagewin'})
    img_urls = [e.get('href') for e in img_link_elems if e.get('href').startswith('http')]


    img_urls = list(set(img_urls))
    return img_urls


if __name__ == '__main__':
    main()
