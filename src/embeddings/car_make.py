import torch
import pickle
import pandas as pd
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
import numpy as np


class CarMakeEmbedding:
    def __init__(
        self, csv_path=None, label_encoder=None, pkl_path=None, embedding_size=10
    ):
        if label_encoder and pkl_path:
            with open(label_encoder, "rb") as f:
                self.label_encoder = pickle.load(f)
            self.num_makes = len(self.label_encoder.classes_)
            self.embedding = nn.Embedding(
                num_embeddings=self.num_makes, embedding_dim=embedding_size
            )
            self.embedding.load_state_dict(torch.load(pkl_path))
        elif csv_path:
            self.csv_path = csv_path
            self.embedding_size = embedding_size
            self._train()
        else:
            raise ValueError(
                "Either csv_path or both label_encoder and pkl_path must be provided."
            )

    def execute(self, make_str):
        make_encoded = self.label_encoder.transform([make_str])
        make_tensor = torch.tensor(make_encoded, dtype=torch.long)
        return self.embedding(make_tensor).detach().cpu().numpy()

    def reverse_execute(self, embedding):
        all_embeddings = self.embedding.weight.detach().cpu().numpy()
        differences = np.linalg.norm(all_embeddings - embedding, axis=1)
        closest_index = np.argmin(differences)
        return self.label_encoder.inverse_transform([closest_index])[0]

    def _train(self):
        self.data_make = pd.read_csv(self.csv_path)["Make"]
        self.data_make = list(map(lambda x: x.lower(), list(self.data_make)))
        self.label_encoder = LabelEncoder()
        make_encoded = self.label_encoder.fit_transform(self.data_make)
        self.make_tensor = torch.tensor(make_encoded, dtype=torch.long)
        self.num_makes = len(self.label_encoder.classes_)
        self.embedding = nn.Embedding(
            num_embeddings=self.num_makes, embedding_dim=self.embedding_size
        )

    def save(self, encoder_path, embedding_path):
        with open(encoder_path, "wb") as f:
            pickle.dump(self.label_encoder, f)
        torch.save(self.embedding.state_dict(), embedding_path)
