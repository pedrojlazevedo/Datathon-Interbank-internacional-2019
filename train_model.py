from lightgbm import LGBMClassifier # Light Gradient Boosting Machine (tree based)

import pandas as pd
import matplotlib.pyplot as plt

X_train = pd.read_csv("train_data_clean.csv").set_index("prediction_id")
X_test  = pd.read_csv("test_data_clean.csv").set_index("prediction_id")
train = pd.read_csv("interbank-internacional-2019/ib_base_inicial_train/ib_base_inicial_train.csv")

y_train = train[['codmes', 'id_persona', 'margen']].copy()
y_train["prediction_id"] = y_train["id_persona"].astype(str) + "_" + y_train["codmes"].astype(str)
y_train["target"] = (y_train["margen"] > 0).astype(int)
y_train = y_train.set_index("prediction_id")

plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.axis([0, 6, 0, 20])
plt.show()

drop_cols = ["codmes"]
fi = []
test_probs = []
train_probs = []

for mes in X_train.codmes.unique():
    print("*"*10, mes, "*"*10)
    Xt = X_train[X_train.codmes != mes]
    yt = y_train.loc[Xt.index, "target"]
    Xt = Xt.drop(drop_cols, axis=1)

    Xv = X_train[X_train.codmes == mes]
    yv = y_train.loc[Xv.index, "target"]
    
    learner = LGBMClassifier(n_estimators=1000)
    learner.fit(Xt, yt,  early_stopping_rounds=100, eval_metric="auc",
                eval_set=[(Xt, yt), (Xv.drop(drop_cols, axis=1), yv)], verbose=50)
    
    test_probs.append(pd.Series(learner.predict_proba(X_test.drop(drop_cols, axis=1))[:, -1],
                                index=X_test.index, name="fold_" + str(mes)))
    train_probs.append(pd.Series(learner.predict_proba(Xv.drop(drop_cols, axis=1))[:, -1],
                                index=Xv.index, name="probs"))
    fi.append(pd.Series(learner.feature_importances_ / learner.feature_importances_.sum(), index=Xt.columns))
    break

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

#
# Saving the data for kaggle
#

test_preds = (test_probs > optimization["x"][0]).astype(int)
test_preds.index.name="prediction_id"
test_preds.name="class"
test_preds.to_csv("results_LGBM.csv", header=True)