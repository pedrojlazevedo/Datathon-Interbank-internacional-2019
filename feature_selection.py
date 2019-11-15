import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso

X_train = pd.read_csv("train_data_clean.csv").set_index("prediction_id")
X_test  = pd.read_csv("test_data_clean.csv").set_index("prediction_id")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")

y_train = train[['codmes', 'id_persona', 'margen']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
y_train["target"] = (y_train["margen"] > 0).astype(int)
y_train = y_train.set_index("prediction_id")


# Filter Method
# Pearson correlation is the most used
# — A value closer to 0 implies weaker correlation (exact 0 implying no correlation)
# — A value closer to 1 implies stronger positive correlation
# — A value closer to -1 implies stronger negative correlation

df = pd.DataFrame(X_train.data, columns = X_train.feature_names)
df["target"] = X_train.target
X = df.drop("target",1)   #Feature Matrix
y = df["target"]          #Target Variable
print(df.head())

#Using Pearson Correlation
plt.figure(figsize=(12,10))
cor = df.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()