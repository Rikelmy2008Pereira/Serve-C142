import pandas as pd
import numpy as np

movies_df = pd.read_csv('movies.csv')
credits_df = pd.read_csv('movie_links.csv')

final_df = pd.merge(movies_df,credits_df,on='original_title')
final_df.to_csv('final.csv')