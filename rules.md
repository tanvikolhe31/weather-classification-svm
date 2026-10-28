# Project Coding & Engineering Rules

## 1. Simplicity & Beginner-Friendliness
- Write simple, explicit Python, HTML, CSS, and JavaScript without complex abstractions, metaprogramming, or obscure one-liners.
- Add clear, informative comments above every major function, pipeline step, and API call explaining *what* it does and *why*.
- Strictly stick to standard, beginner-friendly tools: Flask, scikit-learn, Pandas, Joblib, Requests, HTML, CSS, and Vanilla JS.
- Do not introduce React, Node.js, Streamlit, Docker, SQLite/PostgreSQL, authentication, or task runners.

## 2. Machine Learning & Preprocessing Integrity
- **Dataset First:** Always inspect the actual dataset columns, types, and values before writing feature-selection or preprocessing logic.
- **No Data Fabrication:** Never invent fake rows, synthesize mock predictions, or fabricate classification accuracy scores.
- **Strict Feature Consistency:** Features passed to the model during live inference must exactly match the feature names, ordering, units, and scaling applied during training.
- **Bundle Pipelines:** Save the fitted `StandardScaler` and `SVC` inside a single scikit-learn `Pipeline` to prevent train/test leakage and guarantee uniform preprocessing during inference.

## 3. Web & API Reliability
- **Input Validation:** Validate all city names and numerical inputs before processing.
- **API Error Handling:** Gracefully handle network timeouts, non-200 HTTP responses, and missing geocoding results with clear, helpful user messages.
- **No Ground-Truth Cheating:** Do not use Open-Meteo's weather code to override or simulate the SVM output. Predictions must come genuinely from the SVM model.

## 4. UI Design & User Experience
- Adhere to the clean blue-and-white visual palette with accessible contrast.
- Every interactive action (such as fetching data or running a prediction) must have visual feedback (loading spinners, disabled buttons during flight, and error alert banners).
- Ensure all form inputs have associated labels and unique IDs for accessibility and testing.

## 5. Scope Management
- Do not add features outside the agreed project scope without a clear, justified reason.
- Keep the project lightweight and easily runnable on any basic Python 3 environment.
