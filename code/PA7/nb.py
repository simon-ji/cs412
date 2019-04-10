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
        _row_count = 0

        #Count
        for _row in train_data:
            _row_count += 1
            #for _feature_index in range(0, self.feature_count):
            
            _class = _row[-1]
            if _class in self.P_C:
                self.P_C[_class] += 1
            else:
                self.P_C[_class] = 1

        for _key in self.P_C.keys():
            self.P_C[_key] = self.P_C[_key] / _row_count
        



        print(self.P_C)

    def predict(self, X):
        return 
    

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