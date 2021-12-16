import re

from nltk.stem.snowball import SnowballStemmer
from textpreprocessing import TextPreprocessor
from custom import CustomModelPrediction

class Classifier:

    def __init__(self):
        self.symbols = re.compile('[@_!#$%^&*()<>?/\|}{~:]|[0-9]')
        self.stemmer = SnowballStemmer("english")

    def classify(self,products):
        if len(products)==0:
            return []
        predict_requests_stemmed = []
        for title in products:
            result = ""
            for word in title.split():
                if self.symbols.search(word)== None:
                    result+=(self.stemmer.stem(word)+" ")
            result = result.replace('"','')
            predict_requests_stemmed.append(result)
        #print(predict_requests_stemmed)

        types = ['Appliances','Electronics',
        'Grocery & Gourmet Food', 'Home & Kitchen' ,'Musical Instruments',
        'Office Products' ,'Patio Lawn & Garden' ,'Pet Supplies',
        'Sports & Outdoors' ,'Tools & Home Improvement']
        classifier = CustomModelPrediction.from_path(".")
        results = classifier.predict(predict_requests_stemmed)
        #print(results)
        categories = []
        for i in range(len(results)):
            #print('Predicted labels')
            #print(results)
            # for idx,val in enumerate(results[i]):
            #     if val>0.33:
            #         print(types[idx], "with :",val*100,"accuracy")
            idx=results[i].index(max(results[i]))
            if results[i][idx]<0.33:
                categories+=["Other"]
            else:
                categories+=[types[idx]]
        return categories