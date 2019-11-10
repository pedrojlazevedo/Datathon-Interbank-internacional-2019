import pandas as pd
import numpy as np
import csv
import statistics 

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
    columns  = np.insert(columns, 1, 'variation_linea')
    columns  = np.insert(columns, 1, 'variation_saldo')
    columns  = np.insert(columns, 1, 'avg_linea')
    columns  = np.insert(columns, 1, 'avg_saldo')
    columns  = np.insert(columns, 1, 'variance_linea')
    columns  = np.insert(columns, 1, 'variance_saldo')
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
        all_linea   = []
        all_saldo   = []
        for index, row in lines.iterrows():
            saldo = row['mto_saldo']
            if 'LINEA TOTAL' in row['producto']:            
                if high_linea == 0:
                    high_linea = saldo
                    low_linea = saldo
                all_linea.append(saldo)
                if saldo > high_linea:
                    high_linea = saldo
                elif saldo < low_linea:
                    low_linea = saldo
            else:
                if low_saldo == 0:
                    low_saldo = saldo
                    high_saldo = saldo
                all_saldo.append(saldo)
                if saldo > high_saldo:
                    high_saldo = saldo
                elif saldo < low_saldo:
                    low_saldo = saldo   

        new_rcc['low_saldo'] = low_saldo
        new_rcc['high_saldo'] = high_saldo
        new_rcc['low_linea'] = low_linea
        new_rcc['high_linea'] = high_linea        
        if len(all_saldo) > 2 and len(all_linea) > 2:
            new_rcc['variance_saldo'] = statistics.variance(all_saldo)
            new_rcc['variance_linea'] = statistics.variance(all_linea)
            new_rcc['avg_saldo'] = statistics.mean(all_saldo)
            new_rcc['avg_linea'] = statistics.mean(all_linea)
            new_rcc['variation_saldo'] = all_saldo[len(all_saldo)-1] - all_saldo[0]
            new_rcc['variation_linea'] = all_linea[len(all_linea)-1] - all_linea[0]
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