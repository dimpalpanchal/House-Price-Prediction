import json
import pickle
import pandas as pd


class HousePricePredictor:

    def __init__(self):

        with open(
            "artifacts/model.pkl",
            "rb"
        ) as file:
            self.model = pickle.load(file)

        with open(
            "artifacts/features.json",
            "r"
        ) as file:
            self.features = json.load(file)

    def predict(self, data: dict):

        df = pd.DataFrame(
            [data],
            columns=self.features
        )

        prediction = self.model.predict(df)

        return float(prediction[0])