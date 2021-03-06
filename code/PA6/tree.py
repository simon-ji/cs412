import numpy as np
import pandas as pd
from collections import Counter

class TreeNode(object):
    def __init__(self):
        self.value = None
        self.indecies = None
        self.labels = None
        self.gini_value = None
        self.parent_gini_value = 1
        self.split_feature_index = None
        self.majority_vote = None
        self.majority_ratio = None
        self.sub_trees = {}

class DecisionTree(object):
    def __init__(self, min_sample = 5):
        self.root_node = None
        self.leaf_count = 0
        self.min_sample = min_sample
    
    def predict(self, X):
        _value = None
        _node = self.root_node

        while len(_node.sub_trees) > 0 and (X[_node.split_feature_index] in _node.sub_trees):
            _node = _node.sub_trees[X[_node.split_feature_index]]
            _value = _node.majority_vote     
        
        return _value

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
        if len(np.unique(labels)) == 1:                      #All data points are in same label
            print("All data points in same class")
            return
        if len(exclusion) == features.shape[1] - 1:          #No column left to split
            print("No column left to split")
            return
        if features.shape[0] < self.min_sample:              #No sample left
            print("No sample left")
            return

        _gini_all = [np.inf for i in range(0, features.shape[1])]
        _indecies = np.delete([i for i in range(0, features.shape[1])], exclusion)
        for i in _indecies:
            _gini_all[i] = self.gini(features[:,i], labels)

        _split_index = np.argmin(_gini_all)
        # Do not need to do this
        # if (node.parent_gini_value <= _gini_all[_split_index]):
        #     print("Parent is better. %f < %f"%(node.parent_gini_value, _gini_all[_split_index]))
        #     return
        node.split_feature_index = _split_index - 1
        node.gini_value =  _gini_all[_split_index]
        # print("Split on %d, gini=%f"%(_split_index, node.gini_value))

        _unique_feature_values = np.unique(features[:, _split_index])
        all_indices = {f:features[:, _split_index] == f for f in _unique_feature_values}

        #Check all subtree must contains at least min samples
        _subtree_sample = [sum(all_indices[f]) >= self.min_sample for f in all_indices.keys()]
        if (sum(_subtree_sample) < len(_subtree_sample)):     
            return

        for f in all_indices.keys():
            _indices = all_indices[f]
            if len(_indices) > 0:              #Must has at least one sample for this value
                _sub_features = features[_indices, :]
                _sub_labels = labels[_indices]

                _sub_node = TreeNode()
                _sub_node.value = f
                _sub_node.parent_gini_value = node.gini_value
                _sub_node.indecies = _sub_features[:, 0]
                _sub_node.labels = _sub_labels
                c = Counter(_sub_labels)
                _sub_node.majority_vote = c.most_common(1)[0][0]
                _sub_node.majority_ratio = c.most_common(1)[0][1] / len(_sub_labels)

                # print("index= %d Split value=%d majority_vote=%d majority_ratio = %f majority_count=%d"%
                #         (_split_index, f, _sub_node.majority_vote, _sub_node.majority_ratio, c.most_common(1)[0][1]))
                node.sub_trees[f] = _sub_node

                if (_sub_node.majority_ratio < 1) and (len(exclusion) < features.shape[1] - 2) \
                    and (len(_sub_labels) > self.min_sample):
                    self._split(_sub_features, exclusion + [_split_index], _sub_labels, _sub_node)
                else:
                    self.leaf_count += 1
                    # print("%d, %f"%(len(_sub_labels), _sub_node.majority_ratio))

        return

    def explore_structure(self):
        self.explore_tree(self.root_node, 0)
    
    def explore_tree(self, node, deepth):
        if (len(node.sub_trees) == 0):
            print("Deepth: %d Sample Count:%d"%(deepth, len(node.labels)))
        else:
            for k in node.sub_trees.keys():
                self.explore_tree(node.sub_trees[k], deepth + 1)


data = pd.read_csv('training.txt', sep=' ', header = None)
train_label = np.array(data[0])
train_feature = np.array(data.iloc[:,1:])

for i in range(0, train_feature.shape[0]):
    train_feature[i] = [int(d.split(':')[1]) for d in train_feature[i]]

data = pd.read_csv('testing.txt', sep=' ', header = None)
test_feature = np.array(data)

for i in range(0, test_feature.shape[0]):
    test_feature[i] = [int(d.split(':')[1]) for d in test_feature[i]]

####Testing
# Fold = 5

# train_sample_count = int(len(train_feature) / Fold)
# sample_indecis = np.random.choice(len(train_feature), len(train_feature), replace=False)
# sample = []
# for i in range(0, Fold):
#     sample += [sample_indecis[(i * train_sample_count):((i + 1) * train_sample_count)]]

# for m in [1, 2, 4, 8, 12, 16, 20, 24, 30, 34, 40]:
#     train_acc = 0
#     test_acc = 0
#     for k in range(0, Fold):
#         train_sample = np.array([], np.int)
#         for i in range(0, Fold):
#             if i != k:
#                 train_sample = np.append(train_sample, sample[i])
#         test_sample = sample[k]

#         dt = DecisionTree(m)
#         dt.train(train_feature[train_sample], train_label[train_sample])
#         # print("Min_Sample:%d, Leaf Count:%d"%(m, dt.leaf_count))
#         train_predict = [train_label[i] == dt.predict(train_feature[i]) for i in train_sample]
#         test_predict = [train_label[i] == dt.predict(train_feature[i]) for i in test_sample]
#         train_acc += sum(train_predict)/len(train_predict)
#         test_acc += sum(test_predict)/len(test_predict)

#     print("[%d] Training Accuracy:%f, Test Accuracy:%f"%(m, train_acc / Fold, test_acc / Fold))


dt = DecisionTree(16)
dt.train(train_feature, train_label)
# dt.explore_structure()
for x in test_feature:
    print(dt.predict(x))