from itertools import count
from os import link
from selenium import webdriver
import time
import re
from pdfminer.high_level import extract_text ##此函数能够将pdf中文本转化为字符串的形式
pdf = open('D:\Python_Homework1/sample.pdf', mode="rb")
text = extract_text( pdf )
#print(repr(text))

def Cut_Ref(text):##从pdf转化而成的txt中将Reference部分截取出来
##由于不同类型的文章的References的格式不同，这里函数仅仅适用于CVPR类型的文章
    keylab = "References\n\n"
    for idx in range(len(text)): 
        if text[idx : idx + len(keylab)] == keylab:
            return text[idx:]
            break
        elif idx >= len(text) - len(keylab) : 
            print("No Refrences in this article !\n")
            break 
        
text1 = Cut_Ref(text)
#print(repr(text1))

def Ref_List(txt):##该函数将截取的Ref按每一条拆开，将文本中多余的字符去除，并有序存入一个list中
    keylab1 = "["
    keylab2 = "\n\n"
    RefList = [0 for i in range(txt.count(keylab1))]
    for idx in range(len(txt)):
        if txt[idx] == keylab1:
            idx2 = idx
            idx3 = idx2
            while txt[idx3] != "]":
                idx3 = idx3 + 1
            num = int(txt[idx2+1 : idx3])
            print(num)
            while txt[idx2 : idx2 + len(keylab2)] != keylab2:
                idx2 = idx2 + 1
            OneRef = txt[idx : idx2-2].replace("\n","  ").replace("-","")
            RefList[num-1] = OneRef
            
    return(RefList)

print()


class References(object):
    idx1, idx2 = 0, 0
    keylab1 = "\""
    keylab2 = ","
    def __init__(self) :

        while self[idx2] != keylab1:
            idx2 = idx2 + 1
        self.author = self[idx1 : idx2 - 1]
        idx1 = idx2 + 1
        while self[idx2] != keylab2:
            idx2 = idx2 + 1
        self.title = self[idx1 : idx2]
        idx1 = idx2 + 2
        if self[idx1 : idx1+2] == "in":
            idx1 = idx1 + 3
        while self[idx2] != keylab2:
            idx2 = idx2 + 1
        self.publication = self[idx1 : idx2]
    
    def __search_bib__ (self):
        downloadBib("title:" + self.title)
        

def paperUrl(txt):
    txt = re.sub(" ","%20",txt)
    txt = re.sub(":","%3A",txt)
    url = "https://dblp.org/search?q=" + txt
    return url

def downloadBib(url):
    driver = webdriver.Edge("C:\Program Files (x86)/Microsoft/Edge/Application/msedgedriver")
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[2]/div[9]/div/ul/li[2]/nav/ul/li[2]/div[1]/a").click()
    time.sleep(0.5)
    link = driver.find_element_by_xpath("/html/body/div[2]/p/a").get_attribute('href')
    driver.get(link)
    time.sleep(3)
    driver.quit()


Ref = Ref_List(text1)
count = 0
for item in Ref:
    count = count + 1
    if count>3:
        break 
    References(item)




        
            
