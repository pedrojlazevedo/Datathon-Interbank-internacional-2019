import pandas as pd
import numpy as np
digital = pd.read_csv("interbank-internacional-2019/data_generation/digital_new.csv")

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
    if n>=201811 and n<201901:
        return 201902
    elif n>=201812 and n<201902:
        return 201903
    elif n>=201901 and n<201903:
        return 201904
    elif n>=201902 and n<201904:
        return 201905
    elif n>201903 and n<=201904:
        return 201906
    else:
        return 201907

print(digital["codmes"].min())
print(digital["codmes"].max())
complementos = []
test = digital
# Apply transformation
test['codmes'] = test['codmes'].apply(lambda x: mapMonth(x))


print(test)

'''for mes in mesesDigital:
    res = {}
    res["codmes"] = mes
    flag = False
    for index, row in digital.iterrows():
        month = row["codmes"]
        if ((mes == 201901 and (month == 201808 or month == 201809 or month == 201810)) or
            (mes == 201902 and (month == 201809 or month == 201810 or month == 201811)) or
            (mes == 201903 and (month == 201810 or month == 201811 or month == 201812)) or
            (mes == 201904 and (month == 201811 or month == 201812 or month == 201901)) or
            (mes == 201905 and (month == 201812 or month == 201901 or month == 201902)) or
            (mes == 201906 and (month == 201901 or month == 201902 or month == 201903)) or
            (mes == 201907 and (month == 201902 or month == 201903 or month == 201904))                
            ):
            flag = True
            print(res["codmes"])
    if flag:
        df = pd.DataFrame([res])
        print(df)
        complementos.append(df)
if aux%1000 == 0:
    print("Mil Done" + str(aux))
aux += 1
print("contatenando complementos")
print(complementos)
complementos = pd.concat(complementos).reset_index().set_index(["id_persona", "codmes"]).astype("float32")
print(complementos)

complementos.to_csv(r"digital_new.csv")
'''