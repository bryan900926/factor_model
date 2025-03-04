import pandas as pd

rf = pd.read_excel(r"C:\TejPro\TejPro\DataExport\20241226113558DataExport.xlsx").drop(columns=['名稱','代號'])
rf = rf.rename(columns={'無風險利率':'RF','年月':'date'})
ff = pd.read_csv(r'C:\Users\bryan\OneDrive\桌面\python\five_factor.csv')
ff['date'] = pd.to_datetime(ff['date'])
rf['date'] = pd.to_datetime(rf['date'],format='%Y/%m')
merge = pd.merge(ff,rf,on=['date']).drop(columns=['Unnamed: 0'])
merge.to_csv('ff.csv')