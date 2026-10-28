# Weather Classification Using Support Vector Machine (SVM)

A functional, beginner-friendly machine learning web application that classifies weather conditions (**Sunny**, **Cloudy**, **Rainy**, or **Snowy**) based on atmospheric measurements. 

The application uses an RBF-kernel Support Vector Machine (SVM) trained on a historical weather dataset, paired with the free **Open-Meteo API** to fetch live atmospheric data for any city in the world through a clean, modern web dashboard.

---

## 🌟 Key Features
- **Machine Learning with SVM:** Evaluates atmospheric features using a standard-scaled RBF-kernel Support Vector Classifier.
- **High Performance:** Achieves **89.73% test accuracy** across four balanced weather classes.
- **Live Weather Integration:** Searches any city globally via Open-Meteo Geocoding and retrieves live atmospheric data via Open-Meteo Forecast API.
- **Interactive Web Interface:** Clean sky-blue and white design built with vanilla HTML, CSS, and JavaScript.
- **Model Transparency:** Shows real-time prediction confidence, probability distributions, and actual test evaluation metrics directly on the dashboard.
- **Beginner-Friendly Architecture:** No complex frameworks, external databases, or heavy dependencies.

---

## 🛠️ Technologies Used
- **Python 3:** Core programming language.
- **Flask:** Lightweight web server connecting the ML model to the browser.
- **Scikit-learn:** Data preprocessing (`StandardScaler`) and classification (`SVC`).
- **Pandas:** Tabular data processing and feature selection.
- **Joblib:** Serializing and loading the trained model pipeline.
- **Requests:** Fetching live weather data from Open-Meteo.
- **HTML5 & Vanilla CSS:** Modern, responsive blue-and-white dashboard styling.
- **Vanilla JavaScript:** Client-side event handling and asynchronous API requests.

---

## 📁 Project Structure
```text
WeatherClassification/
├── PRD.md                       # Project Requirements Document
├── Architecture.md              # System flow, diagrams, and components
├── rules.md                     # Coding rules and engineering guidelines
├── phases.md                    # Development phases and acceptance tracking
├── design.md                    # UI layout, color palette, and design specs
├── memory.md                    # Project development progress log
│
├── app.py                       # Flask backend and API endpoints
├── train_model.py               # Dataset processing, SVM training, & evaluation
├── requirements.txt             # Python package dependencies
├── README.md                    # Documentation and setup guide
│
├── data/
│   └── weather.csv              # Historical Kaggle weather dataset
│
├── models/
│   └── weather_model.joblib     # Saved scikit-learn SVM pipeline & metrics
│
├── templates/
│   └── index.html               # Main dashboard HTML template
│
└── static/
    ├── style.css                # Sky blue & white responsive stylesheet
    └── script.js                # Frontend API fetch and DOM logic
```

---

## 📊 Features & Model Specifications

### Input Features Used:
1. `Temperature` (°C)
2. `Humidity` (%)
3. `Wind Speed` (km/h)
4. `Precipitation (%)` (%)
5. `Atmospheric Pressure` (hPa)
6. `UV Index` (0 - 14)
7. `Visibility (km)` (km)

### Target Categories:
- `Sunny`
- `Cloudy`
- `Rainy`
- `Snowy`

### Model Evaluation Scores (Unseen Kaggle Test Set, 2,640 samples):
- **Accuracy:** 89.73%
- **Weighted Precision:** 89.87%
- **Weighted Recall:** 89.73%
- **Weighted F1-Score:** 89.77%

---

## 🚀 How to Run the Project (Windows)

Open **PowerShell** or **Command Prompt** in the project directory:

### 1. Create a Virtual Environment (Optional but Recommended)
```powershell
python -m venv .venv
```

### 2. Activate the Virtual Environment
```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 4. Train the SVM Model
Run the training script to load `data/weather.csv`, evaluate the classifier, and generate `models/weather_model.joblib`:
```powershell
python train_model.py
```

### 5. Start the Web Server
Launch the Flask development server:
```powershell
python app.py
```

### 6. View the Dashboard
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 💡 How to Use the Application
1. **Search for a City:** Enter any city name (e.g. *London*, *Tokyo*, *New York*, *Cairo*, *Sydney*) into the search box or click a quick suggestion chip.
2. **Fetch Weather:** Click **Fetch Weather** to retrieve current atmospheric conditions from Open-Meteo.
3. **View Atmospheric Cards:** Review real-time temperature, humidity, wind speed, pressure, cloud cover, and precipitation chance.
4. **Inspect SVM Classification:** The trained SVM pipeline classifies the weather type and displays the confidence percentage along with class probabilities.
5. **Review Model Performance:** Scroll to the bottom of the dashboard to view real evaluation metrics from model training.

---

## 🛡️ Error Handling
- **Missing Dataset:** If `data/weather.csv` is absent when running `train_model.py`, a clear warning message explains where to place the file.
- **Invalid City Name:** If a city cannot be resolved, an alert informs the user to check spelling.
- **Missing Model:** If the model hasn't been trained yet, `app.py` displays a friendly message instructing the user to run `python train_model.py`.
- **Network Timeouts:** Graceful error messages appear if Open-Meteo API requests take longer than expected.
