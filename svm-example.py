# We will need to convert everything to numbers and normalised (put them on the same scale)
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

# clf is classifier
# Changed gamma to 0.1 and predictions are off, Gamma as the learning rate (alpha)
clf = svm.SVC(gamma=0.001, C=100)

x,y = digits.data[:-10], digits.target[:-10]
clf.fit(x,y)

print('Prediction: ', clf.predict(digits.data[-4]))

plt.imshow(digits.images[-4], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()