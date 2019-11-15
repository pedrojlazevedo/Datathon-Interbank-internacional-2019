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

print(pd.__version__)

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
aux=0
lastDF = pd.DataFrame()
for product in products:
    product_name_aux=str(product)
    product_name=product_name_aux.replace(" ", "")
    ## adding new metrics
    totalCount = test.groupby(["id_persona","codmes"])[['producto','mto_saldo','rango_mora','clasif']] \
    .apply(lambda x: x[x['producto']==product]) \
    .reset_index()
    finalCount = totalCount.groupby(["id_persona","codmes"]).agg(d)
    finalCount.columns = [' '.join(col).strip() for col in finalCount.columns.values]
    # Renaming dictionary for specific product
    mtosaldoAvgstr=str('mto_saldo')+product_name+str('avg')
    mtosaldoSumstr=str('mto_saldo')+product_name+str('sum')
    clasifAvgstr=str('clasif')+product_name+str('avg')
    clasifMinstr=str('clasif')+product_name+str('min')
    clasifMaxstr=str('clasif')+product_name+str('max')
    rangomoraAvgstr=str('rangomora')+product_name+str('avg')
    rangomoraMinstr=str('rangomora')+product_name+str('min')
    rangomoraMaxstr=str('rangomora')+product_name+str('max')
    renamedDF = finalCount.rename(columns={"mto_saldo mean": mtosaldoAvgstr, "mto_saldo sum": mtosaldoSumstr, \
        "clasif mean":clasifAvgstr, "clasif min":clasifMinstr, "clasif max": clasifMaxstr,        \
        "rango_mora mean":rangomoraAvgstr,"rango_mora min":rangomoraMinstr, "rango_mora max":rangomoraMaxstr})
    # Merging columns 
    if aux==0:
        lastDF = renamedDF
    else:
        lastDF =  pd.merge(lastDF, renamedDF, how='outer', on=['id_persona','codmes'])
    print(lastDF)
    aux+=1
path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation'
rcc_file = str('rcc_new.csv')
lastDF.to_csv(os.path.join(path,rcc_file))