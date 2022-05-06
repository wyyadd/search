# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
from bs4 import BeautifulSoup
import os
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def getall_link():
    '''得到所有古诗文的链接'''
    starturl='https://so.gushiwen.cn/gushi/tangshi.aspx'
    response = requests.get(starturl, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    links=[]
    for i in range(len(soup.select('.typecont a'))):#根据页面标签获取链接
        link=soup.select('.typecont a')[i]['href']
        links.append(link)
    return links
def getdata(links):
    '''根据链接获取古诗文内容'''
    res=[]
    for link in links:
        dic={}
        url='https://so.gushiwen.cn/'+link
        response = requests.get(url, timeout=5)
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        title=soup.select('.main3 .cont h1')[0].text
        author=soup.select('.main3 .cont>.source>a')[0].text
        # chaodai=soup.select('.main3 .cont>.source>a')[1].text
        content=soup.select('.main3 .cont>.contson')[0].text
        content=content.replace(' ','')
        content=content.replace('\n','')
        content=content.replace('\r', '')
        dic['title']=title
        dic['author']=author
        dic['content']=content
        res.append(dic)
    return res
def write2txt(datas,dirname='dictionary'):
    '''写入文件'''
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for data in datas:
        title=data['title']
        filename=title+'.txt'
        with open(dirname+r'/'+filename, 'a', encoding='utf8') as fp:
            fp.write(title)
            fp.write('\n')
            fp.write(data['author'])
            fp.write('\n')
            fp.write(data['content'])
        # break

if __name__ == '__main__':
    links=getall_link()#获取所有古诗文链接
    datas=getdata(links)#获取所有古诗文数据
    write2txt(datas)#写入txt文件

