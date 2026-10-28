/**
 * script.js
 * =========
 * Handles user interactions, API communications with Flask backend,
 * dynamic DOM rendering, and SVM classification for the weather dashboard.
 */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------
    // DOM Elements
    // -------------------------------------------------------------
    const searchForm = document.getElementById("search-form");
    const cityInput = document.getElementById("city-input");
    const fetchBtn = document.getElementById("fetch-btn");
    const classifyBtn = document.getElementById("classify-btn");
    const statusBanner = document.getElementById("status-banner");
    const statusMessage = document.getElementById("status-message");
    const emptyState = document.getElementById("empty-state");
    const weatherContent = document.getElementById("weather-content");

    // Location details
    const resolvedCity = document.getElementById("resolved-city");
    const resolvedCountry = document.getElementById("resolved-country");
    const resolvedCoords = document.getElementById("resolved-coords");

    // Weather metric values
    const valTemp = document.getElementById("val-temp");
    const valHumidity = document.getElementById("val-humidity");
    const valWind = document.getElementById("val-wind");
    const valPressure = document.getElementById("val-pressure");
    const valPrecip = document.getElementById("val-precip");
    const valCloud = document.getElementById("val-cloud");
    const valUv = document.getElementById("val-uv");
    const valVisibility = document.getElementById("val-visibility");

    // Prediction showcase elements
    const weatherIconBadge = document.getElementById("weather-icon-badge");
    const predictionResult = document.getElementById("prediction-result");
    const confidenceBar = document.getElementById("confidence-bar");
    const confidenceValue = document.getElementById("confidence-value");

    // Probability breakdown bars
    const probSunny = document.getElementById("prob-sunny");
    const valProbSunny = document.getElementById("val-prob-sunny");
    const probRainy = document.getElementById("prob-rainy");
    const valProbRainy = document.getElementById("val-prob-rainy");
    const probCloudy = document.getElementById("prob-cloudy");
    const valProbCloudy = document.getElementById("val-prob-cloudy");
    const probSnowy = document.getElementById("prob-snowy");
    const valProbSnowy = document.getElementById("val-prob-snowy");

    // Model metrics elements
    const metricAccuracy = document.getElementById("metric-accuracy");
    const metricPrecision = document.getElementById("metric-precision");
    const metricRecall = document.getElementById("metric-recall");
    const metricF1 = document.getElementById("metric-f1");

    // Cache of currently fetched weather measurements
    let currentMeasurements = null;

    // Icons map for weather classes
    const WEATHER_ICONS = {
        "Sunny": "☀️",
        "Rainy": "🌧️",
        "Cloudy": "☁️",
        "Snowy": "❄️"
    };

    // -------------------------------------------------------------
    // Helper Functions
    // -------------------------------------------------------------
    function showNotification(message, type = "error") {
        statusMessage.textContent = message;
        statusBanner.className = `status-banner ${type}`;
        statusBanner.classList.remove("hidden");
    }

    function hideNotification() {
        statusBanner.classList.add("hidden");
    }

    function setButtonLoading(button, isLoading, normalText) {
        const textSpan = button.querySelector(".btn-text");
        const spinnerSpan = button.querySelector(".btn-spinner");
        if (isLoading) {
            button.disabled = true;
            if (textSpan) textSpan.textContent = "Loading...";
            if (spinnerSpan) spinnerSpan.classList.remove("hidden");
        } else {
            button.disabled = false;
            if (textSpan) textSpan.textContent = normalText;
            if (spinnerSpan) spinnerSpan.classList.add("hidden");
        }
    }

    // -------------------------------------------------------------
    // 1. Fetch Model Evaluation Metrics on Load
    // -------------------------------------------------------------
    async function loadModelMetrics() {
        try {
            const resp = await fetch("/api/metrics");
            const data = await resp.json();
            if (data.success && data.metrics) {
                const m = data.metrics;
                if (metricAccuracy && m.accuracy) metricAccuracy.textContent = (m.accuracy * 100).toFixed(2) + "%";
                if (metricPrecision && m.precision) metricPrecision.textContent = (m.precision * 100).toFixed(2) + "%";
                if (metricRecall && m.recall) metricRecall.textContent = (m.recall * 100).toFixed(2) + "%";
                if (metricF1 && m.f1_score) metricF1.textContent = (m.f1_score * 100).toFixed(2) + "%";
            }
        } catch (err) {
            console.warn("Could not retrieve model metrics from /api/metrics:", err);
        }
    }

    // -------------------------------------------------------------
    // 2. Fetch Live Weather Data for City
    // -------------------------------------------------------------
    async function fetchWeatherData(city) {
        if (!city || !city.trim()) {
            showNotification("Please enter a valid city name.", "error");
            return;
        }

        hideNotification();
        setButtonLoading(fetchBtn, true, "Fetch Weather");

        try {
            const resp = await fetch(`/api/weather?city=${encodeURIComponent(city.trim())}`);
            const data = await resp.json();

            if (!resp.ok || !data.success) {
                showNotification(data.error || "Unable to fetch weather data.", "error");
                setButtonLoading(fetchBtn, false, "Fetch Weather");
                return;
            }

            const info = data.data;
            currentMeasurements = info.measurements;

            // Render location bar
            resolvedCity.textContent = info.city;
            resolvedCountry.textContent = info.country || "Global";
            resolvedCoords.textContent = `${info.latitude.toFixed(2)}°, ${info.longitude.toFixed(2)}°`;

            // Populate measurement cards
            valTemp.textContent = currentMeasurements["Temperature"];
            valHumidity.textContent = currentMeasurements["Humidity"];
            valWind.textContent = currentMeasurements["Wind Speed"];
            valPressure.textContent = currentMeasurements["Atmospheric Pressure"];
            valPrecip.textContent = currentMeasurements["Precipitation (%)"];
            valCloud.textContent = currentMeasurements["Cloud Cover (%)"] ?? 0;
            valUv.textContent = currentMeasurements["UV Index"];
            valVisibility.textContent = currentMeasurements["Visibility (km)"];

            // Reveal weather section
            emptyState.classList.add("hidden");
            weatherContent.classList.remove("hidden");

            // Automatically trigger SVM classification so the user immediately sees ML result
            await classifyCurrentWeather();

        } catch (err) {
            showNotification("Network error occurred while fetching weather data. Please check your connection.", "error");
        } finally {
            setButtonLoading(fetchBtn, false, "Fetch Weather");
        }
    }

    // -------------------------------------------------------------
    // 3. Classify Weather Using SVM Pipeline
    // -------------------------------------------------------------
    async function classifyCurrentWeather() {
        if (!currentMeasurements) {
            showNotification("Please fetch weather data first before classifying.", "error");
            return;
        }

        setButtonLoading(classifyBtn, true, "⚡ Classify Weather With SVM");

        try {
            const resp = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(currentMeasurements)
            });

            const data = await resp.json();

            if (!resp.ok || !data.success) {
                showNotification(data.error || "Classification failed.", "error");
                setButtonLoading(classifyBtn, false, "⚡ Classify Weather With SVM");
                return;
            }

            const predictedClass = data.prediction;
            const confidence = data.confidence !== null ? data.confidence : 0;
            const probs = data.probabilities || {};

            // Render prediction showcase
            predictionResult.textContent = predictedClass;
            predictionResult.className = `prediction-result ${predictedClass.toLowerCase()}`;
            weatherIconBadge.textContent = WEATHER_ICONS[predictedClass] || "🌤️";

            confidenceValue.textContent = `${confidence}%`;
            confidenceBar.style.width = `${Math.min(100, Math.max(0, confidence))}%`;

            // Render class probability bars
            renderProbabilityBar(probSunny, valProbSunny, probs["Sunny"]);
            renderProbabilityBar(probRainy, valProbRainy, probs["Rainy"]);
            renderProbabilityBar(probCloudy, valProbCloudy, probs["Cloudy"]);
            renderProbabilityBar(probSnowy, valProbSnowy, probs["Snowy"]);

        } catch (err) {
            showNotification("An error occurred while contacting the prediction service.", "error");
        } finally {
            setButtonLoading(classifyBtn, false, "⚡ Classify Weather With SVM");
        }
    }

    function renderProbabilityBar(barEl, textEl, value) {
        const val = value !== undefined ? value : 0;
        if (barEl) barEl.style.width = `${Math.min(100, Math.max(0, val))}%`;
        if (textEl) textEl.textContent = `${val}%`;
    }

    // -------------------------------------------------------------
    // Event Listeners
    // -------------------------------------------------------------
    // Search form submit
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        fetchWeatherData(cityInput.value);
    });

    // Classify button click
    classifyBtn.addEventListener("click", () => {
        classifyCurrentWeather();
    });

    // Quick suggestion chips
    document.querySelectorAll(".chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const city = chip.getAttribute("data-city");
            cityInput.value = city;
            fetchWeatherData(city);
        });
    });

    // Initial load: metrics
    loadModelMetrics();
});
