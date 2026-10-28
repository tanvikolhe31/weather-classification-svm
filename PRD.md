# Project Requirements Document (PRD)

## Project Title
**Weather Classification Using SVM**

---

## 1. Project Overview & Purpose
This project is an educational, beginner-friendly machine learning web application. It uses a **Support Vector Machine (SVM)** classifier to predict the general weather category (such as **Sunny**, **Cloudy**, **Rainy**, or **Snowy**) based on atmospheric measurements. 

The application connects a trained machine learning model to a clean, interactive web dashboard using **Flask**. Users can search for any real-world city, retrieve live atmospheric data using the free **Open-Meteo API**, and see the SVM model's prediction in real time alongside model evaluation metrics.

---

## 2. Target Audience
- **Students & Beginners:** Learning practical machine learning workflows, data preprocessing, and model deployment.
- **Instructors & Evaluators:** Reviewing a clean, well-documented, end-to-end data science project without complex dependencies.
- **Self-learners:** Seeking to understand how trained scikit-learn models interface with real-world web APIs.

---

## 3. Key Features
1. **Model Training & Preprocessing:**
   - Automated training pipeline (`train_model.py`) that loads `data/weather.csv`.
   - Feature inspection, validation, and zero data leakage.
   - Standard scaling (`StandardScaler`) and RBF-kernel SVM (`SVC`) bundled into a reusable `Pipeline`.
   - Realistic evaluation metrics: Accuracy, Precision, Recall, and F1-Score saved for UI display.
2. **Live City Weather Search:**
   - Search bar supporting any global city.
   - Coordinates lookup via Open-Meteo Geocoding API.
   - Current atmospheric measurements retrieval via Open-Meteo Forecast API.
3. **Interactive Web Dashboard:**
   - Clean, modern blue-and-white theme.
   - Key atmospheric cards: Temperature, Humidity, Wind Speed, Atmospheric Pressure, Cloud Cover, Precipitation Probability, UV Index, and Visibility.
   - "Classify Weather" button to trigger the SVM prediction.
   - Prominent display of predicted category with relevant visual badges and icons.
   - Display of model evaluation metrics (accuracy, precision, recall, F1).
4. **Robust Error Handling:**
   - Helpful, human-readable notifications for invalid city names, missing files, network errors, or missing data.

---

## 4. Dataset & SVM Algorithm
- **Dataset Source:** `data/weather.csv` (13,200 records, 11 columns).
- **Target Variable:** `Weather Type` (4 balanced classes: `Rainy`, `Cloudy`, `Sunny`, `Snowy` with 3,300 samples each).
- **Features Used:**
  - `Temperature` (°C)
  - `Humidity` (%)
  - `Wind Speed` (km/h)
  - `Precipitation (%)` (%)
  - `Atmospheric Pressure` (hPa)
  - `UV Index` (0–14)
  - `Visibility (km)` (km)
- **Algorithm:** Support Vector Classifier (`SVC`) with Radial Basis Function (`rbf`) kernel.
- **Artifact:** Saved as `models/weather_model.joblib`.

---

## 5. Live Weather API Integration
- **Geocoding API:** `https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1`
- **Forecast API:** `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,surface_pressure,wind_speed_10m,cloud_cover,uv_index,visibility`
- **Feature Consistency:** Measurements are converted into the exact units and names expected by the trained model pipeline before prediction.

---

## 6. Project Limitations & Honest Disclosures
- **Dataset Disparity:** The Kaggle dataset contains synthetic/historical distributions where `Season` and `Location` are categorical columns. Because live weather sensors do not provide static tags like "mountain" or "inland", we select purely physical atmospheric measurements (`Temperature`, `Humidity`, `Wind Speed`, `Precipitation`, `Pressure`, `UV Index`, `Visibility`) to ensure scientific validity and consistency between training and live inference.
- **Local Weather Volatility:** Live microclimates may exhibit borderline atmospheric values that challenge strict 4-class categorization.
- **No Ground-Truth Live Verification:** We do not use Open-Meteo's built-in weather condition code as the SVM output; the SVM makes an independent prediction based solely on sensor numbers.
