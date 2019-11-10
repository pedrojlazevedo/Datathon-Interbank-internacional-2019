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
'''
meses = {
    201901: slice(201808, 201810),
    201902: slice(201809, 201811),
    201903: slice(201810, 201812),
    201904: slice(201811, 201901),
    201905: slice(201812, 201902),
    201906: slice(201901, 201903),
    201907: slice(201902, 201904)
}
complementos = []
for mes in meses.keys():
    print("*"*10, mes, "*"*10)
    res = pd.concat([
        camp_canal.loc[meses[mes]].groupby("id_persona").sum(),
        camp_prod.loc[meses[mes]].groupby("id_persona").sum()
        
    ], axis=1)
    res["codmes"] = mes
    res = res.reset_index().set_index(["id_persona", "codmes"]).astype("float32")
    complementos.append(res)
'''
with open('campaign_treatment.csv', mode='w', newline='') as csv_file:
    csv_f = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    base_camp = pd.read_csv("interbank-internacional-2019/ib_base_campanias/ib_base_campanias.csv")
    ## unique keys
    ids         = base_camp.id_persona.unique()
    campaigns = base_camp.producto.unique()
    ## headers
    ''' campaigns = np.insert(campaigns,0,'id_persona')
    campaigns = np.insert(campaigns,1,'codmes')
    campaigns = np.insert(campaigns,1,'canal_asignado')
    csv_f.writerow(campaigns)'''
    ## counts 1 393 833 1391833
    ##1 658 876‬
    test = base_camp
    newDF = pd.DataFrame()
    aux=0
    for campaign in campaigns:
        countOfCampaign=0
        campaign_name_aux=str(campaign)
        campaign_name=campaign_name_aux.replace(" ", "")+str('Count')
        ## adding new metrics
        totalCount = test.groupby(["id_persona","codmes"])['producto'] \
        .apply(lambda c: c[c == campaign].count()).groupby(level=[0]).cumsum() \
        .reset_index(name=campaign_name)
        if aux==0:
            newDF=totalCount
        else:
            ## merging metrics -> find out to do a full outer join (not losing codmes when relevant)
            newDF = pd.merge(newDF, totalCount, on=['id_persona','codmes'], how='outer')
        aux=aux+1
    path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation'
    camp_file = str('countCampaigns.csv')
    newDF.to_csv(os.path.join(path,camp_file),index=False)
