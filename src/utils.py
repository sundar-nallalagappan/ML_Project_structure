import pickle
import pandas
import os
import sys

import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score

from src.exception import customException
from src.logger import logging

def save_object(file_path, obj):
    logging.info("save_object started")

    try:                
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        logging.info("save_object Nok", str(e))
        raise customException(e, sys)
    
def get_metrics(y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2_square = r2_score(y_true, y_pred)

    return mae, rmse, r2_square
    
def evaluate_models(X_train, y_train, X_test, y_test, models):
    logging.info("Inside evaluate models function")

    try:
        report = {}
        
        for idx, (model_name, model) in enumerate(models.items()):
            print(idx, model_name, model)

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred  = model.predict(X_test)

            train_mae, train_rmse, train_r2 = get_metrics(y_train, y_train_pred)
            test_mae, test_rmse, test_r2 = get_metrics(y_test, y_test_pred)

            logging.info("Model {} : Matrics MAE {}, RMSE {}, R2 {}".format(model_name, test_mae, test_rmse, test_r2))

            report[model_name] = test_r2
        print(report)
        return report

    except Exception as e:
        logging.info("Issue with evaluate models function")
        raise customException(e, sys)