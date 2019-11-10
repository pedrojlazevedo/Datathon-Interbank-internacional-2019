import pandas as pd
import numpy as np
import csv
import math
import re
import numpy_indexed as npi

#
# Working with Campanhas table
with open('campaign_treatment.csv', mode='w', newline='') as csv_file:
    csv_f = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    base_camp = pd.read_csv("interbank-internacional-2019/ib_base_campanias/ib_base_campanias.csv")
    #with open("interbank-internacional-2019/ib_base_rcc/ib_base_rcc.csv", parse_dates=["codmes"]) as myfile:
    base_camp['codmes'] =  pd.to_datetime(base_camp['codmes'], format='%Y%m')
    ids         = base_camp.id_persona.unique()
    camp_prod   = base_camp.producto.unique()
    ids = base_camp.id_persona.unique()
    '''
    There are  14.56 % of regists that we want (1)
    2019-01    54088
    2019-02    46125
    2019-03    52387
    2019-04    60065
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

    campaigns = base_camp.producto.unique()
    campaigns = np.insert(campaigns,0,'id_persona')
    campaigns = np.insert(campaigns,1,'codmes')
    campaigns = np.insert(campaigns,1,'canal_asignado')
    csv_f.writerow(campaigns)
    aux=0
    final = base_camp.groupby(["id_persona","codmes","producto"]).first()
    
    print(final)
    print(aux)