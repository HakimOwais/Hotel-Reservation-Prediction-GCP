from fastapi import FastAPI
import uvicorn
import pandas as pd
import joblib
from application.schema import ReservationPrediction
from pipeline.inference_pipeline import load_pipeline

app = FastAPI()

# Load the model when the app starts
model_loaded = load_pipeline()

@app.get("/")
async def index():
    return "Service is healthy and running"

@app.post("/predict")
async def get_prediction(prediction_details: ReservationPrediction):
    data = prediction_details.model_dump()

    new_data = {
        'lead_time': data['lead_time'],
        'no_of_special_requests': data['no_of_special_requests'],
        'avg_price_per_room': data['avg_price_per_room'],
        'arrival_month': data['arrival_month'],
        'arrival_date': data['arrival_date'],
        'market_segment_type': data['market_segment_type'],
        'no_of_week_nights': data['no_of_week_nights'],
        'no_of_weekend_nights': data['no_of_weekend_nights'],
        'type_of_meal_plan': data['type_of_meal_plan'],
        'room_type_reserved': data['room_type_reserved'],
    }

    df = pd.DataFrame([new_data])

    # Make prediction
    prediction = model_loaded.predict(df)
    pred = 'Not Cancel' if prediction[0] == 1 else 'Cancel'

    return {"Status of Reservation": pred}


if __name__ == "__main__":
    uvicorn.run(app)