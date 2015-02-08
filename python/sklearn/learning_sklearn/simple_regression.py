import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
boston = load_boston()
print boston.data.shape
print boston.feature_names
print np.max(boston.target), np.min(boston.target),np.mean(boston.target)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test =train_test_split(boston.data, boston.target, test_size=0.25,random_state=33)
from sklearn.preprocessing import StandardScaler
scalerX = StandardScaler().fit(X_train)
scalery = StandardScaler().fit(y_train)
X_train = scalerX.transform(X_train)
y_train = scalery.transform(y_train)
X_test = scalerX.transform(X_test)
y_test = scalery.transform(y_test)

from sklearn.cross_validation import *
def train_and_evaluate(clf, X_train, y_train):
    clf.fit(X_train, y_train)
    print "Coefficient of determination on training set:",clf.score(X_train, y_train)
    # create a k-fold cross validation iterator of k=5 folds
    cv = KFold(X_train.shape[0], 5, shuffle=True,
       random_state=33)
    scores = cross_val_score(clf, X_train, y_train, cv=cv)
    print "Average coefficient of determination using 5-fold crossvalidation:",np.mean(scores)
       
from sklearn import linear_model
clf_sgd = linear_model.SGDRegressor(loss='squared_loss',
   penalty=None,  random_state=42)
train_and_evaluate(clf_sgd,X_train,y_train)

clf_sgd1 = linear_model.SGDRegressor(loss='squared_loss',penalty='l2',  random_state=42)
train_and_evaluate(clf_sgd1, X_train, y_train)

##Surport vector machine for regression
from sklearn import svm
clf_svr = svm.SVR(kernel='linear')
train_and_evaluate(clf_svr, X_train, y_train)

#use non-linear kernel
clf_svr_poly = svm.SVR(kernel='poly')
train_and_evaluate(clf_svr_poly, X_train, y_train)

clf_svr_rbf = svm.SVR(kernel='rbf')
train_and_evaluate(clf_svr_rbf, X_train, y_train)

#use RF to do regression
from sklearn import ensemble
clf_et=ensemble.ExtraTreesRegressor(n_estimators=10,
   compute_importances=True, random_state=42)
train_and_evaluate(clf_et, X_train, y_train)

from sklearn import metrics
def measure_performance(X, y, clf, show_accuracy=True, show_classification_report=True, show_confusion_matrix=True,show_r2_score=False):
    y_pred = clf.predict(X)
    if show_accuracy:
        print "Accuracy:{0:.3f}".format(metrics.accuracy_score(y, y_pred)),"\n"
    if show_classification_report:
        print "Classification report"
        print metrics.classification_report(y, y_pred),"\n"
    if show_confusion_matrix:
        print "Confusion matrix"
        print metrics.confusion_matrix(y, y_pred),"\n"
    if show_r2_score:
        print "Coefficient of determination:{0:.3f}".format(metrics.r2_score(y, y_pred)),"\n"

measure_performance(X_test, y_test, clf_et,show_accuracy=False, show_classification_report=False,show_confusion_matrix=False, show_r2_score=True)


