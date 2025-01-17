# import numpy as np
from operator import index
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# what we need for today
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster

from sklearn import metrics 
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

import scikitplot as skplt





# WARMUP EXERICSE:
# dataset:
# https://vincentarelbundock.github.io/Rdatasets/csv/Stat2Data/Election08.csv

# task
# use hierarchical clustering on the election dataset
# keep just the numerical columns
# add state abbreviation as the index
# use complete linkage and generate 4 clusters
# put back onto the original dataset
# profile the number of states by cluster assignment and the % that Obama won


# read in the dataset
URL = "https://vincentarelbundock.github.io/Rdatasets/csv/Stat2Data/Election08.csv"
eo = pd.read_csv(URL)
eo.shape
eo.head(3)

# state an index
# just numeric data

eo.columns = eo.columns.str.lower()

eo.index = eo.abr

election = eo.loc[:,"income":"dem.rep"]



# standardized


# caculate z score
scaler = StandardScaler()
escaled = scaler.fit_transform(election)

# cluster now
hc1.shape
hc1 = linkage(escaled, method = 'complete')


# plot

plt.figure(figsize=(15,5))
dendrogram(hc1,labels = election.index)
plt.show()



# extract 4 clusters

eo['cluster'] = fcluster(hc1,4, criterion='maxclust')
eo.sample(3)



# value counts
#counts on each cluster
eo.cluster.value_counts()


#profiling
eo.groupby('cluster')['obamawin'].mean()



eo.index = eo.State
eo.drop(columns="State", inplace=True)

election = eo.loc[:, "Income":"Dem.Rep"]

scaler = StandardScaler()
election_scaled = scaler.fit_transform(election)
type(election_scaled)

hc1 = linkage(election_scaled, method="complete")
hc1

# create the plot
plt.figure(figsize=(15,5))
dendrogram(hc1)
plt.show()

# create 4 clusters
cluster = fcluster(hc1, 4, criterion="maxclust")
cluster

eo['cluster'] = cluster

# simple profile of a cluster
eo.groupby('cluster')['ObamaWin'].mean()
eo.cluster.value_counts()

eo.loc[eo.cluster==4, :]




######### KMEANS

SQL = "SELECT * from `questrom.datasets.judges`"
PROJECT = "ba820-330120"
judges = pd.read_gbq(SQL, PROJECT)

judges.shape

judges.sample(3)

judges.info()

# column lowercase
judges.columns = judges.columns.str.lower()

# the judge as the index
judges.index = judges.judge
del judges['judge']

# the datatypes
judges.dtypes

# lets describe the dataset
judges.describe().T

# fit our first kmeans - 3 clusters
k3 = KMeans(3, random_state=820)
k3.fit(judges)

k3_labs = k3.predict(judges)
k3_labs

# how many iterations were needed for convergence
k3.n_iter_

# put these back onto the original dataset
judges['k3'] = k3_labs
judges.sample(3)

# start to profile/learn about our cluster
judges.k3.value_counts()

# groupby
k3 = judges.groupby("k3").mean()

k3.T

sns.heatmap(k3, cmap='Reds')
plt.show()

### take 5 minutes
### fit a cluster solution that has 5 clusters
### add to the judges dataset
### how many records in each cluster
### the "mean" profile to personas of the 5-cluster solution


j = judges.copy()
del j['k3']
k5 = KMeans(5,random_state=820)
k5.fit(j)

# check iterations for convergence
k5.n_iter_


# put labs back on the original dataset
j['k5'] = k5.predict(j)


# start to profile/learn about our cluster
j.k5.value_counts()

#  groupby labels
k5_profile = j.groupby('k5').mean()
k5_profile.T

sns.heatmap(k5_profile,cmap='Reds')
plt.show()


k5.inertia_


## fit range of cluster solutions for 2 to 10. k=2, k3

# interia



for i in range(2,11):
    j = judges.copy()
    del j['k3']
    k = KMeans(i,random_state=830)
    k.fit(j)
    print(k.inertia_)




silo_overall = metrics.silhouette_score(j, k5.predict[j])
silo_overall




judges.sample(3)
j = judges.copy()
del j['k3']
j.head(3)

k5 = KMeans(5)
judges['k5'] = k5.fit_predict(j)
judges.sample(3)

# extract the cluster centers
# # clusters, # features
j.shape

k5.cluster_centers_

test_centers = k5.cluster_centers_
test_centers.shape

judges.k5.value_counts()
k5_profile = judges.groupby("k5").mean()
k5_profile

sns.heatmap(k5_profile)
plt.show()


####### goodness of fit
k3.inertia_
k5.inertia_


## exercise
## how would you iterate over solutions from 2 - 10 on the judges dataset
## fit the cluster solution for 2 - 10
## and how would evaluate/inspect the inertia for solutions
KRANGE = range(2, 11)

# create a container
ss = []

for k in KRANGE:
    km = KMeans(k)
    lab = km.fit_predict(j)
    ss.append(km.inertia_)

sns.lineplot(KRANGE, ss)
plt.show()


# silo scores - k5
k5.inertia_

# silo score from sklearn --- metrics module

silo_overall = metrics.silhouette_score(j, k5.predict(j))
silo_overall

silo_sample = metrics.silhouette_samples(j,k5.predict(j))
silo_sample


# silo samples
silo_samples = metrics.silhouette_samples(j, k5.predict(j))
type(silo_samples)
silo_samples.shape

# plot up the the fit
skplt.metrics.plot_silhouette(j, k5.predict(j), figsize=(7,7))
plt.show()


