print("      ")
import pandas as pd 
import os
import sys
from src.logger import logging
from src.exception import customException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.components.data_transformation import dataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class dataIngestionConfig:
    raw_data_path: str=os.path.join('artifacts', 'data.csv')
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')

class dataIngestion:
    def __init__(self):
        self.Ingestion_config = dataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Start of data ingestion")
        logging.info("data ingestion - reading csv file")
        try:
            raw_data = pd.read_csv("Notebook\StudentsPerformance.csv")
            logging.info("Raw_data shape is {}".format(raw_data.shape))
            
            logging.info("Creation of directory")
            os.makedirs(os.path.dirname(self.Ingestion_config.raw_data_path), exist_ok=True)
            raw_data.to_csv(self.Ingestion_config.raw_data_path, header=True, index=False)

            train_set, test_set = train_test_split(raw_data, test_size=0.2, random_state=1702)

            logging.info("Creation of train set")
            train_set.to_csv(self.Ingestion_config.train_data_path, header=True, index=False)

            logging.info("Creation of test set")
            test_set.to_csv(self.Ingestion_config.test_data_path, header=True, index=False)

            return (
                self.Ingestion_config.train_data_path,
                self.Ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Data ingestion - Fatal error")
            customException(e, sys)
            raise e

if __name__ == "__main__":
    di = dataIngestion()
    train_data_path, test_data_path = di.initiate_data_ingestion()
    print(train_data_path, test_data_path)

    dt = dataTransformation()
    train_arr, test_arr, preproc_path = dt.initiate_data_transformation(train_data_path, test_data_path)

    print(train_arr)

    mt = ModelTrainer()
    r2score = mt.initiate_model_trainer(train_arr, test_arr, preproc_path)
    print(r2score)

