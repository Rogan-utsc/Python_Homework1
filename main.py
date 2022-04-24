from utilities import *

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


root = tk.Tk()
ap = App(root)
root.mainloop()


