from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from src.prediction.predict import HousePricePredictor
from src.prediction.schema import HouseData


app = FastAPI(
    title="House Price Prediction API",
    version="1.0"
)

predictor = HousePricePredictor()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": None
        }
    )


@app.post("/predict-form", response_class=HTMLResponse)
def predict_form(
    request: Request,

    OverallQual: int = Form(...),
    GrLivArea: float = Form(...),
    GarageCars: float = Form(...),
    GarageArea: float = Form(...),
    TotalBsmtSF: float = Form(...),
    YearBuilt: int = Form(...),
    LotArea: float = Form(...),

    FirstFlrSF: float = Form(None),
    FullBath: int = Form(None),
    TotRmsAbvGrd: int = Form(None),
    YearRemodAdd: int = Form(None),
    MasVnrArea: float = Form(None),
    Fireplaces: int = Form(None),
):

    FirstFlrSF = FirstFlrSF if FirstFlrSF is not None else GrLivArea
    FullBath = FullBath if FullBath is not None else 2
    TotRmsAbvGrd = TotRmsAbvGrd if TotRmsAbvGrd is not None else 6
    YearRemodAdd = YearRemodAdd if YearRemodAdd is not None else YearBuilt
    MasVnrArea = MasVnrArea if MasVnrArea is not None else 0
    Fireplaces = Fireplaces if Fireplaces is not None else 1

    input_data = {
        "OverallQual": OverallQual,
        "GrLivArea": GrLivArea,
        "GarageCars": GarageCars,
        "GarageArea": GarageArea,
        "TotalBsmtSF": TotalBsmtSF,
        "1stFlrSF": FirstFlrSF,
        "FullBath": FullBath,
        "TotRmsAbvGrd": TotRmsAbvGrd,
        "YearBuilt": YearBuilt,
        "YearRemodAdd": YearRemodAdd,
        "MasVnrArea": MasVnrArea,
        "Fireplaces": Fireplaces,
        "LotArea": LotArea
    }

    prediction = predictor.predict(input_data)

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "prediction": f"{prediction:,.0f}"
    }
)


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

    prediction = predictor.predict(input_data)

    return {
        "predicted_price": round(prediction, 2)
    }