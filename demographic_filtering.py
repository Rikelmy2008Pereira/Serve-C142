import pandas as pd
df = pd.read_csv('final.csv')

df = df.sort_values('weighted_rating',ascending=False)

output = df[['original_title','poster_link','release_date','runtime','weighted_rating']].head(20)