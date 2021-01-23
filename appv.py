# appv.py - VAERS database report tool
# to install:
# pip3 install numpy
# pip3 install matplotlib
# pip3 install requests
# to run:
# python3 ./appv.py

import requests
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from datetime import datetime
from io import StringIO

year='2021'

fnamedata='./'+year+'VAERSDATA.csv'
fnamevax='./'+year+'VAERSVAX.csv'

dtd = (int, 'S12', 'S10', float, float, float, 'S4', 'S10', 'S48', 'S4', 'S12', 'S4', 'S4', 'S4', float, 'S10', 'S4', 'S4',  'S12',  'S12', float, 'S48', 'S4', 'S10', 'S48', 'S48', 'S48', 'S48', 'S48', int,  'S12', 'S10', 'S4', 'S4', 'S48')

dtv = (int, 'S12', 'S24', 'S24', 'S10', 'S10', 'S10', 'S24')

todate = lambda x: datetime.strptime(x.decode("utf-8"), '%m/%d/%Y')

convertersd = { "RECVDAT":todate,
                "DATEDIED":todate,
                "VAX_DATE":todate}

# open the two files
fd = open(fnamedata, "r")
fv = open(fnamevax, "r")

# read in the data into tbld and tblv
line=fd.readline()
tbldcolnames=line.split(',')
tbldcolnames[0]="VAERS_ID"
tbld=genfromtxt(fd, delimiter=',',names=tbldcolnames, dtype=dtd, converters=convertersd, usecols=np.arange(0,len(tbldcolnames)))
fd.close()
line=fv.readline()
tblvcolnames=line.split(',')
tblv=genfromtxt(fv, delimiter=',', names=tblvcolnames, dtype=dtv, usecols=np.arange(0,len(tblvcolnames)))
fv.close()

print(tbldcolnames)
print(tblvcolnames)

temprow=tbld[1]
tempc=np.array(temprow.tolist())[0:]
#print(temprow)
#print(tbld[1]["VAX_DATE"])


############ reports ################
reports_list=[]
for dat_iter in tbld:
    for vax_iter in tblv:
        if (dat_iter["VAERS_ID"] == vax_iter["VAERS_ID"]):
            reports_list.append(vax_iter["VAX_MANU"])

# count unique manufacturers
count=0
unique_list=[]
for item in reports_list: 
    if item not in unique_list: 
        count+=1
        unique_list.append(item) 

# sum them up
print("Reports counts in "+year)
for mnfr_iter in unique_list:
    count=0
    for reports_iter in reports_list:
        if (reports_iter==mnfr_iter):
            count+=1
    print(f"{mnfr_iter}: {count}")

############ deaths ################
death_list=[] # used to store the vax entry for each death
death_main_list=[] # used to store the death entry for each death
for dat_iter in tbld:
    if ("Y" in dat_iter["DIED"].decode(encoding='utf-8')):
        for vax_iter in tblv:
            if (dat_iter["VAERS_ID"] == vax_iter["VAERS_ID"]):
                #death_list.append(vax_iter["VAX_MANU"])
                death_list.append(vax_iter)
                death_main_list.append(dat_iter)

# count unique manufacturers
count=0
unique_list=[]
for item in death_list: 
    if item["VAX_MANU"] not in unique_list: 
        count+=1
        unique_list.append(item["VAX_MANU"]) 

# sum them up
print("Death counts in "+year)
for mnfr_iter in unique_list:
    count=0
    for death_iter in death_list:
        if (death_iter["VAX_MANU"]==mnfr_iter):
            count+=1
    print(f"{mnfr_iter}: {count}")
    i=0
    for death_iter in death_list:
        if (death_iter["VAX_MANU"]==mnfr_iter):
            print("   "+str(death_main_list[i]["SYMPTOM_TEXT"]))
        i+=1

