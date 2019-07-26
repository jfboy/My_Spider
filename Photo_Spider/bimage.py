from _md5 import md5  #可以在后面保存图片的时候起到去重的作用
from gevent import os
from requests import RequestException
import re
import requests
import photo_wall

def get_page(keyword): #获取网页
    url ='https://image.baidu.com/search/index?tn=baiduimage&word='+ keyword
    try:
        re = requests.get(url)
        if re.status_code == 200:
            html = re.text
            return html
        return None
    except RequestException:
        print("获取网页出错！")
        return None

def parse_page(html,new_path ): #分析网页
    pattern = re.compile('"objURL":"(.*?)"')  #data-objurl="(.*?)"
    result = re.findall(pattern,html)
    for url in result:
        download_images(url,new_path )

def download_images(url,new_path ): #下载图片
    print("正在下载", url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_images(response.content,new_path ) #保存图片
            print("下载成功！")
        return None
    except RequestException:
        print("下载图片出错",url)
        return None

def save_images(content,new_path ): #保存图片
    file_path = '{0}/{1}.{2}'.format(new_path, md5(content).hexdigest(), 'jpg')  # 获得当前项目路径并保存,md5判断，可去重
    if not os.path.exists(file_path):  # 若文件不存在，则存储下来
        with open(file_path, 'wb') as f:  # 写入二进制
            f.write(content)
            f.close()

def new_dir(path_name):
    new_path = os.getcwd() + os.path.sep + path_name  # 新建的文件夹的路径
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    else:
        print("文件夹已存在！")
    return new_path

def main(keyword):
    new_path = new_dir(keyword)
    html = get_page(keyword)
    parse_page(html, new_path)
    photo_wall.main(keyword)

if __name__ == "__main__":
    with open('keyword.txt', 'rt') as f:
        keyword = f.readline()
        f.close()
    if keyword:
        print('关键字:', keyword)
        main(keyword)
    else:print('关键字不能为空')

