import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


nutrient_data = pd.read_csv("Crop_recommendation.csv")

x = nutrient_data.drop(columns=["label"])
y = nutrient_data["label"]

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = DecisionTreeClassifier()
# model.fit(x_train,y_train)
model.fit(x,y)
new_data=pd.DataFrame([[70,60,20,24,55,7,140]],columns=x.columns)

predictions = model.predict(new_data)
print(predictions)

filename = 'finalized_model.sav'
joblib.dump(model, filename)