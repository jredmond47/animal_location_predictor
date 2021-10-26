#adapted from https://heartbeat.comet.ml/working-with-geospatial-data-in-machine-learning-ad4097c7228d
#https://www.programcreek.com/python/example/103493/sklearn.cluster.AgglomerativeClustering
#https://towardsdatascience.com/dbscan-clustering-for-data-shapes-k-means-cant-handle-well-in-python-6be89af4e6ea

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans , AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

os.chdir('c:\\Users\\gilma\\animal_tracking\\api\\data\\movebank')

#path = os.path.join('data','movebank','gps_events_s21231406_i24563363_ss653.csv')

data = pd.read_csv("gps_events_s8019591_i54137415_ss653.csv", dtype={
    "location_lat": float,
    "location_long": float},
                   low_memory=False)
data.dropna()
data =data[~data.isin([np.nan, np.inf, -np.inf]).any(1)]

data_coo = data[["location_lat" , "location_long"]]

#s21231406_i24563363_ss653
#data.drop(columns=['height_above_ellipsoid',
#                   'import_marked_outlier',
#                   'magnetic_field_raw_x',
#                   'magnetic_field_raw_y',
#                   'magnetic_field_raw_z'])


#plt.figure(figsize = (15,8))
#sns.scatterplot(data["location_lat"], data["location_long"])

x = data["location_lat"]
y = data["location_long"]
sns.regplot(x, y)
plt.scatter(x, y)
plt.show()

#create clusters with DBSCAN

#Transform data for DBSCAN
scaler = StandardScaler()
data_coo_scaled = scaler.fit_transform(data_coo)

# cluster the data into five clusters
dbscan = DBSCAN(eps=0.13, min_samples = 7)
clusters = dbscan.fit_predict(data_coo_scaled)

# plot the cluster assignments
plt.scatter(data["location_lat"], data["location_long"], c=clusters, cmap="plasma")
plt.xlabel("Latitute")
plt.ylabel("Longitute")
plt.show()

# transform the data to be stretched
rng = np.random.RandomState(74)
transformation = rng.normal(size=(2, 2))
data_coo_scaled_kmeans = np.dot(data_coo, transformation)

# create clusters using k-means clustering algorithm.
#kmeans = KMeans(5)
#clusters = kmeans.fit_predict(data[['location_lat','location_long']])
#data['location_cluster'] = kmeans.predict(data[['location_lat','location_long']])

# create clusters using k-means - NOT WORKING
kmeans = KMeans(n_clusters=3)
kmeans.fit(data_coo_scaled_kmeans)
y_pred = kmeans.predict(data_coo_scaled_kmeans)

# plot the cluster assignments and cluster centers
plt.scatter(data["location_lat"], data["location_long"],
            c=y_pred, cmap="plasma")
plt.scatter(kmeans.cluster_centers_[:, 21],
            kmeans.cluster_centers_[:, 22],
            marker='^',
            c=[0, 1, 2],
            s=100,
            linewidth=2,
            cmap="plasma")
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.show()

# creates clusters using hierarchical clustering.
agc = AgglomerativeClustering(n_clusters =5, affinity='euclidean', linkage='ward')
data['location_cluster'] = agc.fit_predict(data[['location_lat','location_long']])