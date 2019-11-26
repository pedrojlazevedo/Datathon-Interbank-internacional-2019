import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import SVC
from mlens.ensemble import SuperLearner
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from itertools import combinations

lr = LogisticRegression()

# Create classifiers
seed = 1075
rf = RandomForestClassifier()
et = ExtraTreesClassifier()
knn = KNeighborsClassifier()
svc = SVC()
rg = RidgeClassifier()

clf_array = [rf, et, knn, svc, rg]  
names = ['Random Forest', 'Extra Trees', 'KNeighbors', 'SVC', 'Ridge Classifier']

X_train = pd.read_csv("interbank-internacional-2019/data_generation/train_data.csv").set_index("prediction_id")

X_test  = pd.read_csv("interbank-internacional-2019/data_generation/test_data.csv").set_index("prediction_id")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")

y_train = train[['codmes', 'id_persona', 'margen', 'codtarget']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
y_train["target"] = (y_train["codtarget"]).astype(int)
y_train = y_train.set_index("prediction_id")

drop_cols = ["codmes"]

def zip_stacked_classifiers(*args):
    to_zip = []
    for arg in args:
        combined_items = sum([list(map(list, combinations(arg, i))) for i in range(len(arg) + 1)], [])
        combined_items = filter(lambda x: len(x) > 0, combined_items)
        to_zip.append(combined_items)
    
    return zip(to_zip[0], to_zip[1])
    
stacked_clf_list = zip_stacked_classifiers(clf_array, names)
best_combination = [0.00, ""]

X_train = X_train.fillna(-1)
X_test = X_test.fillna(-1)
y_train = y_train.fillna(-1)

for mes in X_train.codmes.unique():
    Xt = X_train[X_train.codmes != mes]
    Xt = Xt.drop(drop_cols, axis=1)
    yt = y_train.loc[Xt.index, "target"]

    Xv = X_train[X_train.codmes == mes]
    Xv = Xv.drop(drop_cols, axis=1)
    yv = y_train.loc[Xv.index, "target"]
'''
print(Xt)
print(Xv)
print(yt)
print(yv)

Xt.fillna(-1)
Xv.fillna(-1)
yt.fillna(-1)
yv.fillna(-1)

print(Xt)
'''
for clf in stacked_clf_list:
    ensemble = SuperLearner(scorer = accuracy_score, 
                            random_state = seed, 
                            folds = 10)
    ensemble.add(clf[0])
    ensemble.add_meta(lr)
    ensemble.fit(Xt, yt)
    preds = ensemble.predict(Xv)
    accuracy = accuracy_score(preds, yv)
    
    if accuracy > best_combination[0]:
        best_combination[0] = accuracy
        best_combination[1] = clf[1]
    
    print(f"Accuracy score: {accuracy} {clf[1]}")
    print(f"\nBest stacking model is {best_combination[1} with accuracy of: {best_combination[0]}")# Output

#Accuracy score: 0.674 ['Random Forest']
#Accuracy score: 0.663 ['Extra Trees']
#Accuracy score: 0.547 ['KNeighbors']
#Accuracy score: 0.481 ['SVC']
#...Best stacking model is ['Extra Trees', 'KNeighbors', 'SVC'] with accuracy of: 0.691