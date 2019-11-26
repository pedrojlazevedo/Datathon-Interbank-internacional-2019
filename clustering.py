from sklearn.cluster import OPTICS
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

vehicular = pd.read_csv("interbank-internacional-2019/ib_base_vehicular/ib_base_vehicular.csv")
#print(len(vehicular.marca.unique()))
#print((vehicular[["marca"]].isna()).sum())
print("length vehicular: " + str(len(vehicular)))
print("unique cars: " + str(len(vehicular.marca.unique())))
vehicular["marca"] = vehicular[["marca"]].fillna("NA")
vehicular["veh_var1"] = vehicular[["veh_var1"]].fillna(-1)
vehicular["veh_var2"] = vehicular[["veh_var2"]].fillna(-1)
encoder = LabelEncoder()
vehicular["marca"] = encoder.fit_transform(vehicular['marca'].astype(str))
# eps - predefined min threshold distance
# delta/min_sample - minimum number of other instances
optics = OPTICS(min_samples=8)
X = np.array(vehicular)
optics.fit(X)
vehicular["marca"] = pd.Series(optics.labels_)
labels = optics.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print("number of clusters: " + str(n_clusters_))
outliers = (vehicular["marca"]==-1).sum()
print("outliers: " + str(outliers))
print((vehicular["marca"]==0).sum())
'''
print(len(dbscan.core_sample_indices_))
print(dbscan.core_sample_indices_)
print(dbscan.components_)
'''