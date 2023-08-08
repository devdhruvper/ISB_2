import requests
import pandas as pd
from pathlib import Path
import pandas as pd

def Date_convert(month :str):
 date_string = "jun-23"
 date = pd.to_datetime(date_string, format="%b-%y")
 formatted_date = date.strftime("%d-%m-%Y")
 return formatted_date


path=Path.cwd()
raw_path = Path.joinpath(path,"data","raw",'transmission_lines.csv')
url="https://cea.nic.in/api/transmission_lines.php"
Response=requests.get(url)


DF=pd.read_json(Response.text)
DF['month'] = DF['month'].apply(Date_convert)
DF.rename(columns = {'month':'date'}, inplace = True)
DF.to_csv(raw_path,index=False)
