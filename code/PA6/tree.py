import numpy as np
import pandas as pd

class TreeNode(object):
    def __init__(self):
        self.value = None
        self.indecies = None
        self.labels = None
        self.feature_index = None
        self.sub_trees = []

class DecisionTree(object):
    def __init__(self):
        self.root_node = None
    
    def predict(self):
        return

    def gini(self, feature_values, labels):
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
                #print(p_l)
                g_f -= p_l ** 2
            
            g += g_f * (len(label_set)/len(feature_values))
        
        return g

    def train(self, features, labels):
        self.root_node = TreeNode()
        #Add column number to the original data set for tracking purpuse
        _data = np.hstack(([[i] for i in range(0, features.shape[0])], features))

        self._split(_data, [0], labels, self.root_node)
    
    def _split(self, features, exclusion, labels, node):
        if len(np.unique(labels)) == 1:                     #All data points are in same label
            return
        if len(exclusion) == features.shape[1] - 1:          #No column left to split
            return
        
        _gini_all = [np.inf for i in range(0, features.shape[1])]
        _indecies = np.delete([i for i in range(0, features.shape[1])], exclusion)
        for i in _indecies:
            _gini_all[i] = self.gini(features[:,i], labels)

        node.feature_index = np.argmin(_gini_all)
        node.indecies = features[:,0]
        node.labels = labels

        unique_feature_values = np.unique(features[:, node.feature_index ]) 
        for f in unique_feature_values:
            sub_node = TreeNode()
            sub_node.value = f
            node.sub_trees += [sub_node]
            
            sub_features = features[features[:, node.feature_index] == f, :]
            sub_labels = labels[features[:, node.feature_index] == f]
            self._split(sub_features, exclusion + [node.feature_index], sub_labels, sub_node)

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

dt = DecisionTree()
#dt.train(train_feature, train_label)

features = np.array([[1,1,1],[2,2,2],[3,3,3]])
labels = np.array([1,2,3])
print(dt.gini(features[:,0], labels))

#print(dt.gini(train_feature[:,0], train_label))
