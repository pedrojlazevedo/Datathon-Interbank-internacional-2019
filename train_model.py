from lightgbm import LGBMClassifier # Light Gradient Boosting Machine (tree based)
from lightgbm import LGBMRegressor

import pandas as pd
import gc
import csv

X_train = pd.read_csv("interbank-internacional-2019/data_generation/train_data.csv").set_index("prediction_id")

X_test  = pd.read_csv("interbank-internacional-2019/data_generation/test_data.csv").set_index("prediction_id")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")

y_train = train[['codmes', 'id_persona', 'margen', 'codtarget']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
y_train["target"] = (y_train["codtarget"]).astype(int)
y_train = y_train.set_index("prediction_id")


drop_cols = ["codmes"]
fi = []
test_probs = []
train_probs = []

 #LGBMClassifier!!! Probably not the best
aux = 1
for mes in X_train.codmes.unique():
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]

    learner = LGBMClassifier(n_estimators=10000)
    learner.fit(Xt, yt,  early_stopping_rounds=100, eval_metric="auc",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    gc.collect()
    test_probs.append(pd.Series(learner.predict_proba(X_test.drop(drop_cols, axis=1))[:, -1],
                                index=X_test.index, name="fold_" + str(mes)))
    train_probs.append(pd.Series(learner.predict_proba(Xv.drop(drop_cols, axis=1))[:, -1],
                                index=Xv.index, name="probs"))
    fi.append(pd.Series(learner.feature_importances_ / learner.feature_importances_.sum(), index=Xt.columns))
    gc.collect()
    if aux == 9:
        break
    aux += 1

'''
aux = 1
for mes in X_train.codmes.unique():
    if aux < 4:
        aux += 1
        continue
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]
    
    learner = LGBMRegressor(n_estimators=10000)
    learner.fit(Xt, yt,  early_stopping_rounds=100, eval_metric="auc",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    gc.collect()
    test_probs.append(pd.Series(learner.predict(X_test.drop(drop_cols, axis=1)),
                                index=X_test.index, name="fold_" + str(mes)))
    train_probs.append(pd.Series(learner.predict(Xv.drop(drop_cols, axis=1)),
                                index=Xv.index, name="probs"))
    fi.append(pd.Series(learner.feature_importances_ / learner.feature_importances_.sum(), index=Xt.columns))
    gc.collect()

    aux += 1
'''
test_probs = pd.concat(test_probs, axis=1).mean(axis=1)
train_probs = pd.concat(train_probs)
fi = pd.concat(fi, axis=1).mean(axis=1)

print(fi.sort_values().tail(50).to_frame())

#
# Optimizar
#

from scipy.optimize import differential_evolution

res = y_train.join(train_probs.rename("probs"))
optimization = differential_evolution(lambda c: -((res.probs > c[0]) * res.margen / res.margen.sum()).sum(), [(0, 1)])
print(optimization)

print("#########")
print(X_test)
print("#########")
print(test_probs)

test_preds = (test_probs > optimization["x"][0]).astype(int)
test_preds.index.name="prediction_id"
test_preds.name="class"

print("#########")
print(test_preds)

del test_probs, train_probs
#
# Split Information! Train for the margen
#

X_test  = pd.read_csv("interbank-internacional-2019/data_generation/test_data.csv").set_index("prediction_id")

y_train = train[['codmes', 'id_persona', 'margen', 'codtarget']].copy()
y_train = y_train[ y_train['codtarget'] == 1 ]

y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
print("#########TRAIN###########")
print(y_train)
y_train["target"] = (y_train["margen"] > 0).astype(int)
print("#########TARGET###########")
print(y_train)
y_train = y_train.set_index("prediction_id")

test_preds.to_csv("results_LGBM_Regressor.csv", header=True)
test_preds = pd.read_csv("results_LGBM_Regressor.csv")
prev_test = test_preds.copy()
test_entries = test_preds[ test_preds['class'] == 1 ]
test_entries = test_entries.drop(['class'], axis=1)
X_final_test = X_test.reset_index().merge(test_entries, on=["prediction_id"]).set_index("prediction_id")

#
# Train for positive margin
#

X_train = pd.read_csv("interbank-internacional-2019/data_generation/train_data.csv").set_index("prediction_id")

train_temp = train[["codtarget", "codmes"]]
train_temp["prediction_id"] = train_temp["id_persona"].astype(str) + "_" + train_temp["codmes"].astype(str)
print(train_temp)
train_temp.drop(["codmes"], axis = 1)
print(train_temp)
X_train = X_train.join(train, on=["prediction_id"]).set_index("prediction_id")
X_train = X_train[ X_train['codtarget'] == 1 ]
X_train = X_train.drop(['codtarget'], axis=1)

aux = 8
fi = []
test_probs = []
train_probs = []
for mes in X_train.codmes.unique():
    if aux < 4:
        aux += 1
        continue
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]
    
    learner = LGBMRegressor(n_estimators=10000)
    learner.fit(Xt, yt,  early_stopping_rounds=100, eval_metric="mae",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    gc.collect()
    test_probs.append(pd.Series(learner.predict(X_final_test.drop(drop_cols, axis=1)),
                                index=X_final_test.index, name="fold_" + str(mes)))
    train_probs.append(pd.Series(learner.predict(Xv.drop(drop_cols, axis=1)),
                                index=Xv.index, name="probs"))
    fi.append(pd.Series(learner.feature_importances_ / learner.feature_importances_.sum(), index=Xt.columns))
    gc.collect()

    aux += 1
#
# Joining information
#

test_probs = pd.concat(test_probs, axis=1).mean(axis=1)
train_probs = pd.concat(train_probs)
fi = pd.concat(fi, axis=1).mean(axis=1)

print(fi.sort_values().tail(50).to_frame())

#
# Optimizar
#

from scipy.optimize import differential_evolution

res = y_train.join(train_probs.rename("probs"))
optimization = differential_evolution(lambda c: -((res.probs > c[0]) * res.margen / res.margen.sum()).sum(), [(0, 1)])
print(optimization)

print("#########")
print(test_probs)
test_probs.to_csv("results_LGBM_Regressor.csv", header=True)

test_preds = (test_probs > optimization["x"][0]).astype(int)
test_preds.index.name="prediction_id"
test_preds.name="class"
print("#########")
print(test_probs)

print("#########")
print(test_preds)

with open('results_LGBM_all.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["prediction_id","class"])
    print(type(test_preds))
    for index, row in prev_test.iterrows():
        if row['class'] == 0:
            csv_writer.writerow( [ str(row['prediction_id']), str(row['class'])] )
    for i, v in test_preds.iteritems():
        csv_writer.writerow( [str(i), str(v)] )
    