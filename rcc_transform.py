import pandas as pd
import csv

rcc = pd.read_csv(r"interbank-internacional-2019\data_generation\rcc_new.csv")

meses = {
    201901: slice(201808, 201810),
    201902: slice(201809, 201811),
    201903: slice(201810, 201812),
    201904: slice(201811, 201901),
    201905: slice(201812, 201902),
    201906: slice(201901, 201903),
    201907: slice(201902, 201904)
}

complementos    = []
ids             = rcc.id_persona.unique()
cols            = rcc.columns
aux = 1
print(len(ids))
with open(r'interbank-internacional-2019\data_generation\rcc_final.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(cols)
    calcs = ["max", "min", "avg", "count", "sum"]
    for id in ids:
        for mes in meses:
            res = {}
            res["id_persona"] = id
            res["codmes"] = mes    
            lines = rcc.loc[rcc['id_persona'] == id]            
            flag = False

            #init variables
            for col in cols:
                if col == "id_persona" or col == "codmes":
                    continue
                elif col == "mto_saldo":
                    for calc in calcs:
                        res[col + "_" + calc] = 0
                elif col == "rango_mora":
                    res["rango_mora_atraso"] = 0
                    res["rango_mora_super_atraso"] = 0
                elif col == "cod_banco"
                    res["banco_count"] = 0                
                elif col == "clasif"
                    res["clasif_avg"] = 0

            for index, row in lines.iterrows():
                month = row["codmes"]
                if ((mes == 201901 and (month == 201807 or month == 201808 or month == 201809)) or
                    (mes == 201902 and (month == 201808 or month == 201809 or month == 201810)) or
                    (mes == 201903 and (month == 201809 or month == 201810 or month == 201811)) or
                    (mes == 201904 and (month == 201810 or month == 201811 or month == 201812)) or
                    (mes == 201905 and (month == 201811 or month == 201812 or month == 201901)) or
                    (mes == 201906 and (month == 201812 or month == 201901 or month == 201902)) or
                    (mes == 201907 and (month == 201901 or month == 201902 or month == 201903))                
                    ):
                    flag = True
                    my_list = []
                    for col in cols:
                        if col == "id_persona" or col == "codmes":
                            continue
                        elif col == "mto_saldo":
                            if  res[col + "_" + "max"] < row["mto_saldo"]:
                                res[col + "_" + "max"] = row["mto_saldo"]
                            if  res[col + "_" + "min"] > row["mto_saldo"] or res[col + "_" + "min"] == 0:
                                res[col + "_" + "min"] = row["mto_saldo"]
                            if  res[col + "_" + "count"]
                        elif col == "rango_mora":
                            res["rango_mora_atraso"] = 0
                            res["rango_mora_super_atraso"] = 0
                        elif col == "cod_banco"
                            res["banco_count"] = 0                        
                        elif col == "clasif"
                            res["clasif_avg"] = 0
            #print(res)
            if flag:
                #calcular
                csv_writer.writerow(res.values())
        if aux%1000 == 0:
            print("Mil Done" + str(aux))
        aux += 1