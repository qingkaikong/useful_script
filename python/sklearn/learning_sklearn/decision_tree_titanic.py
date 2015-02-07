import csv
import numpy as np


#read in data
with open('./titanic.csv', 'rb') as csvfile:
    titanic_reader = csv.reader(csvfile, delimiter=',',quotechar='"')
    # Header contains feature names
    row = titanic_reader.next()
    feature_names = np.array(row)
    # Load dataset, and target classes
    titanic_X, titanic_y = [], []
    for row in titanic_reader:
        titanic_X.append(row)
        titanic_y.append(row[2]) # The target value is "survived"
    titanic_X = np.array(titanic_X)
    titanic_y = np.array(titanic_y)
    
# we keep class, age and sex
titanic_X = titanic_X[:, [1, 4, 10]]
feature_names = feature_names[[1, 4, 10]]

# We have missing values for age
# Assign the mean value
ages = titanic_X[:, 1]
mean_age = np.mean(titanic_X[ages != 'NA',1].astype(np.float))
titanic_X[titanic_X[:, 1] == 'NA', 1] = mean_age

# Encode sex
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
label_encoder = enc.fit(titanic_X[:, 2])
print "Categorical classes:", label_encoder.classes_
integer_classes =label_encoder.transform(label_encoder.classes_)
print "Integer classes:", integer_classes
t = label_encoder.transform(titanic_X[:, 2])
titanic_X[:, 2] = t

#Using one hot encoder
from sklearn.preprocessing import OneHotEncoder
enc = LabelEncoder()
label_encoder = enc.fit(titanic_X[:, 0])
print "Categorical classes:", label_encoder.classes_
integer_classes = label_encoder.transform(label_encoder.classes_).reshape(3, 1)
print "Integer classes:", integer_classes
enc = OneHotEncoder()
one_hot_encoder = enc.fit(integer_classes)
# First, convert classes to 0-(N-1) integers using label_encoder
num_of_rows = titanic_X.shape[0]
t = label_encoder.transform(titanic_X[:,0]).reshape(num_of_rows, 1)
# Second, create a sparse matrix with three columns, each one indicating if the instance belongs to the class
new_features = one_hot_encoder.transform(t)
# Add the new features to titanix_X
titanic_X = np.concatenate([titanic_X,new_features.toarray()], axis = 1)
#Eliminate converted columns
titanic_X = np.delete(titanic_X, [0], 1)
# Update feature names
feature_names = ['age', 'sex', 'first_class', 'second_class','third_class']
# Convert to numerical values
titanic_X = titanic_X.astype(float)
titanic_y = titanic_y.astype(float)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(titanic_X, titanic_y, test_size=0.25, random_state=33)

#decision tree
from sklearn import tree
clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=3,min_samples_leaf=5)
clf = clf.fit(X_train,y_train)

import pydot,StringIO
dot_data = StringIO.StringIO()
tree.export_graphviz(clf, out_file=dot_data,feature_names=['age','sex','1st_class','2nd_class', '3rd_class'])
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_png('titanic.png')

from sklearn import metrics

def measure_performance(X,y,clf, show_accuracy=True,show_classification_report=True, show_confussion_matrix=True):
    y_pred=clf.predict(X)
    if show_accuracy:
        print "Accuracy:{0:.3f}".format(
            metrics.accuracy_score(y, y_pred)),"\n"
    if show_classification_report:
        print "Classification report"
        print metrics.classification_report(y,y_pred),"\n"
    if show_confussion_matrix:
      print "Confussion matrix"
      print metrics.confusion_matrix(y,y_pred),"\n"

measure_performance(X_train,y_train,clf,show_classification_report=False, show_confussion_matrix=False)

from sklearn.cross_validation import cross_val_score, LeaveOneOut
from scipy.stats import sem
def loo_cv(X_train, y_train,clf):
    # Perform Leave-One-Out cross validation
    # We are preforming 1313 classifications!
    loo = LeaveOneOut(X_train[:].shape[0])
    scores = np.zeros(X_train[:].shape[0])
    for train_index, test_index in loo:
        X_train_cv, X_test_cv = X_train[train_index],X_train[test_index]
        y_train_cv, y_test_cv = y_train[train_index],y_train[test_index]
        clf = clf.fit(X_train_cv,y_train_cv)
        y_pred = clf.predict(X_test_cv)
        scores[test_index] = metrics.accuracy_score(y_test_cv.astype(int), y_pred.astype(int))
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

loo_cv(X_train, y_train,clf)

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10, random_state=33)
clf = clf.fit(X_train, y_train)
loo_cv(X_train, y_train, clf)


clf_dt = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3, min_samples_leaf=5)
clf_dt.fit(X_train, y_train)
measure_performance(X_test, y_test, clf_dt)
