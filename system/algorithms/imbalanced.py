from collections import Counter
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.over_sampling import RandomOverSampler

class BalanceData:
    
    def __init__(self, algorithm=None, k_neighbors=1):
        self.algorithm = algorithm
        self.k_neighbors = k_neighbors

    def set_data(self, X, y):
        self.X, self.y = X, y

    def run(self):
        if self.algorithm == "SMOTE":
            self.X_resampled, self.y_resampled = SMOTE(kind='regular', k_neighbors=self.k_neighbors).fit_resample(self.X, self.y)
        else:
            if self.algorithm == "ADASYN":
                self.X_resampled, self.y_resampled = ADASYN(kind='regular', k_neighbors=self.k_neighbors).fit_resample(self.X, self.y)
            else:
                ros = RandomOverSampler(random_state=0)
                self.X_resampled, self.y_resampled = ros.fit_resample(self.X, self.y)

        print(sorted(Counter(self.y_resampled).items()))
        return self.X_resampled, self.y_resampled
