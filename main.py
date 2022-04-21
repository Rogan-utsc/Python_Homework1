from itertools import count
import requests
import time
import re
from lxml import etree
import urllib.request
from pdfminer.high_level import extract_text ##此函数能够将pdf中文本转化为字符串的形式

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
        

#print(repr(text1))

def Ref_List(txt):##该函数将截取的Ref按每一条拆开，将文本中多余的字符去除，并有序存入一个list中
    keylab1 = "["
    L = txt.count(keylab1)
    RefList = [0 for i in range(L)]
    idx_index_list = txt.find('[')
    #txt = txt.replace("\n","")
    ref_list_disordered = txt.split(keylab1)
    del(ref_list_disordered[0])

    last_ref = ref_list_disordered[L - 1]
    idx_del = last_ref.rfind(".")
    ref_list_disordered[L - 1] = last_ref[:idx_del]

    for i in range(L):
        ref_list_disordered[i] = "[" + ref_list_disordered[i]
        ref_list_disordered[i] = ref_list_disordered[i][:-2]
        ref_list_disordered[i] = re.sub("-\n","",ref_list_disordered[i])
        ref_list_disordered[i] = re.sub("\n\n","",ref_list_disordered[i])
        ref_list_disordered[i] = re.sub("\n"," ",ref_list_disordered[i])

    for i in range(L):
        oneref = ref_list_disordered[i]
        for idx in range(len(oneref)):
            if(oneref[idx] == "]"):
                num = int(oneref[1 : idx])
                RefList[num-1] = oneref
    return(RefList)



def split(self):
    idx1, idx2 = 0, 0
    keylab0 = ']'
    keylab1 = '“'
    keylab2 = ","
    keylab3 = "."
    L = len(self)
    while self[idx2] != keylab0:
        if idx2 > L:
            return False
        idx2 = idx2 + 1

    index = self[idx1 + 1 : idx2 ]
    idx1 = idx2 + 1

    if self.find(keylab1) < 0:
        idx2 = self.find(keylab3)
        author = self[idx1 : idx2]
        idx1 = idx2+1
        self = self[idx1:]
        idx1 = 0
        idx2 = self.find(keylab3)
        title = self[idx1: idx2]
        return index, author, title

    while self[idx2] != keylab1:
        if idx2 > L:
            return False
        idx2 = idx2 + 1
    author = self[idx1 + 4 : idx2 - 2]

    idx1 = idx2 + 1
    while self[idx2] != keylab2:
        if idx2 > L - 2:
            return False
        idx2 = idx2 + 1
    title = self[idx1 : idx2]
    return index, author, title


class References(object):
    def __init__(self, index, author, title) :
        self.index =index 
        self.author = author
        self.title = title

    def downloadBib(self, path):
        txt = self.title
        txt = re.sub(" ","%20",txt)
        txt = re.sub(":","%3A",txt)
        url = "https://dblp.org/search?q=" + txt
        res = requests.get(url)
        dom = etree.HTML(res.text)
        content = dom.xpath("/html/body/div[2]/div[9]/div/ul/li[2]/nav/ul/li[2]/div[1]/a/@href")

        if content:
            download_url = content[0].replace("html?view=bibtex", "bib?param=1")
            file_path = path + "\\" + self.index + ".bib"
            urllib.request.urlretrieve(download_url, file_path )
            return True
        else:
            #print("The %s reference cannot be found in DBLP !"%self.index)
            print(dom)
            return False

save_path="D:\Python_Homework1"
article_path='D:\Python_Homework1/sample.pdf'

def download_bib_for_article(article_path , save_path):
    pdf = open(article_path, mode="rb")
    text = extract_text( pdf )
    Ref = Ref_List(Cut_Ref(text))
    L = len(Ref)
    print("This article has %d references!"%L)
    fail_list = []
    for i in range(L): 
        one_ref = split(Ref[i])
        one_instace = References(one_ref[0],one_ref[1],one_ref[2])
        if(one_instace.downloadBib(save_path) == False):
            fail_list.append(i+1)
            print(one_instace.title)
    if(fail_list): 
        print("The following reference failed to be downloaded!")
        print( "The rate of failure is %f"%( len(fail_list)/L ) )
        print(fail_list)

    else :
        print("All references have been sucessfully downloaded!")

download_bib_for_article(article_path , save_path)