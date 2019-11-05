import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")
print("# Filas: {0}".format(str(train.shape[0])))
print("# Columnas: {0}".format(str(train.shape[1])))

print("Compruebo tipos de datos de las columnas")
train.dtypes
print("compruebo valores nulos")
train.isna().sum()

print("Observamos las proporciones del target")
print(train.groupby("codtarget").size() / len(train))

print("calculamos quienes son rentables y quienes son, margen > 0 es rentable")
train["esRentable"] = np.where(train.margen > 0, 1, 0)
print(train.groupby("esRentable").size() / len(train))

print("vemos quienes son rentables y compraron una TC")
print(train.groupby(["codtarget","esRentable"]).size() / len(train))

variables = ["margen", "cem", "ingreso_neto", "linea_ofrecida"]

for variable in variables:
    print("calculo deciles para variable {0}".format(variable))
    print("----------------------------------")
    dfAux = train.groupby(["codmes", pd.qcut(train[variable], 10, duplicates = "drop"), "codtarget"]).size().reset_index().rename(columns = {0 : "qCasos"})
    crosstab = pd.crosstab(index = [dfAux.codmes, dfAux[variable]], columns = dfAux.codtarget, values = dfAux["qCasos"], aggfunc = "sum").reset_index()
    crosstab["totales"] = crosstab[0]+crosstab[1]
    crosstab["%target0"] = crosstab[0]/crosstab["totales"]
    crosstab["%target1"] = crosstab[1]/crosstab["totales"]
    print(crosstab[crosstab.codmes == 201901])

variables = ["margen", "cem", "ingreso_neto", "linea_ofrecida"]

for variable in variables:
    print("calculo deciles para variable {0}".format(variable))
    print("----------------------------------")
    dfAux = train.groupby(["codmes", pd.qcut(train[variable], 4, duplicates = "drop"), "codtarget"]).size().reset_index().rename(columns = {0 : "qCasos"})
    crosstab = pd.crosstab(index = [dfAux.codmes, dfAux[variable]], columns = dfAux.codtarget, values = dfAux["qCasos"], aggfunc = "sum").reset_index()
    crosstab["totales"] = crosstab[0]+crosstab[1]
    crosstab["%target0"] = crosstab[0]/crosstab["totales"]
    crosstab["%target1"] = crosstab[1]/crosstab["totales"]
    print(crosstab[crosstab.codmes == 201901])

train[train.codtarget == 1].groupby("codmes").agg({"linea_ofrecida": ["min", "max", "mean", "median"], 
                                                   "cem": ["min", "max", "mean", "median"], 
                                                   "ingreso_neto": ["min", "max", "mean", "median"], 
                                                   "margen": ["min", "max", "mean", "median"]})

train[train.codtarget == 0].groupby("codmes").agg({"linea_ofrecida": ["min", "max", "mean", "median"], 
                                                   "cem": ["min", "max", "mean", "median"], 
                                                   "ingreso_neto": ["min", "max", "mean", "median"], 
                                                   "margen": ["min", "max", "mean", "median"]})

train["ratioLineaIngreso"] = train["linea_ofrecida"] / train["ingreso_neto"]
train.groupby(["codmes", "codtarget"]).agg({"ratioLineaIngreso": ["min", "max", "mean", "median"]})

variables = ["ratioLineaIngreso"]

for variable in variables:
    print("calculo deciles para variable {0}".format(variable))
    print("----------------------------------")
    dfAux = train.groupby(["codmes", pd.qcut(train[variable], 10, duplicates = "drop"), "codtarget"]).size().reset_index().rename(columns = {0 : "qCasos"})
    crosstab = pd.crosstab(index = [dfAux.codmes, dfAux[variable]], columns = dfAux.codtarget, values = dfAux["qCasos"], aggfunc = "sum").reset_index()
    crosstab["totales"] = crosstab[0]+crosstab[1]
    crosstab["%target0"] = crosstab[0]/crosstab["totales"]
    crosstab["%target1"] = crosstab[1]/crosstab["totales"]
    print(crosstab[crosstab.codmes == 201901])

print("valido la cantidad de veces que una persona aparece en las bases")
print("----------------------------------------------------------------")
a = train.groupby("id_persona").size().reset_index().rename(columns ={0:"qApariciones"})
b = train.groupby("id_persona").codtarget.max().reset_index()
c = pd.merge(a,b, on ="id_persona", how = "left")
print(c[c.qApariciones > 1].groupby("codtarget").size() / len(c[c.qApariciones > 1]))
print("valido segun las apariciones en la base como se comporta segun la venta de los productos")
print("---------------------------------------------------------------------------------------")

print(c.groupby(["codtarget", "qApariciones"]).size() / len(c))

print("valido los porcentajes de target cuando aparece solo una vez el cliente")
print("-----------------------------------------------------------------------")

print(c[c.qApariciones == 1].groupby("codtarget").size() / len(c[c.qApariciones == 1]))

meses = train.codmes.drop_duplicates().values
for codmes in meses:
    print("cantidad de registros para el mes {0} son {1}".format(codmes, len(train[train.codmes == codmes])))
    a = train[train.codmes < codmes].groupby("id_persona").size().reset_index().rename(columns ={0:"qApariciones"})
    b = train[train.codmes == codmes].groupby("id_persona").codtarget.max().reset_index()
    c = pd.merge(b,a, on ="id_persona", how = "left").fillna(0)
    print("valido el paso anterior pero cada uno de los meses separados")
    print("------------------------------------------------------------")
    print(c.groupby(["codtarget", "qApariciones"]).size() / len(c))

    print("con solo la aparicion del mes en curso")
    print("--------------------------------------")
    print(c[c.qApariciones == 0].groupby(["codtarget"]).size() / len(c[c.qApariciones == 0]))
    print("con una aparicion ademas del mes en curso")
    print("-----------------------------------------")
    print(c[c.qApariciones == 1].groupby(["codtarget"]).size() / len(c[c.qApariciones == 1]))

    print("con al menos una aparicion ademas del mes en curso")
    print("--------------------------------------------------")
    print(c[c.qApariciones == 1].groupby(["codtarget"]).size() / len(c[c.qApariciones == 1]))

print("revisamos para aquellos que hayan tenido una aparicion anteriormente como se comportan en base a los limites otorgados anteriormente y ahora")
print("el campo mayorLimite es 1 entonces se otorga en el mes en curso mayor limite que en otra aparicion")
print("--------------------------------------------------------------------------------------------------")
meses = train.codmes.drop_duplicates().values
#meses = [201904]
for codmes in meses:
    a = train[train.codmes < codmes].groupby("id_persona").size().reset_index().rename(columns ={0:"qApariciones"})    
    b = train[train.codmes == codmes].groupby("id_persona").agg({"codtarget": "max", "linea_ofrecida": "max"}).reset_index().rename(columns = {"linea_ofrecida": "ultimaLinea"})
    c = train[train.codmes < codmes].groupby("id_persona").linea_ofrecida.max().reset_index()
    d = pd.merge(b,a, on ="id_persona", how = "left").fillna(0)
    e = pd.merge(d, c, on = "id_persona", how = "left").fillna(0)
    e = e[e.qApariciones > 0]
    e["mayorLimite"] = np.where(e.ultimaLinea > e.linea_ofrecida, 1, 0)
    print("como se comporta la cartera mes a mes en base al target y si se aumento o no el limite")
    print("--------------------------------------------------------------------------------------")
    print(e.groupby(["mayorLimite", "codtarget"]).size() / len(e))
    print("como se comportan aquellos que la linea ofrecida disminuye")
    print(e[e.mayorLimite == 0].groupby(["mayorLimite", "codtarget"]).size() / len(e[e.mayorLimite == 0]))
    
    print("como se comportan aquellos que la linea ofrecida aumenta")
    print(e[e.mayorLimite == 1].groupby(["mayorLimite", "codtarget"]).size() / len(e[e.mayorLimite == 1]))

##################

digital = pd.read_csv("interbank-internacional-2019/ib_base_digital/ib_base_digital.csv")
digital.head()
digital["codmes"] = digital.apply(lambda x: x.codday // 100, axis = 1)
digital["codmes"] = digital["codmes"].astype(int)
agregatedColumns = ['simu_prestamo', 'benefit', 'email', 'facebook',
       'goog', 'youtb', 'compb', 'movil', 'desktop', 'lima_dig', 'provincia_dig', 'extranjero_dig', 'n_sesion',
       'busqtc', 'busqvisa', 'busqamex', 'busqmc', 'busqcsimp', 'busqmill',
       'busqcsld', 'busq', 'n_pag', 'android', 'iphone']


aggFunctions = dict()
for column in agregatedColumns:
  aggFunctions[column] = "sum"





