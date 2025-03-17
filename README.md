# Hotel Reservation Cancellation Prediction

## Problem Statement
The rise of online hotel reservation platforms has significantly influenced customer behavior. However, a considerable number of reservations are canceled or result in no-shows. The common reasons for cancellations include changes in plans, scheduling conflicts, or the flexibility to cancel with little to no charge. While this benefits hotel guests, it negatively impacts hotel revenue and operational efficiency.

**Objective:** Can we predict if a customer will honor their reservation or cancel it? This project aims to develop a machine learning model to make accurate predictions based on historical booking data.

---

## Solution Approach
This project follows an end-to-end MLOps pipeline to predict hotel reservation cancellations. It involves:

1. **Data Ingestion & Processing:**
   - Collect and preprocess reservation data using Python.
   - Store data securely in **Google Cloud Bucket**.
   
2. **Model Training & Experimentation:**
   - Train a machine learning model using Python.
   - Use **Scikit-learn** and other ML libraries to develop and evaluate predictive models.
   - Track experiments and model performance using **MLflow**.

3. **Model Deployment:**
   - Containerize the model using **Docker**.
   - Implement CI/CD using **Jenkins**.
   - Deploy the model using **Google Cloud Run**.

4. **API Integration:**
   - Serve the model using **FastAPI**.
   - Expose REST API endpoints for predictions.

---

## How to Run the Project
### 1. Clone the Repository
```bash
git clone <repo-url>
cd <repo-directory>
```

### 2. Train the Model
Run the training pipeline using:
```bash
python pipeline/training_pipeline.py
```

### 3. Test the Model using FastAPI
After training the model, test it locally by running the FastAPI application:
```bash
python application/api.py
```

Then send a request to the API:
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"feature1": value, "feature2": value, ...}'
```

### 4. Deploy the Model
Use Docker to build and run the container:
```bash
docker build -t hotel-reservation-predictor .
docker run -p 8000:8000 hotel-reservation-predictor
```

Alternatively, deploy using Google Cloud Run:
```bash
gcloud run deploy hotel-reservation-predictor --image gcr.io/<project-id>/hotel-reservation-predictor --platform managed
```

---

## Technologies Used
- **Python**: Data ingestion, processing, and model training
- **MLflow**: Experiment tracking and model versioning
- **Google Cloud Bucket**: Data storage
- **Docker**: Containerization
- **Jenkins**: CI/CD pipeline
- **Google Cloud Run**: Model deployment
- **FastAPI**: API service for model predictions

---

## Future Improvements
- Enhance model performance with additional features
- Implement automated model monitoring and retraining
- Integrate a front-end dashboard for better visualization

---

## License
This project is open-source and available under the MIT License.
