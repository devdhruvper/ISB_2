#improting necessary python libraries
from pathlib import Path
import pandas as pd
import os
import glob

#setting the path 

path=Path.cwd()
print(path)
Path_1 = Path.joinpath(path,"projects","women-mnrega","data","raw",'Women_Mnrega')
Path_2 = Path.joinpath(path,"projects","women-mnrega","data","raw",'merged.csv')

#Getting the sub folder names

dirs=[]
for path in os.scandir(Path_1):
  if path.is_dir():
    dirs.append(path.name)

#Appending the data frames using a for loop to iterate through subfolders and in them files 
data_frames=[]
for dir in dirs:
  dir_path=Path.joinpath(Path_1,f"{dir}")
  for root, dirs, filenames in os.walk(dir_path):
    for file in filenames:
      file_path=Path.joinpath(dir_path,f"{file}")
      df=pd.read_csv(file_path)
      data_frames.append(df)

#converting our appended dataframes to a single dataframe and finally a csv
result = pd.concat(data_frames)   
result.to_csv(Path_2, index=False)
print("Done")
