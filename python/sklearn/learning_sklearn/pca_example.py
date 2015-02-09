from sklearn.datasets import load_digits
digits = load_digits()
X_digits, y_digits = digits.data, digits.target

import matplotlib.pyplot as plt
n_row, n_col = 2, 5

def print_digits(images, y, max_n=10):
    # set up the figure size in inches
    fig = plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    i=0
    while i < max_n and i < images.shape[0]:
        p = fig.add_subplot(n_row, n_col, i + 1, xticks=[],yticks=[])
        p.imshow(images[i], cmap=plt.cm.bone,
             interpolation='nearest')
        # label the image with the target value
        p.text(0, -1, str(y[i]))
        i=i+ 1
        
    plt.show()

print_digits(digits.images, digits.target, max_n=10)

def plot_pca_scatter():
    colors = ['black', 'blue', 'purple', 'yellow', 'white','red', 'lime', 'cyan', 'orange', 'gray']
    for i in xrange(len(colors)):
        px = X_pca[:, 0][y_digits == i]
        py = X_pca[:, 1][y_digits == i]
        plt.scatter(px, py, c=colors[i])
    plt.legend(digits.target_names)
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.show()
    
from sklearn.decomposition import PCA
estimator = PCA(n_components=2)
X_pca = estimator.fit_transform(X_digits)
plot_pca_scatter()

def print_pca_components(images, n_col, n_row):
    plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    for i, comp in enumerate(images):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(comp.reshape((8, 8)),
             interpolation='nearest')
        plt.text(0, -1, str(i + 1) + '-component')
        plt.xticks(())
        plt.yticks(())
    plt.show()

