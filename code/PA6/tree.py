import numpy as np
import pandas as pd


def gini(feature_values, labels):
    unique_feature_value = np.unique(feature_values)
    unique_label_value = np.unique(labels)
    
    feature_value_set = {}
    for f in unique_feature_value:
        feature_value_set[f] = np.where(feature_values == f)[0]
    
    g = 0
    for f in unique_feature_value:
        g_f = 1
        label_set = labels[feature_value_set[f]]
        for l in unique_label_value:
            p_l = np.sum(label_set == l) / len(label_set)
            g_f -= p_l ** 2
        
        g += g_f * (len(label_set)/feature_values.shape[0])
    
    return g

def split_tree(features, labels):
    gini_all = [gini(features[:,i], labels) for i in range(0, features.shape[1])]

    feature_index = np.argmin(gini_all)
    unique_feature_values = np.unique(features[:, feature_index])
    children_indices = {}
    for f in unique_feature_values:
        children_indices[f] = labels[features[:, feature_index] == f].index

    return

data = pd.read_csv('training.txt', sep=' ', header = None)
train_label = data[0]
train_feature = np.array(data.iloc[:,1:])

for i in range(0, train_feature.shape[0]):
    train_feature[i] = [int(d.split(':')[1]) for d in train_feature[i]]

data = pd.read_csv('testing.txt', sep=' ', header = None)
test_feature = np.array(data)

for i in range(0, test_feature.shape[0]):
    test_feature[i] = [int(d.split(':')[1]) for d in test_feature[i]]

split_tree(train_feature, train_label)