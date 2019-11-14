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
test = rcc.head(200)
aux=0
d = {'mto_saldo': ['mean','sum'], 'clasif': ['mean','min','max'], 'rango_mora': ['mean','min','max']} 
for product in products:
    product_name_aux=str(product)
    product_name=product_name_aux.replace(" ", "")
    ## adding new metrics
    totalCount = test.groupby(["id_persona","codmes"])[['producto','mto_saldo','rango_mora','clasif']] \
    .apply(lambda x: x[x['producto']==product]) \
    .reset_index()
    finalCount = totalCount.groupby(["id_persona","codmes"]).agg(d)
    print(finalCount)
    path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation\rcc'
    camp_file = product_name + str('.csv')
    final_path = path+camp_file
    with open(final_path, 'w') as f:
        f.write('\n'.join([','.join(h) for h in zip(*finalCount.columns)]) + '\n')
        finalCount.to_csv(final_path, mode='a', index=True, header=False)
