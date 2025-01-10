import joblib
from streamlit_star_rating import st_star_rating
import plotly.express as px
import streamlit as st
import pandas as pd
import pickle
import sys
import os
from sklearn.experimental import enable_iterative_imputer

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from src.analytics.models.car_make import CarMakeEmbedding

st.title("Models")

st.write("## Car Make Embedding")

st.markdown(
    "A car make embedding is a way of representing car brands as numerical codes that computers can understand. "
    "Think of it like translating car makes into a different language that allows computers to analyze and "
    "compare them.\n\n"
    "This information can be used to improve the performance of machine learning models in various tasks, such as:\n\n"
    "* **Predicting car prices:**  Embeddings can help models understand how the car make influences its price.\n"
    "* **Recommending cars:** Embeddings can help identify cars from similar or different brands based on user preferences.\n"
    "* **Analyzing brand trends:** Embeddings can be used to visualize relationships between car makes and identify trends in the market."
)

st.plotly_chart(
    px.scatter_3d(
        pd.read_csv("ui/sample_tables/embedding_makes.csv"),
        x="X",
        y="Y",
        z="Z",
        color="Make",
    ),
    use_container_width=True,
)


st.write("## Variational Autoencoder")

st.markdown(
    "This code defines a Variational Autoencoder (VAE) model, a special type of neural network that learns "
    "the underlying patterns in data. Imagine it like this: the VAE takes your data and compresses it into "
    "a smaller, simpler representation, like creating a zip file. But unlike a regular zip file, the VAE also "
    "learns how to create new data similar to the original. The VAE has two main parts:\n\n"
    "* **Encoder:** This part takes the original data and compresses it into a smaller representation, like creating a summary.\n\n"
    "* **Decoder:** This part takes the summary and tries to recreate the original data, like expanding the zip file.\n\n"
    "The magic happens in between these two parts. The VAE doesn't just create a simple summary; it learns a special "
    "code that captures the most important information about the data. This code can then be used to generate new "
    "data points that are similar to the original ones.\n\n"
    "VAEs have many applications, including:\n\n"
    "* **Generating new data:** VAEs can create new images, text, or other types of data that resemble the training data.\n\n"
    "* **Learning meaningful representations:** The compressed representation learned by the VAE can be used for other tasks, like classification or clustering.\n\n"
    "* **Removing noise from data:** VAEs can be used to clean up noisy data by reconstructing a cleaner version."
)

st.image("ui/vae_diagram.png", caption="Variational Autoencoder")

st.write("## Safety Rating by Brand")

st.markdown(
    """
    In this section, we tested two different machine learning models, Random Forest and K-Nearest Neighbors, 
    called `GridSearchCV` to find the best performing model. 

    `GridSearchCV` systematically tests different combinations of hyperparameters for each model and identifies 
    the combination that yields the highest cross-validation score. This score is an estimate of the model's 
    performance on unseen data.

    Based on the results, the Random Forest model outperformed the KNN model, achieving a higher 
    cross-validation score and likely demonstrating better generalization ability on the test set.

    The model that we trained used as input the car manufacturer and its age, and returns a prediction of the 
    safety rating that it would get in the NHTSA test. In order to make it more visually appealing, we decided 
    to compute here the embedding, a step that is being performed in the Feature Engineering layer.

    Below, the model can be tested.
    """
)

brand_model = joblib.load("ui/models/brand_rating_model.pkl")

col1, col2 = st.columns([1, 1])
make = col1.selectbox(
    "Car Make",
    (
        "honda",
        "ford",
        "alfa romeo",
        "jeep",
        "mazda",
        "dodge",
        "gmc",
        "volvo",
        "chevrolet",
        "buick",
        "ram",
        "toyota",
        "tesla",
        "freightliner",
    ),
)

year = col2.slider("Vehicle Age", 1, 30, 1)

cme = CarMakeEmbedding(
    label_encoder="ui/models/encoder.pkl",
    pkl_path="ui/models/embedding.pkl",
)

embedding = cme.execute(make).tolist()
df = pd.DataFrame(
    [embedding[0] + [year]], columns=[f"make_{i}" for i in range(10)] + ["vehicle_age"]
)
prediction = brand_model.predict(df)

st_star_rating(
    label="Model prediction",
    maxValue=5,
    defaultValue=prediction,
    read_only=True,
)

st.write("## Safety Rating by Accidents")

st.markdown(
    "The model employed is a Random Forest Regressor with a maximum depth of 10 and 200 decision trees "
    "(estimators). This model predicts the overall safety rating of cars based on the properties of the "
    "passengers who were driving them. The ratings are standardized to range from 0.5 to 5.0 in increments "
    "of 0.5. By using a Random Forest, the model can handle complex relationships and interactions between "
    "features without overfitting, thanks to the ensemble of multiple decision trees.\n\nTo assess the performance "
    "of the model, several metrics are used: mean absolute error (MAE), mean squared error (MSE), root mean squared "
    "error (RMSE), and the R-squared score (R²). These metrics provide a comprehensive evaluation of the model's "
    "accuracy and reliability. MAE and MSE measure the average magnitude of errors in the predictions, RMSE provides "
    "insight into the model's prediction error in the same units as the target variable, and R² indicates the "
    "proportion of variance in the dependent variable that is predictable from the independent variables. Together, "
    "these metrics help in understanding how well the model is performing in predicting the car safety ratings based "
    "on passenger characteristics."
)

vehicle_age = None
vehicle_make = None

col11, col12 = st.columns([1, 1])
vehicle_make = col11.selectbox(
    "Car make",
    (
        "honda",
        "ford",
        "alfa romeo",
        "jeep",
        "mazda",
        "dodge",
        "gmc",
        "volvo",
        "chevrolet",
        "buick",
        "ram",
        "toyota",
        "tesla",
        "freightliner",
    ),
)

vehicle_age = col12.slider("Vehicle age", 1, 30, 1)

col21, col22 = st.columns([1, 1])
person_sex = col21.selectbox(
    "Person Sex",
    ("Male", "Female", "Unknown"),
)
person_age = col22.slider("Person Age", 18, 85, 23)


cme = CarMakeEmbedding(
    label_encoder="ui/models/encoder.pkl",
    pkl_path="ui/models/embedding.pkl",
)

embedding = cme.execute(vehicle_make).tolist()
df2 = pd.DataFrame(
    [
        [
            person_sex == "Female",
            person_sex == "Male",
            person_sex == "Unknown",
            vehicle_age,
            person_age,
        ]
        + embedding[0]
    ],
    columns=["F", "M", "U", "person_age", "vehicle_age"]
    + [f"make_{i}" for i in range(10)],
)

accident_model = joblib.load("ui/models/accident_rating_model.pkl")
prediction2 = accident_model.predict(df2)[0]

st_star_rating(
    label="Model prediction",
    maxValue=5,
    defaultValue=prediction2,
    read_only=True,
)
