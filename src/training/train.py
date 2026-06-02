import os
import sys
import json
import pickle

import pandas as pd

import mlflow
import mlflow.sklearn
import dagshub

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    root_mean_squared_error
)

from src.logger import logger
from src.exception import CustomException


FEATURES = [
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "GarageArea",
    "TotalBsmtSF",
    "1stFlrSF",
    "FullBath",
    "TotRmsAbvGrd",
    "YearBuilt",
    "YearRemodAdd",
    "MasVnrArea",
    "Fireplaces",
    "LotArea"
]

TARGET = "SalePrice"


def load_data():
    df = pd.read_csv("artifacts/raw/train.csv")

    df = df[FEATURES + [TARGET]]

    df["MasVnrArea"] = df["MasVnrArea"].fillna(
        df["MasVnrArea"].median()
    )

    return df


def evaluate_model(model, X_train, X_test, y_train, y_test):

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "r2": float(
            r2_score(y_test, predictions)
        ),
        "mae": float(
            mean_absolute_error(
                y_test,
                predictions
            )
        ),
        "rmse": float(
            root_mean_squared_error(
                y_test,
                predictions
            )
        )
    }

    return metrics


def save_model(model):

    os.makedirs("artifacts", exist_ok=True)

    with open(
        "artifacts/model.pkl",
        "wb"
    ) as file:
        pickle.dump(model, file)


def save_metrics(metrics):

    with open(
        "artifacts/metrics.json",
        "w"
    ) as file:
        json.dump(
            metrics,
            file,
            indent=4
        )


def save_features():

    with open(
        "artifacts/features.json",
        "w"
    ) as file:
        json.dump(
            FEATURES,
            file,
            indent=4
        )


def main():

    try:

        logger.info(
            "Training pipeline started"
        )

        dagshub.init(
            repo_owner="dimpalpanchal68",
            repo_name="House-Price-Prediction",
            mlflow=True
        )

        mlflow.set_experiment(
            "HousePricePrediction"
        )

        df = load_data()

        X = df.drop(columns=[TARGET])
        y = df[TARGET]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        models = {
            "LinearRegression":
                LinearRegression(),

            "DecisionTree":
                DecisionTreeRegressor(
                    random_state=42
                ),

            "RandomForest":
                RandomForestRegressor(
                    random_state=42
                ),

            "GradientBoosting":
                GradientBoostingRegressor(
                    random_state=42
                )
        }

        results = {}

        best_model = None
        best_model_name = None
        best_score = -1

        for name, model in models.items():

            with mlflow.start_run(
                run_name=name
            ):

                logger.info(
                    f"Training {name}"
                )

                metrics = evaluate_model(
                    model,
                    X_train,
                    X_test,
                    y_train,
                    y_test
                )

                results[name] = metrics

                mlflow.log_param(
                    "model_name",
                    name
                )

                mlflow.log_metric(
                    "r2",
                    metrics["r2"]
                )

                mlflow.log_metric(
                    "mae",
                    metrics["mae"]
                )

                mlflow.log_metric(
                    "rmse",
                    metrics["rmse"]
                )

                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model"
                )

                logger.info(
                    f"{name} Metrics: {metrics}"
                )

                if metrics["r2"] > best_score:

                    best_score = metrics["r2"]
                    best_model = model
                    best_model_name = name

        save_model(best_model)

        results["best_model"] = best_model_name

        save_metrics(results)

        save_features()

        print("\nTraining Completed")
        print(f"Best Model : {best_model_name}")
        print(f"Best R2    : {best_score:.4f}")

        logger.info(
            f"Best Model: {best_model_name}"
        )

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()