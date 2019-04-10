import pandas as pd
import numpy as np

class  NaiveBayes(object):
    def __init__(self):
        self.P_C = None
        self.P_X_C = None
        self.feature_count = 0
        self.class_count = 0
    
    def fit(self, train_data, class_values, features_values):
        self.class_count = len(class_values)
        self.P_C = {c:0 for c in class_values}

        self.feature_count = len(features_values)
        self.P_X_C = [{i:{c:0 for c in class_values} for i in values} for values in features_values ]

        #Count
        for _row in train_data:
            _class_type = _row[-1]
            self.P_C[_class_type] += 1
            for _feature_index in range(0, self.feature_count):
                _feature_value = _row[_feature_index]
                self.P_X_C[_feature_index][_feature_value][_class_type] += 1

        #Calculate probabilities
        for _feature_index in range(0, self.feature_count):
            for _feature_key in self.P_X_C[_feature_index].keys():
                for _class_key in self.P_X_C[_feature_index][_feature_key].keys():
                    self.P_X_C[_feature_index][_feature_key][_class_key] = \
                        (self.P_X_C[_feature_index][_feature_key][_class_key] + 0.1) \
                            / (self.P_C[_class_key] + 0.1 * len(features_values[_feature_index]))
                
        for _class_key in self.P_C.keys():
            self.P_C[_class_key] = (self.P_C[_class_key] + 0.1) / (len(train_data) + 0.1 * self.class_count)


    def predict(self, X):
        p = 0
        for c in self.P_C.keys():
            for i in X:
                p += 1
    
        return p


data = np.array(pd.read_csv('data.txt'))

train = data[data[:, -1] > 0][:, 1:]
test = data[data[:, -1] < 0][:, 1:]

nb = NaiveBayes()
class_values = [1,2,3,4,5,6,7]
features_values = [
    [0,1],
    [0,1],
    [0,1],
    [0,1],    
    [0,1],
    [0,1],    
    [0,1],
    [0,1],  
    [0,1],
    [0,1],
    [0,1],
    [0,1],       
    [0,2,4,5,6,8],
    [0,1],
    [0,1],    
    [0,1],
]
nb.fit(train,class_values, features_values)