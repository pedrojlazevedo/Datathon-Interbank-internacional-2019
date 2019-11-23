import numpy as np
import pandas as pd
from sympy import *
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
train = pd.read_csv("X_train.csv").drop(columns=["prediction_id"])
reniec = pd.read_csv("interbank-internacional-2019/ib_base_reniec/ib_base_reniec.csv")

test_reniec = reniec[reniec['soc_var6'].isnull()]
print(test_reniec)
## Multiple Regression with Many Predictor Variables
## soc_var6 = b0+b1*soc_var1+b2*soc_var2+b3*soc_var3+b4*soc_var4+b5*soc_var5

## linear regressor
'''
soc_var = LinearRegression()

train_clean = train.dropna()
y_train = np.array(train_clean[["soc_var6"]])
X_train = np.array(train_clean.drop(columns=["soc_var6"]))

## polynomial regressor
poly = PolynomialFeatures(2)
X_transform = poly.fit_transform(X_train)
## train regression model
model = soc_var.fit(X_transform, y_train)
## apply predictions train
dep_predicted = model.predict(X_transform)
## get regression metric values
rmse = mean_squared_error(y_train, dep_predicted)
r2 = r2_score(y_train, dep_predicted)
print('Slope:' ,model.coef_)
print('Intercept:', model.intercept_)
print('Root mean squared error: ', rmse)
print('R2 score: ', r2)
print(dep_predicted)
print()
## apply training to test set

train_set = reniec.dropna(how="any")
test_set = reniec[reniec['soc_var6'].isnull()]
print(test_set)
'''
