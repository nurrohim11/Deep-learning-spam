from flask import Flask,render_template,url_for,request
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib as jb
import sys
import logging
import os
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')

@app.route('/')
def home():
    # THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    # my_file = os.path.join(THIS_FOLDER, 'home.html')
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    df = pd.read_csv('spam.csv',encoding='ISO-8859-1')
    df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
    df['label'] = df['class'].map({'ham': 0, 'spam': 1})
    y = df['label']
    # Features and Labels
    X = df['message']
    cv = CountVectorizer()
    X = cv.fit_transform(X)

    # Fit the Data
    # Extract Feature With CountVectorizer
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    #Naive Bayes Classifier
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    clf.score(X_test,y_test)
    #Alternative Usage of Saved Model
    # joblib.dump(clf, 'NB_spam_model.pkl')
    # NB_spam_model = open('NB_spam_model.pkl','rb')
    # clf = joblib.load(NB_spam_model)
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
    return render_template('result.html',prediction = my_prediction)

if __name__ == '__main__':
    app.run(debug=True)