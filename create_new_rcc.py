import pandas as pd
import numpy as np
import csv

#
# Working with RCC table
# Search IDS and save to only one entry
#
with open('rcc_new.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # ['codmes', 'id_persona', 'cod_banco', 'producto', 'clasif', 'mto_saldo', 'rango_mora']
    rcc = pd.read_csv("interbank-internacional-2019/ib_base_rcc/ib_base_rcc.csv", parse_dates=["codmes"])
    rcc['codmes'] =  pd.to_datetime(rcc['codmes'], format='%Y%m')

    ids         = rcc.id_persona.unique()
    productos   = rcc.producto.unique()
    columns = productos.copy()

    columns  = np.insert(columns, 0, 'id_persona')
    columns  = np.insert(columns, 1, 'high_linea')
    columns  = np.insert(columns, 1, 'low_linea')
    columns  = np.insert(columns, 1, 'high_saldo')
    columns  = np.insert(columns, 1, 'low_saldo')

    csv_writer.writerow(columns)

    aux = 0
    print(len(ids))
    for id in ids:
        lines = rcc.loc[rcc['id_persona'] == id]
        new_rcc = {}
        new_rcc['id_persona'] = id

        lines.sort_values(by=['codmes'])
        low_saldo   = 0
        high_saldo  = 0
        low_linea   = 0
        high_linea  = 0
        for index, row in lines.iterrows():
            saldo = row['mto_saldo']
            if 'LINEA TOTAL' in row['producto']:            
                if high_linea == 0:
                    high_linea = saldo
                    low_linea = saldo

                if saldo > high_linea:
                    high_linea = saldo
                elif saldo < low_linea:
                    low_linea = saldo
            else:
                if low_saldo == 0:
                    low_saldo = saldo
                    high_saldo = saldo

                if saldo > high_saldo:
                    high_saldo = saldo
                elif saldo < low_saldo:
                    low_saldo = saldo   

        new_rcc['low_saldo'] = low_saldo
        new_rcc['high_saldo'] = high_saldo
        new_rcc['low_linea'] = low_linea
        new_rcc['high_linea'] = high_linea        

        count_productos = lines.producto.value_counts()
        name_productos = count_productos.keys()

        for producto in productos:
            if producto in name_productos:
                new_rcc[producto] = count_productos[producto]
            else:
                new_rcc[producto] = 0

        csv_writer.writerow(new_rcc.values())
        
        if aux%1000 == 0:
            print("Mais mil! Num:" + str(aux))
        aux += 1