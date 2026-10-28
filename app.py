"""
app.py
======
Flask backend for the Weather Classification web application.
Connects the web frontend with:
1. Open-Meteo Geocoding and Forecast APIs to retrieve live atmospheric measurements.
2. Trained Support Vector Machine (SVM) pipeline to classify weather.

Routes:
- GET  /             : Serves the dashboard HTML interface.
- GET  /api/weather  : Retrieves current weather data for a specified city.
- POST /api/predict  : Predicts the weather class (Sunny, Rainy, Cloudy, Snowy) using the SVM.
- GET  /api/metrics  : Returns trained model evaluation scores (accuracy, precision, recall, F1).
"""

import os
import requests
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Paths and model configuration
MODEL_PATH = os.path.join("models", "weather_model.joblib")
FEATURE_COLUMNS = [
    "Temperature",
    "Humidity",
    "Wind Speed",
    "Precipitation (%)",
    "Atmospheric Pressure",
    "UV Index",
    "Visibility (km)"
]

# Global cache for loaded model and metrics
model_pipeline = None
model_metrics = None


def load_model():
    """
    Safely loads the trained SVM pipeline and evaluation metrics from disk.
    Supports both bundled dictionary and direct Pipeline artifacts.
    """
    global model_pipeline, model_metrics
    if os.path.exists(MODEL_PATH):
        try:
            saved_obj = joblib.load(MODEL_PATH)
            if isinstance(saved_obj, dict) and "pipeline" in saved_obj:
                model_pipeline = saved_obj["pipeline"]
                model_metrics = saved_obj.get("metrics", {})
            else:
                model_pipeline = saved_obj
                model_metrics = getattr(saved_obj, "custom_metrics_", {})
            print(f"[INFO] Successfully loaded model from '{MODEL_PATH}'")
        except Exception as e:
            print(f"[WARNING] Failed to load model from '{MODEL_PATH}': {e}")
            model_pipeline = None
            model_metrics = None
    else:
        print(f"[WARNING] Model file not found at '{MODEL_PATH}'. Run train_model.py first.")
        model_pipeline = None
        model_metrics = None


# Load model at startup
load_model()


@app.route("/")
def index():
    """Renders the main dashboard page."""
    return render_template("index.html")


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """
    Returns the evaluation metrics from model training.
    """
    if model_metrics:
        return jsonify({
            "success": True,
            "metrics": model_metrics
        })
    return jsonify({
        "success": False,
        "error": "Model metrics not available. Please train the model using 'python train_model.py'."
    }), 404


@app.route("/api/weather", methods=["GET"])
def get_weather():
    """
    Fetches live weather data for a given city using Open-Meteo APIs.
    Query param: city (string)
    """
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"success": False, "error": "City name is required."}), 400

    try:
        # 1. Geocoding API: lookup city coordinates
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_resp = requests.get(geocode_url, timeout=10)

        if geo_resp.status_code != 200:
            return jsonify({
                "success": False,
                "error": f"Geocoding service returned status {geo_resp.status_code}."
            }), 502

        geo_data = geo_resp.json()
        results = geo_data.get("results")
        if not results or len(results) == 0:
            return jsonify({
                "success": False,
                "error": f"City '{city}' not found. Please check spelling."
            }), 404

        top_result = results[0]
        latitude = top_result.get("latitude")
        longitude = top_result.get("longitude")
        resolved_name = top_result.get("name", city)
        country = top_result.get("country", "")

        # 2. Forecast API: fetch current atmospheric measurements
        # Requesting parameters that match the Kaggle dataset measurements
        forecast_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&"
            f"current=temperature_2m,relative_humidity_2m,precipitation_probability,"
            f"surface_pressure,wind_speed_10m,cloud_cover,uv_index,visibility"
        )
        forecast_resp = requests.get(forecast_url, timeout=10)

        if forecast_resp.status_code != 200:
            return jsonify({
                "success": False,
                "error": f"Weather service returned status {forecast_resp.status_code}."
            }), 502

        current = forecast_resp.json().get("current", {})

        # 3. Clean and convert units to match model training features
        # Visibility from Open-Meteo is in meters; convert to kilometers (km)
        raw_visibility = current.get("visibility")
        visibility_km = round(raw_visibility / 1000.0, 1) if raw_visibility is not None else 10.0

        # Precipitation probability percentage (0 - 100)
        raw_precip = current.get("precipitation_probability")
        precip_pct = float(raw_precip) if raw_precip is not None else 0.0

        # UV Index
        raw_uv = current.get("uv_index")
        uv_val = float(raw_uv) if raw_uv is not None else 0.0

        weather_data = {
            "city": resolved_name,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "measurements": {
                "Temperature": round(float(current.get("temperature_2m", 20.0)), 1),
                "Humidity": int(round(float(current.get("relative_humidity_2m", 50.0)))),
                "Wind Speed": round(float(current.get("wind_speed_10m", 10.0)), 1),
                "Precipitation (%)": precip_pct,
                "Atmospheric Pressure": round(float(current.get("surface_pressure", 1013.25)), 2),
                "UV Index": uv_val,
                "Visibility (km)": visibility_km,
                # Cloud cover displayed on the dashboard for user awareness
                "Cloud Cover (%)": current.get("cloud_cover", 0)
            }
        }

        return jsonify({
            "success": True,
            "data": weather_data
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Request to weather API timed out. Please try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Network error contacting weather API: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/predict", methods=["POST"])
def predict_weather():
    """
    Classifies weather using the trained SVM pipeline.
    Accepts JSON body with numeric measurements matching FEATURE_COLUMNS.
    """
    global model_pipeline
    if model_pipeline is None:
        load_model()
        if model_pipeline is None:
            return jsonify({
                "success": False,
                "error": "Trained model not found. Please run 'python train_model.py' first."
            }), 503

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"success": False, "error": "Invalid request: JSON body required."}), 400

    # Extract and validate required features
    input_values = {}
    missing_fields = []
    for col in FEATURE_COLUMNS:
        val = payload.get(col)
        if val is None:
            missing_fields.append(col)
        else:
            try:
                input_values[col] = float(val)
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": f"Field '{col}' must be a valid number."
                }), 400

    if missing_fields:
        return jsonify({
            "success": False,
            "error": f"Missing required feature fields: {missing_fields}"
        }), 400

    try:
        # Create single-row DataFrame with the exact column order used during training
        input_df = pd.DataFrame([input_values], columns=FEATURE_COLUMNS)

        # Predict using SVM pipeline (handles StandardScaler scaling internally)
        prediction = model_pipeline.predict(input_df)[0]

        # Extract probability confidence scores if available
        confidence = None
        probabilities = {}
        if hasattr(model_pipeline, "predict_proba"):
            probs = model_pipeline.predict_proba(input_df)[0]
            classes = list(model_pipeline.classes_)
            for cls, prob in zip(classes, probs):
                probabilities[cls] = round(float(prob) * 100, 1)
            pred_idx = classes.index(prediction)
            confidence = round(float(probs[pred_idx]) * 100, 1)

        return jsonify({
            "success": True,
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "input_features": input_values
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error running model prediction: {str(e)}"
        }), 500


if __name__ == "__main__":
    # Start local Flask development server
    print("=" * 60)
    print(" Starting Weather Classification Web Server")
    print(" Local address: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)