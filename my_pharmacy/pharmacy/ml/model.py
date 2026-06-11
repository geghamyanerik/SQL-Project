from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from .dataset import data

class MedicineModel:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = RandomForestClassifier()

        X = [x[0] for x in data]
        y = [x[1] for x in data]

        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)

    def predict(self, symptom):
        vec = self.vectorizer.transform([symptom])
        return self.model.predict(vec)[0]