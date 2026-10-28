# Design Document: Weather Dashboard

## 1. Visual Theme & Atmosphere
The dashboard employs an airy, modern **Blue & White** aesthetic reminiscent of clear skies, designed for high readability, visual clarity, and student-friendly accessibility.

- **Background:** Soft gradient from light sky blue (`#e0f2fe`) to crisp off-white (`#f8fafc`).
- **Primary Accent:** Vivid royal blue (`#0284c7` / `#0369a1`) for buttons, active indicators, and highlights.
- **Card Surfaces:** Pure white (`#ffffff`) with subtle translucent shadows (`rgba(15, 23, 42, 0.08)`) and soft rounded borders (`16px`).
- **Typography:** Modern clean sans-serif system stack (`'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif`).
- **Text Colors:**
  - Headings / Primary: Deep slate navy (`#0f172a`)
  - Subheadings / Body: Cool slate grey (`#475569`)
  - Subtle Labels: Muted blue-grey (`#64748b`)

---

## 2. Page Layout & Component Hierarchy

```
+---------------------------------------------------------------+
|                      HEADER & TITLE                           |
|      Weather Classification using Support Vector Machine      |
|  Enter any city to fetch live weather data & predict climate  |
+---------------------------------------------------------------+
|                      CITY SEARCH BAR                          |
|   [ 🔍 Enter city (e.g. London, Tokyo) ]  [ Fetch Weather ]   |
+---------------------------------------------------------------+
|                    STATUS & NOTIFICATIONS                     |
|           (Loading Spinner / Error Message Toast)             |
+---------------------------------------------------------------+
|                       WEATHER CARDS                           |
|  +--------------+ +--------------+ +--------------+ +-------+ |
|  | Temperature  | |   Humidity   | |  Wind Speed  | | ...   | |
|  |    22.5 °C   | |     65 %     | |   14.2 km/h  | |       | |
|  +--------------+ +--------------+ +--------------+ +-------+ |
+---------------------------------------------------------------+
|                 SVM CLASSIFICATION SHOWCASE                   |
|                  [ ⚡ Classify Weather Now ]                  |
|                                                               |
|        Predicted Weather:  [ ☀️ Sunny / 🌧️ Rainy ]           |
|         Confidence: 94.2%   | Model: RBF-Kernel SVM           |
+---------------------------------------------------------------+
|                   MODEL EVALUATION METRICS                    |
|   Accuracy: 89.7% | Precision: 90% | Recall: 90% | F1: 90%    |
+---------------------------------------------------------------+
|                         FOOTER                                |
+---------------------------------------------------------------+
```

---

## 3. Key Components & States

### A. Search Section
- Clean input field with clear placeholder text, focus ring (`#38bdf8`), and accessible `<label>`.
- Responsive "Fetch Weather" button with hover elevation and active press effect.

### B. Weather Information Grid
- Multi-column responsive grid (collapses from 4 columns on desktop to 2 columns on tablet, 1 on mobile).
- Each card features:
  - Weather icon / symbol (e.g. 🌡️ for temp, 💧 for humidity, 💨 for wind, ⏲️ for pressure).
  - Clear label (e.g., "Atmospheric Pressure").
  - Prominent numerical measurement with proper unit (e.g., "1013.2 hPa").

### C. Prominent Prediction Card
- Highlighted central card with a soft gradient background (`linear-gradient(135deg, #f0f9ff, #e0f2fe)`).
- Distinct badge for the 4 classes:
  - **Sunny:** Warm golden-amber accent (`#f59e0b`)
  - **Rainy:** Ocean blue accent (`#0284c7`)
  - **Cloudy:** Soft steel blue accent (`#64748b`)
  - **Snowy:** Icy cyan-indigo accent (`#06b6d4`)
- Displays classification probabilities / confidence when available.

### D. Model Metrics Bar
- Displays real test evaluation scores directly from the trained model metadata.
- Clean 4-pillar badge layout: Accuracy, Precision, Recall, and F1-Score.

### E. Interactive States
- **Loading State:** Subtle CSS keyframe spinner with a helpful message: *"Fetching live atmospheric data from Open-Meteo..."*
- **Error State:** Friendly red/rose tinted alert box (`#fef2f2`, border `#fca5a5`) describing the exact problem (e.g., *"City not found. Please verify spelling."*).
- **Empty State:** Clean prompt inviting the user to search for a city or try popular suggestions (London, Tokyo, New York, Cairo, Mumbai).
