from streamlit_star_rating import st_star_rating
import plotly.express as px
import streamlit as st
import pandas as pd
import pickle
import sys
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from src.embeddings.car_make import CarMakeEmbedding

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
        pd.read_csv("./sample_tables/embedding_makes.csv"),
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

st.image("./vae_diagram.png", caption="Sunrise by the mountains")

st.write("## Safety Rating by Brand")

st.markdown(
    "The code evaluates two machine learning models, Random Forest and K-Nearest Neighbors (KNN), using a technique "
    "called `GridSearchCV` to find the best performing model. `GridSearchCV` systematically tests different "
    "combinations of hyperparameters for each model and identifies the combination that yields the highest "
    "cross-validation score. This score is an estimate of the model's performance on unseen data. Based on the "
    "results, the Random Forest model outperformed the KNN model, achieving a higher cross-validation score and "
    "likely demonstrating better generalization ability on the test set. This suggests that, for this specific "
    "dataset and problem, the Random Forest algorithm with the optimized hyperparameters is the more suitable "
    "choice for classification."
)

filename = "./models/rf_brands.pkl"
with open(filename, "rb") as file:
    loaded_model = pickle.load(file)

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
    label_encoder="./models/encoder.pkl",
    pkl_path="./models/embedding.pkl",
)

embedding = cme.execute(make).tolist()
df = pd.DataFrame(
    [embedding[0] + [year]], columns=[f"make_{i}" for i in range(10)] + ["vehicle_age"]
)
prediction = loaded_model.predict(df)[0]

st_star_rating(
    label="Model prediction",
    maxValue=5,
    defaultValue=prediction,
    read_only=True,
)

st.write("## Safety Rating by Accidents")
