import pandas as pd

rolling_value=10
df_original = pd.read_csv('ratedump.csv', header=0,index_col=0)
num_original = len(df_original.index)
abc = df_original.groupby(df_original.index // 900).max()
abc.to_csv('MaxCsv.csv', sep=',')

abc = df_original.groupby(df_original.index // 900).mean()
abc.to_csv('AvgCsv.csv', sep=',')

##df_rolling_max = df_original.rolling(rolling_value).max()
##df_rolling_max_clipped = df_rolling_max
####df_rolling_max_clipped=df_rolling_max.iloc[rolling_value-1:,:]
##df_rolling_max_clipped.reset_index(inplace=True, drop=True)
##num_original_max = len(df_rolling_max_clipped)
##df_rolling_max_clipped.to_csv('RollingMaxCSV.csv')
##
##
##df_original_clippped=df_original
####df_original_clippped = df_original.iloc[:num_original-rolling_value+1,:]
##df_original_clippped.reset_index(inplace=True, drop=True)
##df_original_clippped.to_csv('OriginalClippedcsv.csv')
##
##
##
##df_subtracted=df_rolling_max_clipped.subtract(df_original_clippped, axis = 1)
##
##df_subtracted= df_rolling_max_clipped - df_original_clippped
####print(len(df_rolling_max.index))
##print(df_rolling_max_clipped.index)
##print(df_original_clippped.index)
##print(df_subtracted.index)
##df_subtracted.to_csv('subtractedcsv.csv')
                 


