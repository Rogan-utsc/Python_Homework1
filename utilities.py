from importlib.resources import path
from itertools import count
import requests
import re
from lxml import etree
import urllib.request
from pdfminer.high_level import extract_text ##此函数能够将pdf中文本转化为字符串的形式
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.filedialog as tkfd
import tkinter.ttk
import os

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
    def __init__(self, index, author, title):
        self.index = index
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
            return False   


save_path = "D:\Python_Homework1"
article_path='D:\Python_Homework1/sample.pdf'

def download_bib_for_article(article_path , save_path):
    pdf = open(article_path, mode="rb")
    text = extract_text( pdf )
    Ref = Ref_List(Cut_Ref(text))

class App():

    def __init__(self, root):
        self.article_path = ""
        self.save_path = ""
        self.display_width = 60

        frame = tk.Frame(root)
        root.title("References Analysis")
        root.resizable(False, False)
        window_height = 600
        window_width = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.canvas1 = tk.Canvas(root, width = window_width, height = window_height)
        self.canvas1.pack()

        self.label1 = tk.Label(root, text='Weclcme to use this app !')
        self.canvas1.create_window(220, 20, window=self.label1)
        self.label2 = tk.Label(root,text = 'Please choose an article first')
        self.canvas1.create_window(240, 520, window=self.label2)

        self.listbox1 = tk.Listbox(root, width=self.display_width, height=25)
        self.canvas1.create_window(240, 270, window=self.listbox1)

        self.button1 = tk.Button(text='Choose', command=lambda: App._choose(self))
        self.canvas1.create_window(500, 100, window=self.button1)
        self.button2 = tk.Button(text="Display", command=lambda: App._display(self))
        self.canvas1.create_window(500, 150, window=self.button2)
        self.button3 = tk.Button(text="Download", command=lambda: App._download(self))
        self.canvas1.create_window(500, 200, window=self.button3)
        self.button4 = tk.Button(text="Combine", command=lambda: App._combine(self))
        self.canvas1.create_window(500, 250, window=self.button4)
        self.button5 = tk.Button(text="Delete", command=lambda: App._delete(self))
        self.canvas1.create_window(500, 300, window=self.button5)


    def _choose(self):
        self.listbox1.delete(0, tk.END)
        self.label2.config(text = "")
        filename = tkfd.askopenfilename()
        pdf = open(filename, mode="rb")
        self.label2.config(text = "Analyzing the References...  Please wait...  ")
        root.update()
        text = extract_text(pdf)
        Ref = Ref_List(Cut_Ref(text))
        self.Ref = Ref
        self.label2.config(text = "Now you can display all the References or Download them")

    def _display(self):
        L = len(self.Ref)
        self.label2.config(text = "This article has %d references!"%L)
        for i in range(L):
            self._print(self.Ref[i])
    
    def _print(self,text):
        L = len(text)
        num_row = L//self.display_width + 1
        for i in range(num_row):
            self.listbox1.insert(tk.END, text[i*self.display_width: (i+1)*self.display_width+1])
        self.listbox1.insert(tk.END,'\n')

    def _download(self):
        self.listbox1.delete(0, tk.END)
        self.label1.config(text="Downloading...  Please wait for a while... ")
        root.update()
        self.label2.config(text = " ")
        self.save_path = tkfd.askdirectory()
        self.fail_list = []
        L = len(self.Ref)
        self.listbox1.insert(tk.END, "The following reference failed to be downloaded:\n\n\n")
        for i in range(L): 
            one_ref = split(self.Ref[i])
            self.label2.config(text= "Process: "+str(i+1)+" / "+str(L))
            root.update()
            one_instace = References(one_ref[0],one_ref[1],one_ref[2])
            if(one_instace.downloadBib(self.save_path) == False):
                self.fail_list.append(i)
                list_item = str(i+1) + ":" + one_instace.title
                self._print(list_item)
                root.update()
        if(self.fail_list): 
            self.label2.config(text="The rate of failure is %f"%( len(self.fail_list)/L ) )
            root.update()
        else :
            self.label2.config(text="All references have been sucessfully downloaded!")
        
        self.label1.config(text="Downloading is now finished!")
        self.label2.config(text="You can choose to combine all the bib together !\nOr you can delete the bib downloaded just before")
        root.upate()

    def _combine(self):
        self.label1.config(text="Combining...  Please wait for a while... ")
        root.update()
        self.label2.config(text = " ")
        save_path = tkfd.askdirectory()
        bib_text = ""
        for i in range(len(self.Ref)):
            if i not in self.fail_list:
                file_name = self.save_path+ "/"+ str(i+1) + ".bib"
                with open(file_name, "r" ) as f:
                    bib_text = bib_text + f.read() + "\n"
        fw = open(save_path+"/combined.bib", "w")
        fw.write(bib_text)
        self.label1.config(text="Combinination finished")
        root.update()

    
    def _delete(self):
        self.label1.config(text="Deleting...  Please wait for a while... ")
        root.update()
        bib_text = ""
        for i in range(len(self.Ref)):
            if i not in self.fail_list:
                path = self.save_path+ "/"+ str(i+1) + ".bib"
                os.remove(path)
        self.label1.config(text = "Deleting finished")
        self.label2.config(text="You can choose another article or you can click 'X' to quit")
        root.update()