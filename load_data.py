import pandas as pd
df  = pd.read_pickle('bse_data_scrapy.pkl')
print(df)
df.to_csv('data.csv')