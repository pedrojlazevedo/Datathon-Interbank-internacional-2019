import pandas as pd

digital = pd.read_csv("interbank-internacional-2019/ib_base_digital/ib_base_digital.csv")

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
ids          = digital.id_persona.unique()
aux = 1
print(len(ids))
for id in ids:
    for mes in meses:
        res = {}
        res["id_persona"] = id        
        lines = digital.loc[digital['id_persona'] == id]
        res["codmes"] = mes
        flag = False
        res["teste_prestamos"] = 0
        res["visited_site"] = 0
        res["movil"] = 0
        res["n_rep30"] = 0
        res["recencia"] = 0
        res["visita_estrangeiro"] = 0
        res["tempo"] = 0
        res["n_sesion"] = 0
        res["busqtc"] = 0 
        res["busqvisa"] = 0
        res["busqamex"] = 0
        res["busqmc"] = 0
        res["busqcsimp"] = 0
        res["busqmill"] = 0
        res["busqcsld"] = 0
        res["n_pag"] = 0
        res["busq"] = 0
        for index, row in lines.iterrows():
            month = int(row["codday"]/100)
            if ((mes == 201901 and (month == 201808 or month == 201809 or month == 201810)) or
                (mes == 201902 and (month == 201809 or month == 201810 or month == 201811)) or
                (mes == 201903 and (month == 201810 or month == 201811 or month == 201812)) or
                (mes == 201904 and (month == 201811 or month == 201812 or month == 201901)) or
                (mes == 201905 and (month == 201812 or month == 201901 or month == 201902)) or
                (mes == 201906 and (month == 201901 or month == 201902 or month == 201903)) or
                (mes == 201907 and (month == 201902 or month == 201903 or month == 201904))                
                ):
                flag = True
                res["teste_prestamos"] += row["simu_prestamo"] + row["benefit"]
                res["visited_site"] += (row["email"] 
                                    + row["facebook"] + row["goog"]
                                    + row["youtb"] + row["compb"])
                res["movil"] += row["movil"] + row["desktop"]
                res["n_rep30"] += row["n_rep30"]
                res["recencia"] += row["recencia"]
                res["visita_estrangeiro"] += row["lima_dig"] + row["provincia_dig"] + row["extranjero_dig"]
                res["tempo"] += row["time_ctasimple"] + row["time_mllp"] + row["time_mllst"] + row["time_ctasld"] + row["time_tc"]
                res["n_sesion"] += row["n_sesion"]
                res["busqtc"] += row["busqtc"]
                res["busqvisa"] += row["busqvisa"]
                res["busqamex"] += row["busqamex"]
                res["busqmc"] += row["busqmc"]
                res["busqcsimp"] += row["busqcsimp"]
                res["busqmill"] += row["busqmill"]
                res["busqcsld"] += row["busqcsld"]
                res["n_pag"] += row["n_pag"]
                res["busq"] += row["busq"]
        if flag:
            df = pd.DataFrame([res])
            complementos.append(df)
    if aux%1000 == 0:
        print("Mil Done" + str(aux))
    aux += 1
print("contatenando complementos")
complementos = pd.concat(complementos).reset_index().set_index(["id_persona", "codmes"]).astype("float32")
print(complementos)

complementos.to_csv(r"digital_new.csv")