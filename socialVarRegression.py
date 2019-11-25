import numpy as np
import pandas as pd
from sympy import *
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
train = pd.read_csv("X_train.csv").drop(columns=["prediction_id"])
#print(list(set(final_test_nondup.id_persona.unique())-set(test_reniec.id_persona.unique())))

## Multiple Regression with Many Predictor Variables
## soc_var6 = b0+b1*soc_var1+b2*soc_var2+b3*soc_var3+b4*soc_var4+b5*soc_var5
## linear regressor
soc_var = LinearRegression()
train_clean = train[train['soc_var6'].notna()].sort_values(by=['codmes']) \
    .drop_duplicates(subset="id_persona", keep='last', inplace=False) \
    .fillna(-1).head(1000)
del train
x, y = np.array(train_clean.drop(columns=["soc_var6","id_persona","codmes"])), np.array(train_clean['soc_var6'])
## polynomial regressor
poly = PolynomialFeatures(2, include_bias=False)
X_transform = poly.fit_transform(x)
## train regression model
model = soc_var.fit(X_transform, y)
## get regression metric values
# Step 4: Get results
r_sq = model.score(X_transform, y)
print('Slope:' ,model.coef_)
print('Intercept:', model.intercept_)
print('R2 score: ', r_sq)

## apply training to test set
reniec = pd.read_csv("interbank-internacional-2019/ib_base_reniec/ib_base_reniec.csv")
test_reniec = reniec[reniec['soc_var6'].isnull()] \
        .drop(columns=["soc_var1","soc_var2","soc_var3","soc_var4","soc_var5","soc_var6"])
del reniec
train = pd.read_csv("X_train.csv").drop(columns=["prediction_id"])
test = pd.read_csv("X_test.csv").drop(columns=["prediction_id"])
## merging the null soc_var6 with the training set
test_and_train = pd.concat([test, train], sort=False).drop(columns=["soc_var6"])
del test,train
final_test = pd.merge(test_reniec, test_and_train, on=['id_persona'], how='left')
final_test_nondup = final_test.drop_duplicates(subset="id_persona", keep='last', inplace=False) \
    .fillna(-1).reset_index(drop=True)
personas = final_test_nondup["id_persona"]

i=1
finalDF = pd.DataFrame()
for i  in range(12):
    j=i*1000
    i+=1
    if i<11000:
        nrows = final_test_nondup.iloc[j:j+1000]
    else:
        nrows = final_test_nondup.iloc[j:j+742]
    x_test = np.array(nrows.drop(columns=["id_persona","codmes"]))
    test_transform = poly.fit_transform(x_test)
    dep_predicted = model.predict(test_transform)
    df = pd.Series(dep_predicted)
    finalDF = pd.concat([finalDF, df], sort=False)
rcc_file = str('social_var_regression.csv')
lastDF.to_csv(os.path.join(path,rcc_file))