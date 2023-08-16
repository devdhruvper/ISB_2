from pathlib import Path
import pandas as pd
import os
import glob

path=Path.cwd()
print(path)
Path_1 = Path.joinpath(path,"projects","transmission-lines","data","raw",'Women_Mnrega')
Path_2 = Path.joinpath(path,"projects","transmission-lines","data","raw",'merged.csv')
print(r'C:\Users\dhruv\OneDrive\Desktop\ML_projects\ML_project_5\ISB\BIPP\New folder\bipp-datasets\projects\transmission-lines\data\raw\Women_Mnrega')


dirs=[]
for path in os.scandir(Path_1):
  if path.is_dir():
    dirs.append(path.name)


data_frames=[]
for dir in dirs:
  dir_path=Path.joinpath(Path_1,f"{dir}")
  for root, dirs, filenames in os.walk(dir_path):
    for file in filenames:
      file_path=Path.joinpath(dir_path,f"{file}")
      df=pd.read_csv(file_path)
      data_frames.append(df)


result = pd.concat(data_frames)   
result.to_csv(Path_2, index=False)
print("Done")
# all_filenames = []
# for root, dirs, filenames in os.walk(Path_1):
#    for dir in dirs:
#      print (dir)
    # for file in filenames:
    #  all_filenames.append(os.path.join(root, file))

# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
# combined_csv.to_csv(raw_path,"merged.csv", index=False, encoding='utf-8-sig')
# print(raw_path)