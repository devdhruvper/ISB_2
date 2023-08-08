import requests
import pandas as pd
path='C:\Users\dhruv\OneDrive\Desktop\ML_projects\ML_project_5\ISB\BIPP\New folder\bipp-datasets\projects\transmission-lines\data\raw'
url="https://cea.nic.in/api/transmission_lines.php"
Response=requests.get(url)
DF=pd.read_json(Response.text)
DF.to_csv('Transmission_lines.csv',index=False)