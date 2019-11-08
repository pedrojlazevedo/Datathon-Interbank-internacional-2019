import pandas as pd
import matplotlib.pyplot as plt

################
# DATA READING #
################

train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")
X_test = pd.read_csv("interbank-internacional-2019/ib_base_inicial_test/ib_base_inicial_test.csv")

sunat = pd.read_csv("interbank-internacional-2019/ib_base_sunat/ib_base_sunat.csv")
reniec = pd.read_csv("interbank-internacional-2019/ib_base_reniec/ib_base_reniec.csv")
vehicular = pd.read_csv("interbank-internacional-2019/ib_base_vehicular/ib_base_vehicular.csv")
campanias = pd.read_csv("interbank-internacional-2019/ib_base_campanias/ib_base_campanias.csv")
digital = pd.read_csv("interbank-internacional-2019/ib_base_digital/ib_base_digital.csv")
rcc = pd.read_csv("rcc_new_3.csv")

#
# Target Binary
#

y_train = train[['codmes', 'id_persona', 'margen']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
y_train["target"] = (y_train["margen"] > 0).astype(int)
y_train = y_train.set_index("prediction_id")
X_train = train.drop(["codtarget", "margen"], axis=1)
X_train["prediction_id"] = X_train["id_persona"].astype(str) + "_" + X_train["codmes"].astype(str)
del train

#
# id_persona
#

rcc = rcc.set_index("id_persona").astype("int32")
sunat = sunat.groupby(["id_persona", "activ_econo"]).meses_alta.sum().unstack(level=1, fill_value=0).astype("int32")
vehicular1 = vehicular.groupby(["id_persona", "marca"]).veh_var1.sum().unstack(level=1, fill_value=0).astype("float32")
vehicular2 = vehicular.groupby(["id_persona", "marca"]).veh_var2.sum().unstack(level=1, fill_value=0).astype("float32")
reniec = reniec.set_index("id_persona").astype("float32")
del vehicular

vehicular1.columns = [c + "_v1" for c in vehicular1.columns]
vehicular2.columns = [c + "_v2" for c in vehicular2.columns]

X_train = X_train.set_index("prediction_id").astype("int32").reset_index().set_index("id_persona").join(vehicular1).join(vehicular2).join(reniec).join(sunat).join(rcc)
X_test = X_test.set_index("prediction_id").astype("int32").reset_index().set_index("id_persona").join(vehicular1).join(vehicular2).join(reniec).join(sunat).join(rcc)
del vehicular1, vehicular2, reniec, sunat

camp_canal = campanias.groupby(["codmes", "id_persona", "canal_asignado"]).size().unstack(level=2, fill_value=0).reset_index().set_index("codmes").sort_index().astype("int32")
camp_prod = campanias.groupby(["codmes", "id_persona", "producto"]).size().unstack(level=2, fill_value=0).reset_index().set_index("codmes").sort_index().astype("int32")
del campanias


#
# Digital
#

meses = {
    201901: slice(201808, 201810),
    201902: slice(201809, 201811),
    201903: slice(201810, 201812),
    201904: slice(201811, 201901),
    201905: slice(201812, 201902),
    201906: slice(201901, 201903),
    201907: slice(201902, 201904)
}

import gc

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
        for index, row in lines.iterrows():
            month = int(row["codday"]/100)
            if ((mes == 201901 and (month == 201809 or month == 201809 or month == 201810)) or
                (mes == 201902 and (month == 201809 or month == 201810 or month == 201811)) or
                (mes == 201903 and (month == 201810 or month == 201811 or month == 201812)) or
                (mes == 201904 and (month == 201811 or month == 201812 or month == 201901)) or
                (mes == 201905 and (month == 201812 or month == 201901 or month == 201902)) or
                (mes == 201906 and (month == 201901 or month == 201902 or month == 201903)) or
                (mes == 201907 and (month == 201902 or month == 201903 or month == 201904))                
                ):
                flag = True
                res["visited_site"] = (row["simu_prestamo"] + row["benefit"] + row["email"] 
                                    + row["facebook"] + row["goog"]
                                    + row["youtb"] + row["compb"])
                res["movil"] = row["movil"] + row["desktop"]
                res["n_rep30"] = row["n_rep30"]
                res["recencia"] = row["recencia"]
                res["visita_estrangeiro"] = row["lima_dig"] + row["provincia_dig"] + row["extranjero_dig"]
                res["tempo"] = row["time_ctasimple"] + row["time_mllp"] + row["time_mllst"] + row["time_ctasld"] + row["time_tc"]
                res["n_sesion"] = row["n_sesion"]
                res["busqtc"] = row["busqtc"]
                res["busqvisa"] = row["busqvisa"]
                res["busqamex"] = row["busqamex"]
                res["busqmc"] = row["busqmc"]
                res["busqcsimp"] = row["busqcsimp"]
                res["busqmill"] = row["busqmill"]
                res["busqcsld"] = row["busqcsld"]
                res["n_pag"] = row["n_pag"]
                res["busq"] = row["busq"]
        if flag:
            df = pd.DataFrame([res])
            complementos.append(df)
    if aux%1000 == 0:
        print("Mil Done" + str(aux))
    aux += 1
print("contatenando complementos")
complementos = pd.concat(complementos).reset_index().set_index(["id_persona", "codmes"]).astype("float32")
print(complementos)
gc.collect()

X_train = X_train.reset_index().join(complementos, on=["id_persona", "codmes"]).set_index("prediction_id")
X_test  = X_test.reset_index().join(complementos, on=["id_persona", "codmes"]).set_index("prediction_id")

del digital, complementos,res
#
# Campanias
#

gc.collect()

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

gc.collect()
print("contatenando complementos")
complementos = pd.concat(complementos)
print(complementos)
gc.collect()
print("X_train join")
X_train = X_train.reset_index().join(complementos, on=["id_persona", "codmes"]).set_index("prediction_id")
gc.collect()
print("X_test join")
X_test = X_test.reset_index().join(complementos, on=["id_persona", "codmes"]).set_index("prediction_id")
gc.collect()

del camp_canal, camp_prod, complementos,res
gc.collect()

#
# Removing Non ASCII characters
#

non_ascii = X_train.columns[[not all(ord(c) < 128 for c in s) for s in X_train.columns]].tolist()
non_ascii

for i, c in enumerate(non_ascii):
    X_train["non_ascii_" + str(i)] = X_train[c]
    X_train = X_train.drop(c, axis= 1)
    X_test["non_ascii_" + str(i)] = X_test[c]
    X_test = X_test.drop(c, axis= 1)

X_train.to_csv(r'train_data_clean.csv')
X_test.to_csv(r'test_data_clean.csv')