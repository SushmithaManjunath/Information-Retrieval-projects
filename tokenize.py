from sys import argv
import os
import sys
import codecs
from bs4 import BeautifulSoup
from collections import Counter
import glob
import codecs
import re
import time
import matplotlib.pyplot as plt

sorted_tokens={}
sorted_values={}
'''to store frequency of tokens'''

data =[]
data_len=[]
#path =str(sys.argv[1]+'/*.html')
path = str(argv[1]+'/*.html')

files=glob.glob(path)#to acess the path of inputfile
for file in files:
    f = codecs.open(file,"r",encoding='utf-8',errors='ignore')
    soupout = BeautifulSoup(f.read().lower(),'html.parser')
    data.append(soupout.get_text())

for x in data:
    data_len.append(len(x))

out =[y for x,y in sorted(list(zip(data_len,data)))]    

data_len.sort()


timer1=[]
timer2=[]
data1=[]
#print data[0]
for doc in out:
    start_1=time.time()
    data1.append(list(filter(None, doc.split(" "))))#split based on spaces
    end_1=time.time()
    timer1.append(end_1-start_1)
 
all_token=[]    
data2=[]
for f,x in enumerate(data1):
    zz =[]
    start_2=time.time()
    for y in x:
        zz.extend(list(filter(None,re.findall('[a-zA-Z]+|[.,!?;]+|\\d+',y))))
    end_2=time.time()
    timer2.append(end_2-start_2)
    
    data2.append(zz)
    all_token.extend(zz)
    with open(argv[2]+str(f)+".data","w") as f :
        f.writelines(zz)  
    
token_dict= Counter(all_token)   


kl = list(token_dict.keys())
kl.sort()

for key, value in sorted(token_dict.items(), key=lambda v: v[1]):
    sorted_values[key] = value

for ky in kl:
    sorted_tokens[ky]=token_dict[ky]
timer=[]
for i in range(0,len(list(zip(timer1,timer2)))):
    timer.append(timer1[i]+timer2[i])

    
with open(argv[2]+'/sorted_by_token.data',"w") as f :
        f.writelines(sorted_tokens) 
with open(argv[2]+'/sorted_by_value.data',"w") as f :
        f.writelines(sorted_values) 
    
    
plt.scatter(data_len,timer)
plt.title('Tokenization Process Time VS Size of Text ')
plt.xlabel('Length of Text')
plt.ylabel('Time for Process')
plt.savefig(argv[2]+'graph_time.png')
plt.show()