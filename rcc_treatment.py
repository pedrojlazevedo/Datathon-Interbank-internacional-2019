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

with open('rcc_treatment.csv', mode='w', newline='') as csv_file:
    csv_f = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    rcc = pd.read_csv(r"C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\ib_base_rcc\ib_base_rcc.csv")
    ## unique keys
    ids         = rcc.id_persona.unique()
    products = rcc.producto.unique()
    test = rcc
    newDF = pd.DataFrame()
    aux=0
    d = {'mto_saldo': ['mean','sum'], 'clasif': ['mean','min','max'], 'rango_mora': ['mean','min','max']} 
    for product in products:
        product_name_aux=str(product)
        product_name=product_name_aux.replace(" ", "")+str('Count')
        ## adding new metrics
        totalCount = test.groupby(["id_persona","codmes"])[['producto','mto_saldo','rango_mora','clasif']] \
        .apply(lambda x: x[x['producto']==product]) \
        .reset_index()
        finalCount = totalCount.groupby(["id_persona","codmes"]).agg(d)
        print(finalCount)
        if aux==0:
            newDF=totalCount
        else:
            ## merging metrics -> find out to do a full outer join (not losing codmes when relevant)
            newDF = pd.merge(newDF, finalCount, on=['id_persona','codmes'], how='outer')
        aux=aux+1
    path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation'
    camp_file = str('countCampaigns.csv')
    newDF.to_csv(os.path.join(path,camp_file),index=False)
