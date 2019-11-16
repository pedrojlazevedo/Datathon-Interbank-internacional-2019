import pandas as pd
import numpy as np
import csv
import math
import re
import numpy_indexed as npi
import sys
import os
# Working with Campanhas table

rcc = pd.read_csv("interbank-internacional-2019\ib_base_rcc\ib_base_rcc_test.csv")
## unique keys
ids         = rcc.id_persona.unique()
products = rcc.producto.unique()
test = rcc
aux=0
lastDF = pd.DataFrame
d = {'mto_saldo': ['mean','sum'], 'clasif': ['mean','min','max'], 'rango_mora': ['mean','min','max']} 
rcc_banco = rcc.groupby(["codmes", "id_persona","cod_banco", "producto"]).agg(d) \
    .unstack(level=3, fill_value=0).reset_index().set_index("codmes").sort_index().astype("int32")
rcc.to_csv(os.path.join(path,digital_file),index=True)



meses = {
    201901: slice(201808, 201810),
    201902: slice(201809, 201811),
    201903: slice(201810, 201812),
    201904: slice(201811, 201901),
    201905: slice(201812, 201902),
    201906: slice(201901, 201903),
    201907: slice(201902, 201904)
}


'''for product in products:
    product_name_aux=str(product)
    product_name=product_name_aux.replace(" ", "")
    ## adding new metrics
    totalCount = test.groupby(["id_persona","codmes"])[['producto','mto_saldo','rango_mora','clasif']] \
    .apply(lambda x: x[x['producto']==product]) \
    .reset_index()
    finalCount = totalCount.groupby(["id_persona","codmes"]).agg(d)
    finalCount.columns = [' '.join(col).strip() for col in finalCount.columns.values]
    # Renaming dictionary for specific product
    # Merging columns 
    if aux==0:
        lastDF = renamedDF
    else:
        lastDF =  pd.merge(lastDF, renamedDF, how='outer', on=['id_persona','codmes'])
    print(lastDF)
    aux+=1
path = str("interbank-internacional-2019\data_generation")
rcc_file = str('rcc_perfil_persona.csv')
lastDF.to_csv(os.path.join(path,rcc_file))'''