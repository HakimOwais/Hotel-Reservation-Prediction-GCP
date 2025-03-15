import os
import joblib
from config.path_config import MODEL_OUTPUT_PATH

#Deserialization
def load_pipeline():
    model_loaded = joblib.load(MODEL_OUTPUT_PATH)
    print(f"Model has been loaded")
    return model_loaded

if __name__=="__main__":
    load_pipeline()