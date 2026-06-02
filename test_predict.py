from src.prediction.predict import HousePricePredictor

predictor = HousePricePredictor()

sample = {
    "OverallQual": 8,
    "GrLivArea": 2200,
    "GarageCars": 2,
    "GarageArea": 500,
    "TotalBsmtSF": 1200,
    "1stFlrSF": 1200,
    "FullBath": 2,
    "TotRmsAbvGrd": 8,
    "YearBuilt": 2005,
    "YearRemodAdd": 2005,
    "MasVnrArea": 150,
    "Fireplaces": 1,
    "LotArea": 9000
}

predictor = HousePricePredictor()

print(
    predictor.predict(sample)
)