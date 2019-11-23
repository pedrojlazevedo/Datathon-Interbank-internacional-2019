

variable_ind = dataset
variable_dep = dataset.drop(columns=["label"])
## Removing linear depedent variable
## using midspread 50%
Q1 = variable_ind.quantile(0.25)
Q3 = variable_ind.quantile(0.75)
IQR = Q3 - Q1
print("IQR Score: ")
print(IQR)
## number of outliers found for z > 1.5
variable_ind_clean = variable_ind[~((variable_ind < (Q1 - 1.5 * IQR)) |(variable_ind > (Q3 + 1.5 * IQR))).any(axis=1)]
## number of outliers found for z > 1.5
outliers = len(variable_ind)-len(variable_ind_clean)
print("len before outliers: " + str(len(variable_ind)))
print("outliers: " + str(outliers))
## joining with linear depedent var by removing the outliers
final = variable_ind_clean.join(variable_dep, lsuffix='_caller', rsuffix='_other',how="right") \
    .dropna(subset=["soc_var1","soc_var2","soc_var3","soc_var3","soc_var4","soc_var5"]) \
    .reset_index(drop=True)
train_set = variable_ind_clean.join(variable_dep, lsuffix='_caller', rsuffix='_other',how="right") \
    .dropna(how="any") \
    .reset_index(drop=True)
print("len after outliers removal: " + str(len(final)))
print("number of possible regresion targets: " + str(len(final) - len(train_set)))
