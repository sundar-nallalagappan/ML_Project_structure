import pandas as pd
import numpy as np
from dataclasses import dataclass

import os, sys

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor, RandomForestRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRFRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

from src.exception import customException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.modeltrainconfig_obj = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr, preproc_path):
        try:
            logging.info("Train test split")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1], train_arr[:,-1],
                test_arr[:,:-1], test_arr[:,-1]
            )

            logging.info("Shape of X_train, y_train - {} {}".format(X_train.shape, y_train.shape))
            logging.info("Shape of X_test, y_test   - {} {}".format(X_test.shape, y_test.shape))

            models = {
            "LinearModel" : LinearRegression(),
            "Ridge"       : Ridge(),
            "Lasso"       : Lasso(),
            "KNN"         : KNeighborsRegressor(),
            "SVR"         : SVR(),
            "DecisionTree": DecisionTreeRegressor(),
            "Randomforest": RandomForestRegressor(),
            "XGboost"     : XGBRFRegressor(),
            "Catboost"    : CatBoostRegressor()
            }

            model_report:dict = evaluate_models(X_train, y_train, X_test, y_test, models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index((max(sorted(model_report.values()))))]
            logging.info("Best model name & score {} | {} ".format(best_model_name, best_model_score))
            
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                logging.info("No best model found as none of the score is more than 0.6")
                raise customException("no best model found", sys)

            save_object(
                file_path=self.modeltrainconfig_obj.trained_model_file_path,
                obj=best_model
            )

            return best_model_score

        except Exception as e:
            logging.info("Issue with ModelTrainer")
            raise customException(e, sys)

if __name__ == "__main__":
    mt = ModelTrainer()
    mt.initiate_model_trainer()


