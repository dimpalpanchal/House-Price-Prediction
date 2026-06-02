from fastapi import FastAPI

from src.prediction.predict import (
    HousePricePredictor
)

from src.prediction.schema import (
    HouseData
)


app = FastAPI(
    title="House Price Prediction API",
    version="1.0"
)

predictor = HousePricePredictor()


@app.get("/")
def home():

    return {
        "message":
        "House Price Prediction API Running"
    }


@app.post("/predict")
def predict(data: HouseData):

    input_data = {
        "OverallQual": data.OverallQual,
        "GrLivArea": data.GrLivArea,
        "GarageCars": data.GarageCars,
        "GarageArea": data.GarageArea,
        "TotalBsmtSF": data.TotalBsmtSF,
        "1stFlrSF": data.FirstFlrSF,
        "FullBath": data.FullBath,
        "TotRmsAbvGrd": data.TotRmsAbvGrd,
        "YearBuilt": data.YearBuilt,
        "YearRemodAdd": data.YearRemodAdd,
        "MasVnrArea": data.MasVnrArea,
        "Fireplaces": data.Fireplaces,
        "LotArea": data.LotArea
    }

    prediction = predictor.predict(
        input_data
    )

    return {
        "predicted_price":
        round(prediction, 2)
    }