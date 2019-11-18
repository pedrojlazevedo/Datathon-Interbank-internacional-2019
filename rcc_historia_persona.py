import pandas as pd
import numpy as np
import csv
import math
import re
import numpy_indexed as npi
import sys
import os

def rango_weak(series):
    count = 0
    for index, value in series.items():
        if value < 2:
            count += 1
    return count

def rango_medium(series):
    count = 0
    for index, value in series.items():
        if value >= 2 and value < 4:
            count += 1
    return count

def rango_strong(series):
    count = 0
    for index, value in series.items():
        if value > 4:
            count += 1
    return count

# Working with Campanhas table

rcc = pd.read_csv("interbank-internacional-2019\ib_base_rcc\ib_base_rcc.csv")
## unique keys
ids         = rcc.id_persona.unique()
products = rcc.producto.unique()
# Finding number of missing values in column
print("missing values for rango_mora and clasif:")
print((rcc["rango_mora"].isna()).sum())
print((rcc["clasif"].isna()).sum())
# Filling missing values of rcc[clasif] and rcc[rango_mora] to -1
rcc.clasif.fillna(value=-1,inplace=True)
rcc.rango_mora.fillna(value=-1,inplace=True)

# TODO:Trying to create new arrays with count of rango_mora! 
rcc = rcc.sort_values(by=['rango_mora', 'id_persona'], ascending=False)
rcc = rcc.head(100)

# Aggregating by metrics for each [[id_persona,codmes],[bank]] -> for every product
d = {"cod_banco": ['count'],'mto_saldo': ['mean','sum'], 'clasif': ['mean','min','max'], \
    'rango_mora': ['mean','min','max', rango_weak, rango_medium, rango_strong]} 
rcc_banco = rcc.groupby(["codmes", "id_persona", "producto"]).agg(d) \
    .unstack(level=2, fill_value=0).reset_index().set_index("codmes").sort_index().astype("int32")

rcc_banco.columns = [' '.join(col).strip() for col in rcc_banco.columns.values]

path = r'interbank-internacional-2019\data_generation'
rcc_file = str('rcc_historia_persona.csv')
rcc_banco.to_csv(os.path.join(path,rcc_file))