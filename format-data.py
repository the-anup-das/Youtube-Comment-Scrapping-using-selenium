import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

cv=CountVectorizer(decode_error='ignore')

def classifier(message):
    
    transformed = cv.transform([message])
    prediction =  model.predict(transformed)
    if prediction[0] == 0:
        return "ham"
    else:
        return "spam"



data=pd.read_csv("comments.csv")

data.columns=['no','comments']

data=data.drop('no', axis=1)
#data.insert(0, "comments1", data['comments'], False) 

#print(type(data['comments']))
#print(data.head())


file = open('spam_model.pickle', 'rb')
model = pickle.load(file)
file.close()

label_lst=[]
for i in range(len(data)):
    label_lst.append(classifier(data.loc[i, "comments"]))

data.insert(0, "labels", label_lst, False)

dataset=pd.DataFrame(data)
dataset.to_csv("spam_data.csv")

print("Done!")