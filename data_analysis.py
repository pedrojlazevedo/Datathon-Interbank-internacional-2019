import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

X_test = pd.read_csv("interbank-internacional-2019/ib_base_inicial_test/ib_base_inicial_test.csv", parse_dates=["codmes"])
campanias = pd.read_csv("interbank-internacional-2019/ib_base_campanias/ib_base_campanias.csv", parse_dates=["codmes"])
digital = pd.read_csv("interbank-internacional-2019/ib_base_digital/ib_base_digital.csv", parse_dates=["codday"])
rcc = pd.read_csv("interbank-internacional-2019/ib_base_rcc/ib_base_rcc.csv", parse_dates=["codmes"])
reniec = pd.read_csv("interbank-internacional-2019/ib_base_reniec/ib_base_reniec.csv")
sunat = pd.read_csv("interbank-internacional-2019/ib_base_sunat/ib_base_sunat.csv")
vehicular = pd.read_csv("interbank-internacional-2019/ib_base_vehicular/ib_base_vehicular.csv")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv" , parse_dates=["codmes"])

#
# Number of data
#

print('Forma del csv campanias', campanias.shape)
print('Forma del csv digital', digital.shape)
print('Forma del csv rcc', rcc.shape)
print('Forma del csv reniec', reniec.shape)
print('Forma del csv sunat', sunat.shape)
print('Forma del csv vehicular', vehicular.shape)

print("")
print(rcc.producto.value_counts())

#
# Null Inputs in RCC data
#

total = rcc.isnull().sum().sort_values(ascending = False)
percent = (rcc.isnull().sum()/rcc.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("")
print(missing_application_train_data.head(6))

#
# Comparision Train and Test
#

print(train.shape, X_test.shape) # train has target and test not

#
# Null check
#

total = train.isnull().sum().sort_values(ascending = False)
percent = (train.isnull().sum()/train.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("# Train:\n")
print(missing_application_train_data.head(20))

total = X_test.isnull().sum().sort_values(ascending = False)
percent = (X_test.isnull().sum()/X_test.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("# Test:\n")
print(missing_application_train_data.head(20))

total = campanias.isnull().sum().sort_values(ascending = False)
percent = (campanias.isnull().sum()/campanias.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("# Campanias:\n")
print(missing_application_train_data.head(20))

total = digital.isnull().sum().sort_values(ascending = False)
percent = (digital.isnull().sum()/digital.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("# Digital:\n")
print(missing_application_train_data.head(6))

total = reniec.isnull().sum().sort_values(ascending = False)
percent = (reniec.isnull().sum()/reniec.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("# Reniec:\n")
print(missing_application_train_data.head(3))

total = sunat.isnull().sum().sort_values(ascending = False)
percent = (sunat.isnull().sum()/sunat.isnull().count()*100).sort_values(ascending = False)
missing_application_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
print("\n#####")
print("Sunat:\n")
print(missing_application_train_data.head(6))

train['codmes'] = pd.to_datetime(train['codmes'], format='%Y%m')
train['codmes'] = pd.to_datetime(train['codmes'] ).dt.to_period('M')

print("")
print(train.head())

sns.countplot(train['codtarget'], palette='Set3')
print("")
print("There are ", round(100*train["codtarget"].value_counts()[1]/train.shape[0],2), "% of regists that we want (1)")
print(train.codmes.value_counts())

X_test['codmes'] =  pd.to_datetime(X_test['codmes'], format='%Y%m')
X_test['codmes'] = pd.to_datetime(X_test['codmes']).dt.to_period('M')
print("")
print("Test")
print(X_test.codmes.value_counts())

campanias['codmes'] =  pd.to_datetime(campanias['codmes'], format='%Y%m')
campanias['codmes'] = pd.to_datetime(campanias['codmes']).dt.to_period('M')
print("")
print("CAMPANIAS")
print(campanias.codmes.value_counts())

digital['codday'] =  pd.to_datetime(digital['codday'], format='%Y%m%d')
digital['codday'] = pd.to_datetime(digital['codday']).dt.to_period('M')
print("")
print("DIGITAL")
print(digital.codday.value_counts())

rcc['codmes'] =  pd.to_datetime(rcc['codmes'], format='%Y%m')
rcc['codmes']= pd.to_datetime(rcc['codmes']).dt.to_period('M')
print("")
print("RCC")
print(rcc.codmes.value_counts())

#
# Explore RCC
#

# ['codmes', 'id_persona', 'cod_banco', 'producto', 'clasif', 'mto_saldo', 'rango_mora']
print(rcc.columns.tolist())
print(rcc.loc[rcc['id_persona'] == 1])
print(rcc.loc[rcc['id_persona'] == 2])
print(rcc.loc[rcc['id_persona'] == 3])
print(rcc.loc[rcc['id_persona'] == 4])
print(rcc.loc[rcc['id_persona'] == 5])

print(rcc.producto.unique())
print(rcc.clasif.unique())
print(rcc.mto_saldo.unique())
print(rcc.rango_mora.unique())

