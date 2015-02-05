import sklearn as sk
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
from sklearn.datasets import fetch_olivetti_faces
from sklearn import metrics

def print_faces(images, target, top_n):
    '''
    helper function to plot the faces
    '''
    # set up the figure size in inches
    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1,
       hspace=0.05, wspace=0.05)
    for i in range(top_n):
        # plot the images in a matrix of 10x10, so altogether can 
        #plot 100 faces
        print i
        p = fig.add_subplot(10, 10, i + 1, xticks=[],yticks=[])
        p.imshow(images[i], cmap=plt.cm.bone)
        # label the image with the target value
        p.text(0, 14, str(target[i]))
        p.text(0, 60, str(i))
        
    plt.show()
    
def evaluate_cross_validation(clf, X, y, K):
    '''
    helper function to evaluate a classifier with cross validation
    '''
    # create a k-fold croos validation iterator
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))
        
def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    '''
    helper function to do the training and testing
    '''
    clf.fit(X_train, y_train)
    print "Accuracy on training set:"
    print clf.score(X_train, y_train)
    print "Accuracy on testing set:"
    print clf.score(X_test, y_test)
    y_pred = clf.predict(X_test)
    print "Classification Report:"
    print metrics.classification_report(y_test, y_pred)
    print "Confusion Matrix:"
    print metrics.confusion_matrix(y_test, y_pred)


#get the dataset
faces = fetch_olivetti_faces()
print faces.DESCR

#plot the faces
print_faces(faces.images, faces.target, 20)

#split data
X_train, X_test, y_train, y_test = train_test_split(faces.data, faces.target, test_size=0.25, random_state=0)
svc_1 = SVC(kernel='linear')

#using cross validation to evaluate on the training data
evaluate_cross_validation(svc_1, X_train, y_train, 5)

#training and testing
train_and_evaluate(svc_1, X_train, X_test, y_train, y_test)







