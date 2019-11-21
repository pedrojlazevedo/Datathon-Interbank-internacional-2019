import pandas as pd
import numpy as np
import csv
import math
import re
import numpy_indexed as npi
import sys
import os

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
#
# Working with Campanhas table



digital = pd.read_csv("interbank-internacional-2019/data_generation/digital_transform.csv")
## unique keys
ids         = digital.id_persona.unique()
test = digital
aux=0
# Data Analysis - Has any values different then 0
'''
print((test['time_tc']!=0).sum())
print((test['time_ctasld']!=0).sum())
print((test['time_mllp']!=0).sum())
print((test['time_mllst']!=0).sum())
print((test['busqmc']!=0).sum())
print((test['busqamex']!=0).sum())
print(len(test.columns))
'''
def sum_h(series):
    sum = 0
    for index, value in series.items():
        print(str(index))
        print(value)
        sum += value

    return sum

# Dropping columns containing only zeroes
digAnalyzed = test.drop(['time_tc','time_ctasld','time_mllp','time_mllst','busqmc','busqamex'],axis=1) 
'''
# Confirming all columns have atleast 1 relevant result
print(len(digAnalyzed.columns))
for cols in digAnalyzed.columns:
    print((digAnalyzed[cols]!=0).sum())
# Converting codday to codmes and renaming it
digAnalyzed["codday"] = digAnalyzed["codday"].apply(lambda x : int(x/100))
finalDigital = digAnalyzed.rename(columns={"codday":"codmes"})
'''
# Calculating mean min max for every column
totalCount = digAnalyzed.groupby(['id_persona','codmes']).aggregate(['mean','min','max',sum_h])
path = "interbank-internacional-2019\data_generation"
digital_file = str('digital_final.csv')
# Converting multi level header to single level
totalCount.columns = [' '.join(col).strip() for col in totalCount.columns.values]
totalCount.to_csv(os.path.join(path,digital_file),index=True)