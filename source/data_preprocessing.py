import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

from source.custom_exception import CustomException
from source.custom_logger import get_logger
from config.path_config import *
from utils.common_functions import read_yaml, load_data

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting the Data preprocessing")

            logger.info("Dropping unnecessary columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] 
                    , inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying label encoding")
            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("Label mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info("Started skewness handling")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error(f"Error during preprocessing {e}")
            raise CustomException("Error while preprocessing", e)

        
    def balance_data(self, df):
        try:
            logger.info("Balancing the data started")
            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during balancing the data {e}")
            raise CustomException("Error while balancing the data", e)
        

    def select_features(self, df):
        try:
            logger.info("Initializing the feature selection step")

            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                "feature": X.columns,
                "importance": feature_importance
            })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values

            logger.info(f"Features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature slection completed sucesfully")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error while feature selection", e)
    
    def save_data(self, df, file_path):
        try:
            logger.info("Saving our data in the processed dir")

            df.to_csv(file_path, index= False)
            logger.info(f"Data saved successfully in {file_path}")

        except Exception as e:
            logger.error(f"Error during saving processed data{e}")
            raise CustomException("Error saving data", e)
        
    def process(self):
        try:
            logger.info("Loading data from Raw Dir")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]  

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df , PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed sucesfully")    
        except Exception as e:
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error while data preprocessing pipeline", e)
              
    
    
if __name__=="__main__":
    processor = DataProcessing(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()       
    