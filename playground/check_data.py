import pandas as pd

df = pd.read_csv(r'd:\document\files\python大作业\南京2023年5月到2026年2月天气情况.csv', encoding='gb18030')
print('列名:', df.columns.tolist())
print('前5行:')
print(df.head(5).to_string())
print('总行数:', len(df))
print('气温列样例:')
print(df.iloc[:, 2].head(10).tolist())
