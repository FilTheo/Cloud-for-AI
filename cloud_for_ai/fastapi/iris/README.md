Reference [medium]([https://link-url-here.org](https://medium.com/analytics-vidhya/serve-a-machine-learning-model-using-sklearn-fastapi-and-docker-85aabf96729b)https://medium.com/analytics-vidhya/serve-a-machine-learning-model-using-sklearn-fastapi-and-docker-85aabf96729b)

In this example you will learn how to:
- Train and save a simple ML model on the simple Iris dataset
- Create an API that can take incoming predictions requests
- Get your API running using Docker

  ---

  The project structure will be the following:

```
iris/
│
├── models/
│   ├── ml/
│   │    ├── classifier.py
│   │    └── training.py
│   │    └── iris_dt_v1.joblib
│   └── Iris.py
│
├── tests/
│   ├── load_test.py
├── app.py
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
```

Lets take it step by step

## 1. Training the model
Sckit-learn, it's probably the most popular framework for classical machine learning in python; it has an easy-to-use API that supports the most common models.

Data set:

In this project, we'll use the Iris data set to train a classification model.

Iris data set comes with four features:

- sepal length in cm
- sepal width in cm
- petal length in cm
- petal width in cm
These features are used to classify each observation between one of three classes: Iris Setosa, Iris Versicolour, and Iris Virginica.

First, let's set up out train.py, import the methods and iris data, set the features to a NumPy ndarray called X, and the prediction categories to variable y.

```
from joblib import dump
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier


iris = datasets.load_iris(return_X_y=True)
X = iris[0]
y = iris[1]
```
Now, let us create a simple model, remember the main topic of this post isn't model training, so we'll keep it as simple as possible.

As preprocessing step, let's scale our variables and use a decision tree classifier with the default parameters for model training.

```
clf_pipeline = [('scaling', MinMaxScaler()), 
                ('clf', DecisionTreeClassifier(random_state=42))]
pipeline = Pipeline(clf_pipeline)

pipeline.fit(X, y)
```
And as the last step, let's save the trained model so we can use it with our API to make predictions
```
dump(pipeline, './iris_dt_v1.joblib')
```

## Creating the API
Before creating the predict method endpoint, we'll define our Iris model, so we let FastAPI know what we expect as request data; in our iris.py file, write

```
from pydantic import BaseModel, conlist
from typing import List


class Iris(BaseModel):
    data: List[conlist(float, min_length=4, max_length=4)]
```
With this code, we'll ensure that we get a list (or several lists) with the four variables that the model needs to make the prediction.

On the classifier.py, use
```
clf = None
```
clf will work as a placeholder so we can import and reuse our model

Let's now create an endpoint to send prediction requests; first, we need to import the main FastAPI method, the placeholder, and iris model we just created in our app.py

```
import models.ml.classifier as clf
from fastapi import FastAPI, Body
from joblib import load
from models.iris import Iris

app = FastAPI(title="Iris ML API", description="API for iris dataset ml model", version="1.0")
```
Now, we need to get our trained model; we'll make sure that FastAPI import the model only when the app gets started and not in every request because this would add extra latency which is a very bad thing.

So let's read the model and assign it.

```
@app.on_event('startup')
async def load_model():
    clf.model = load('models/ml/iris_dt_v1.joblib')
```
Next, we define the route that will take our requests; it will be a post method to /predict.

This method will take our Iris model to ensure that the request data format is correct and will return our class prediction and the log probabilities for each class.

```
@app.post('/predict', tags=["predictions"])
async def get_prediction(iris: Iris):
    data = dict(iris)['data']
    prediction = clf.model.predict(data).tolist()
    log_proba = clf.model.predict_proba(data).tolist()
    return {"prediction": prediction,
            "log_proba": log_proba}
```
Our base API is ready! by now, the app.py file looks like this

```
import models.ml.classifier as clf
from fastapi import FastAPI
from joblib import load
from models.iris import Iris

app = FastAPI(title="Iris ML API", description="API for iris dataset ml model", version="1.0")


@app.on_event('startup')
def load_model():
    clf.model = load('models/ml/iris_dt_v1.joblib')


@app.post('/predict', tags=["predictions"])
async def get_prediction(iris: Iris):
    data = dict(iris)['data']
    prediction = clf.model.predict(data).tolist()
    log_proba = clf.model.predict_log_proba(data).tolist()
    return {"prediction": prediction,
            "log_proba": log_proba}
```
Let's start it by running:

```
uvicorn app:app --port 5000
```

Now go to: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

Hit the predict end-point and add some values to the data.

You will see you get an outcome.

You can also try it from the terminal as follows

```
curl -X POST "http://127.0.0.1:5000/predict" -H\
 "accept: application/json"\
 -H "Content-Type: application/json"\
 -d "{\"data\":[[4.8,3,1.4,0.3],[2,1,3.2,1.1]]}"
```

## Run with Docker

Now lets dockerize the application to run it at every computer

First edit the requirements.txt by adding the following

```
fastapi==0.57.0
uvicorn==0.11.5
pydantic==1.5.1
starlette==0.13.4
python-multipart==0.0.5
requests==2.24.0
scikit-learn==0.23.1
joblib==0.16.0
```

Now the edit the Dockerfile

```
FROM tiangolo/uvicorn-gunicorn:python3.8-slim 

WORKDIR /app 
ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=app 
ADD requirements.txt . 
RUN pip install -r requirements.txt \    
    && rm -rf /root/.cache 
COPY . .
```
Now let's create the docker image and run the container.

```
docker build -t iris-ml-build .
docker run -d -p 80:80 --name iris iris-ml-build
```
Now go to [http://127.0.0.1/docs](http://127.0.0.1/docs)

You should see the same as before, but now it is running in a docker container; you could take this docker image to any cloud provider, and it should remain the same





