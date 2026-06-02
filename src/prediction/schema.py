from pydantic import BaseModel, Field


class HouseData(BaseModel):

    OverallQual: int
    GrLivArea: float
    GarageCars: float
    GarageArea: float
    TotalBsmtSF: float

    FirstFlrSF: float = Field(
        alias="1stFlrSF"
    )

    FullBath: int
    TotRmsAbvGrd: int
    YearBuilt: int
    YearRemodAdd: int
    MasVnrArea: float
    Fireplaces: int
    LotArea: float

    model_config = {
        "populate_by_name": True
    }