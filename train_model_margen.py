from lightgbm import LGBMClassifier # Light Gradient Boosting Machine (tree based)
from lightgbm import LGBMRegressor

import pandas as pd
import gc

X_train = pd.read_csv("train_data_clean.csv").set_index("prediction_id")
X_train = X_train.drop(['codtarget'], axis=1)

X_test  = pd.read_csv("test_data_clean.csv").set_index("prediction_id")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")

y_train = train[['codmes', 'id_persona', 'margen']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
#y_train["target"] = (y_train["margen"] > 0).astype(int)
y_train = y_train.set_index("prediction_id")

del train
gc.collect()

drop_cols = ["codmes"]
test_preds = []
train_preds = []
y_train["target"] = y_train["margen"].astype("float32")
for mes in X_train.codmes.unique():
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]
    
    learner = LGBMRegressor(n_estimators=1000)
    learner.fit(Xt, yt,  early_stopping_rounds=10, eval_metric="mae",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    gc.collect()
    test_preds.append(pd.Series(learner.predict(X_test.drop(drop_cols, axis=1)),
                                index=X_test.index, name="fold_" + str(mes)))
    train_preds.append(pd.Series(learner.predict(Xv.drop(drop_cols, axis=1)),
                                index=Xv.index, name="probs"))
    gc.collect()

test_preds = pd.concat(test_preds, axis=1).mean(axis=1)
train_preds = pd.concat(train_preds)

drop_cols = ["codmes"]
fi = []
test_probs = []
train_probs = []
y_train["target"] = (y_train["margen"] > 0).astype("int32")
for mes in X_train.codmes.unique():
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]
    
    learner = LGBMClassifier(n_estimators=1000)
    learner.fit(Xt, yt,  early_stopping_rounds=10, eval_metric="auc",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    gc.collect()
    test_probs.append(pd.Series(learner.predict_proba(X_test.drop(drop_cols, axis=1))[:, -1],
                                index=X_test.index, name="fold_" + str(mes)))
    train_probs.append(pd.Series(learner.predict_proba(Xv.drop(drop_cols, axis=1))[:, -1],
                                index=Xv.index, name="probs"))
    gc.collect()

test_probs = pd.concat(test_probs, axis=1).mean(axis=1)
train_probs = pd.concat(train_probs)

test = pd.concat([test_probs.rename("probs"), test_preds.rename("preds")], axis=1)
train = pd.concat([train_probs.rename("probs"), train_preds.rename("preds")], axis=1)

from scipy.optimize import differential_evolution

def clasificar(res, c):
    return ((res.probs > c[0]) | (res.preds > c[1])) * c[2] + ((res.probs > c[3]) & (res.preds > c[4])) * c[5] > c[6]

def cost(res, coefs):
    return -((clasificar(res, coefs) * res.margen) / res.margen.sum()).sum()

res = y_train.join(train)
optimization = differential_evolution(lambda x: cost(res, x), [(-100, 100), (0, 1), (0, 1),
                                                               (-100, 100), (0, 1), (0, 1),
                                                               (0, 2)])
print(optimization)


test_preds = clasificar(test, optimization["x"]).astype(int)
test_preds.index.name="prediction_id"
test_preds.name="class"
test_preds.to_csv("benchmark3.csv", header=True)