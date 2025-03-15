from pydantic import BaseModel

class ReservationPrediction(BaseModel):
    lead_time: float
    no_of_special_requests: float
    avg_price_per_room: float
    arrival_month: int
    arrival_date: int
    market_segment_type: int
    no_of_week_nights: int
    no_of_weekend_nights: int
    type_of_meal_plan: int  # Assuming meal plan is an integer, like 0 for no plan
    room_type_reserved: int

