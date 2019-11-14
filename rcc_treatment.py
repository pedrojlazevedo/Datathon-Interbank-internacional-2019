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



rcc = pd.read_csv(r"C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\ib_base_rcc\ib_base_rcc.csv")
## unique keys
ids         = rcc.id_persona.unique()
products = rcc.producto.unique()
test = rcc
aux=0
print(test)
print(products)
print(len(products))
d = {'mto_saldo': ['mean','sum'], 'clasif': ['mean','min','max'], 'rango_mora': ['mean','min','max']} 
for product in products:
    product_name_aux=str(product)
    product_name=product_name_aux.replace(" ", "")
    ## adding new metrics
    totalCount = test.groupby(["id_persona","codmes"])[['producto','mto_saldo','rango_mora','clasif']] \
    .apply(lambda x: x[x['producto']==product]) \
    .reset_index()
    finalCount = totalCount.groupby(["id_persona","codmes"]).agg(d)
    finalDF = pd.DataFrame(finalCount)
    auxDf = []
    for col in finalDF.columns:
        data = finalDF[col].apply(pd.Series)
        data = auxDf.append(data)
    auxDf = pd.concat(auxDf,axis=1)
    path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation'
    rcc_file = str('rcc') + product_name + str('.csv')
    auxDf.to_csv(os.path.join(path,rcc_file),index=True)