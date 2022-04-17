from itertools import count
from pdfminer.high_level import extract_text
text = extract_text('D:\Python_Homework1/sample3.pdf')
#print(repr(text))
def Cut_Ref(text):
    keylab = "References\n\n"
    for idx in range(len(text)): 
        if text[idx : idx + len(keylab)] == keylab:
            return text[idx:]
            break
        elif idx >= len(text) - len(keylab) : 
            print("No Refrences in this article !\n")
            break 
        
#text2="In the second Pick&Sweep\ntask, the robot is required to pick a sweeping tool (e.g.\ndustpan sweeper, table cloth, or sponge, etc.) up and\nsweep an object into the dustpan. The task is successful\nif the target object is swept into the dustpan within 50\n\n\x0cReferences\n\n[1] F. Ebert, C. Finn, S. Dasari, A. Xie, A. Lee, and\nS. Levine, “Visual foresight: Model-based deep reinforcement\nlearning for vision-based robotic control,” "
text1 = Cut_Ref(text)
#text2 = text1[0:400]
#print(repr(text1))
#print(repr(text1))
#Ref_List

def Ref_List(txt):
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
            OneRef = txt[idx : idx2-2].replace("\n","  ")
            RefList[num-1] = OneRef
            
    return(RefList)

print(Ref_List(text1))
            

#print(repr(text2))




