import pandas as pd
import csv

campanias = pd.read_csv("campanias_new_3.csv")

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
ids          = campanias.id_persona.unique()
cols = campanias.columns
aux = 1
print(len(ids))
with open('campanias_final.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(cols)
    for id in ids:
        for mes in meses:
            res = {}
            res["id_persona"] = id        
            lines = campanias.loc[campanias['id_persona'] == id]
            res["codmes"] = mes
            flag = False

            for col in cols:
                if col == "id_persona" or col == "codmes":
                    continue
                res[col] = 0

            for index, row in lines.iterrows():
                month = row["codmes"]
                if ((mes == 201901 and month == 201810) or
                    (mes == 201902 and month == 201811) or
                    (mes == 201903 and month == 201812) or
                    (mes == 201904 and month == 201901) or
                    (mes == 201905 and month == 201902) or
                    (mes == 201906 and month == 201903) or
                    (mes == 201907 and month == 201904)                
                    ):
                    flag = True
                    for col in cols:
                        if col == "id_persona" or col == "codmes":
                            continue
                        res[col] += row[col]
            #print(res)
            if flag:
                csv_writer.writerow(res.values())
        if aux%1000 == 0:
            print("Mil Done" + str(aux))
        aux += 1