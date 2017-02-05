from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC

from sklearn import metrics

from sklearn.model_selection import GridSearchCV

from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

from sklearn.datasets import load_files

from sklearn.model_selection import train_test_split

DATA_PATH = './data'

TRAINING_SET_SIZE = 0.8

dataset = load_files(DATA_PATH)

n_samples_total = dataset.filenames.shape[0]

docs_train = [open(f).read() for f in dataset.filenames]

xTrain, xTest, yTrain, yTest = train_test_split(docs_train, dataset.target, test_size=0.25, random_state=42)

# Build a vectorizer / classifier pipeline using the previous analyzer
pipeline = Pipeline([
    ('vect', CountVectorizer(max_features=100000)),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC(C=1,kernel='linear')),
])

parameters = {
    'vect__max_df': (.95,),
}

# Fit the pipeline on the training set using grid search for the parameters
grid_search = GridSearchCV(pipeline, parameters, n_jobs=1)
grid_search.fit(xTrain[:200], yTrain[:200])

# Refit the best parameter set on the complete training set
clf = grid_search.best_estimator_.fit(xTrain, yTrain)

# Predict the outcome on the testing set
y_predicted = clf.predict(xTest)

# Print the classification report
print metrics.classification_report(yTest, y_predicted,
                                    target_names=dataset.target_names)

# Plot the confusion matrix
cm = metrics.confusion_matrix(yTest, y_predicted)
print cm

# import pylab as pl
plt.matshow(cm)
plt.show()