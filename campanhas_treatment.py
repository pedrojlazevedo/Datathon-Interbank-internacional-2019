import pandas as pd
import numpy as np
import csv
import math
import re
import numpy_indexed as npi
import sys
import os

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
    ## counts
    test = base_camp.head(10000)
    for campaign in campaigns:
        campaign_name=str(campaign)
        finalCountByMonth = test.groupby(["id_persona","codmes"])['producto'].apply(lambda c: c[c == campaign_name].count())
        ## adding new metrics
        #totalCount = test.groupby(["id_persona"])['producto'].apply(lambda c: c[c == campaign_name].max())
        #avgTotalCount = test.groupby(["id_persona"])['producto'].apply(lambda c: c[c == campaign_name].mean()) todo:mean,max,min,std_dev
        ## merging metrics -> find out to do a full outer join (not losing codmes when relevant)
        #result = pd.merge(finalCountByMonth, totalCount, on='id_persona', how='outer')
        path = r'C:\Users\USER\Desktop\datathon-pedro\Datathon\interbank-internacional-2019\data_generation'
        camp_file = campaign_name +str('.csv')
        finalCountByMonth.reset_index().to_csv(os.path.join(path,camp_file))
