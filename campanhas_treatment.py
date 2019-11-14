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
with open('campaign_treatment.csv', mode='w', newline='') as csv_file:
    csv_f = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    base_camp = pd.read_csv("interbank-internacional-2019/ib_base_campanias/ib_base_campanias.csv")
    ## unique keys
    ids         = base_camp.id_persona.unique()
    campaigns = base_camp.producto.unique()
    ## headers
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
