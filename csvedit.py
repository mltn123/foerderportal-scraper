import pandas as pd
from pandas import DataFrame, merge
import glob
import subprocess
from pathlib import Path
import os
from glob import glob
y=0
pd.options.mode.chained_assignment = None  # default='warn'
save_path = "Cartesian"
if not os.path.exists('Cartesian'):
    os.mkdir(path)
#directory = os.path.join r'\Output\\Heinsberg'


for path in Path(r'C:\Users\dell\Desktop\foerderportal-scraper-main\Output\\').rglob('*.csv'):
    y=y+1
    print(path)
    df = pd.read_csv(path,  encoding='latin-1', sep=';', header=None, engine="python", usecols=[11])
    df = df.iloc[1:]
    #print (df)
    length = df.shape[0]
    for i in range(length):
        df1 = df[:i]
        #print(df1)
        df2 = df[:i]


        #df3 = df1.append([df1]*df.shape[0],ignore_index=True)
    df1['key'] = 0
    df2['key'] = 0
                #print(df1)
    df3 = merge(df1, df2,on='key')
    df3.to_csv(f'{save_path}\cartesian{y}.csv', sep=";")

subprocess.call('copy *.csv merged.csv', shell=True, cwd="./Cartesian")



#print ("länge" + str(df2.shape[0]))
