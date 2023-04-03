print("sairam")
#Global packages
from dataclasses import dataclass
import sys
import os

#Data processing
import pandas as pd
import numpy as np

#Sklearn packages
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

#utilities
from src.exception import customException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path : str=os.path.join("artifacts", "proprocessor.pkl")

class dataTransformation:
    def __init__(self):
        self.data_transformation_config_obj = DataTransformationConfig()

    def read_input(self):
        logging.info("Reading the input")
        data=pd.read_csv("Notebook\StudentsPerformance.csv")

        num_columns = data.select_dtypes(exclude='O').columns
        cat_columns = data.select_dtypes(include='O').columns

        logging.info("Numeric columns {}".format(num_columns))
        logging.info("Cat columns {}".format(cat_columns))
        print(type(num_columns), type(cat_columns))
        print(type(list(num_columns)), type(cat_columns))
        return list(num_columns), list(cat_columns)

    def get_data_transformation_object(self):
        try:
            num_columns, cat_columns = self.read_input()
            print(num_columns, cat_columns)

            try:
                num_columns.remove("math score")
                logging.info("Target feature Math score removed from the list")
            except Exception as e:
                logging.info("Error while removing the target columns from the list")
                customException(e, sys)

            #Define the pipeline for Numerical features treatmeant
            num_col_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("Scaler", StandardScaler())
            ])

            #Define the pipeline for categorical features treatmeant
            cat_col_pipeline = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehotencoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))         #got error and fixed
                ]
            )

            preprocessor = ColumnTransformer(
                [
                ("num_col_pipeline", num_col_pipeline, num_columns),
                ("cat_col_pipeline", cat_col_pipeline, cat_columns)
                ]
            )

            return preprocessor
        
        except Exception as err:
            logging.info("Error in initiate get_data_transformation_object class")
            raise customException(err, sys)
        
    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            train = pd.read_csv(train_data_path)    
            test  = pd.read_csv(test_data_path)
            logging.info("Read the input train & test files")

            logging.info("Received the data transformation object")
            preprocessor = self.get_data_transformation_object()

            target_feature_name = 'math score'

            input_features_train_df = train.drop([target_feature_name], axis=1)
            target_feature_train_df = train[target_feature_name]

            logging.info("train data split ok : train shape = {} | test shape = {}".format(input_features_train_df.shape, target_feature_train_df.shape))

            input_features_test_df = test.drop([target_feature_name], axis=1)
            target_feature_test_df = test[target_feature_name]

            logging.info("test data split ok : train shape = {} | test shape = {}".format(input_features_test_df.shape, target_feature_test_df.shape))

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_features_train_df_arr = preprocessor.fit_transform(input_features_train_df)
            input_features_test_df_arr  = preprocessor.transform(input_features_test_df)

            train_arr = np.c_[(input_features_train_df_arr, target_feature_train_df)]
            test_arr  = np.c_[(input_features_test_df_arr, target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config_obj.preprocessor_obj_file_path,
                obj = preprocessor
            )

            return train_arr, test_arr, self.data_transformation_config_obj.preprocessor_obj_file_path

        except Exception as e:
            logging.info("Error in initiate data transformation class")
            raise customException(e, sys)

        

if __name__ == "__main__":
    dt_obj = dataTransformation()
    print("zero")
    tr_p = "artifacts\\train.csv"
    te_p = "artifacts\\test.csv"

    a,b = dt_obj.initiate_data_transformation(tr_p, te_p)

    print(a)