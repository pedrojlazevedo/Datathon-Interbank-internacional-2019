import pandas as pd
import numpy as np
import os
digital = pd.read_csv("interbank-internacional-2019/ib_base_digital/ib_base_digital.csv")

mesesDigital = {
    201901: slice(201811, 201901),
    201902: slice(201812, 201902),
    201903: slice(201901, 201903),
    201904: slice(201902, 201904),
    201905: slice(201903, 201904),
    201906: slice(201903, 201904),
    201907: slice(201904, 201904)
}

# Return month mapped to final 
def mapMonth(n): 
    meses = []
    if n == 201811 or n == 201812:
        meses.append(201901)
    if n == 201811 or n == 201812 or n == 201901:
        meses.append(201902)
    if n == 201811 or n == 201901 or n == 201902:
        meses.append(201903)
    if n == 201901 or n == 201902 or n == 201903:
        meses.append(201904)
    if n == 201902 or n == 201903 or n == 201904:
        meses.append(201905)
    if n == 201903 or n == 201904:
        meses.append(201906)
    if n == 201904:
        meses.append(201907)
    return meses

test = digital.head(2).copy()
# Apply transformation

test["codday"] = test["codday"].apply(lambda x : int(x/100))
test = test.rename(columns={"codday":"codmes"})
df_to_save = test.head(0).copy()
for index, row in test.iterrows():
    meses = mapMonth(row["codmes"])
    for mes in meses:
        row["codmes"] = mes
        df_to_save = df_to_save.append(row, ignore_index=True)

df_to_save = df_to_save.set_index(['codmes'])
df_to_save.index = df_to_save.index.map(int)
df_to_save = df_to_save.reset_index().set_index(['id_persona'])
df_to_save.index = df_to_save.index.map(int)
df_to_save.to_csv("interbank-internacional-2019/data_generation/digital_transform.csv",index=True)