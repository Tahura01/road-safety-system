# AI-Based Road Accident Severity Prediction, Dynamic Risk Assessment, and Multi-Level Hotspot Mapping System

An intelligent, full-stack, proactively engineered road safety platform designed to shift traffic management from a reactive approach to a predictive, data-driven methodology. This system leverages advanced Machine Learning for crash severity prediction, Unsupervised Spatial Clustering for pinpointing accident blackspots, and live external API integrations to evaluate dynamic risk scores in real time.

---

## 🚀 Key Features

*   **Dynamic Trip AI Prediction:** Processes incoming spatial, temporal, and real-time atmospheric data through an optimized machine learning pipeline to classify potential accident severity (Minor, Serious, Fatal) and calculate a continuous location safety score (0–100).
*   **Multi-Level Hotspot Mapping:** Dual-engine spatial intelligence clustering:
    *   **K-Means Clustering:** Defines regional, macro-level "Centers of Gravity" for high-level resource allocation.
    *   **DBSCAN (Density-Based Spatial Clustering):** Filters out random outlier accidents and charts precise geographic blackspots (e.g., sharp curves, problematic intersections) utilizing the *Haversine formula* for real-world coordinate distance in meters.
*   **Live Environmental Synergy:** Asynchronous retrieval of localized weather patterns and WMO (World Meteorological Organization) codes via the Open-Meteo API.
*   **Interactive Spatial Visualization:** Fully interactive dark-mode GIS dashboard powered by `React-Leaflet` and HTML5 Canvas rendering featuring dynamic marker clustering (restoring 60FPS fluid navigation over thousands of coordinate arrays).
*   **Citizen Reporting Framework:** A human-in-the-loop module allowing public users to drop pins on active hazards (e.g., potholes, poor street lighting). Submissions undergo reverse-geocoding polygon bounding-box validation to isolate and filter out geographic noise.
*   **Authority Control Center:** Closed-loop administration workflow enabling urban planners and traffic authorities to isolate urban hazards, track statuses (`Pending` ➔ `Under Review` ➔ `Fixed`), and strategize predictive infrastructural modifications.

---

## 🛠️ System Architecture & Tech Stack

The platform is designed around a fully decoupled, async-driven layered architecture built to scale.

### Frontend (Client Layer)
*   **Framework:** React 19 (leveraging concurrent rendering hooks)
*   **Build Engine:** Vite (Native ESM-based Hot Module Replacement)
*   **Styling Component:** Tailwind CSS (Utility-First Design System)
*   **Geospatial Rendering:** React-Leaflet / Leaflet.js
*   **Analytics Layer:** Recharts / Chart.js

### Backend (Application Layer)
*   **Framework:** FastAPI (Python 3.11) with native `async`/`await` event loops
*   **Server Core:** Uvicorn (ASGI server implementation)
*   **Client Communication Layer:** HTTPX (asynchronous third-party requests)
*   **Data Validation:** Pydantic Schemas & Auto-generated Swagger/OpenAPI docs

### Core Data & Analytics Pipeline
*   **Supervised Models:** XGBoost Classifier ($90.2\%$ Accuracy Default Engine) & Random Forest Classifier ($87.5\%$ Accuracy Baseline)
*   **Data Manipulation:** Pandas & NumPy
*   **Persistence Layer (ORM):** SQLAlchemy 2.0 (configured via Asynchronous Engines)
*   **Database Engine:** SQLite (Zero-config local development portability) / PostgreSQL target

---

## 📊 Analytical Performance Benchmarks

Evaluated utilizing a rigorous 80/20 Hold-Out Validation split on a diverse multi-modal dataset. Cost-sensitive parameters (`class_weight="balanced"`) were implemented to mitigate the standard "Accuracy Paradox" of sparse fatal metrics:

| Model Architecture | Overall Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest Baseline** | 87.5% | 0.86 | 0.85 | 0.85 |
| **XGBoost Engine (Production)** | **90.2%** | **0.89** | **0.88** | **0.88** |

---

## 📂 Project Directory Structure

```text
├── backend/
│   ├── app/
│   │   ├── core/            # Security middleware and fallback configurations
│   │   ├── database/        # Async SQLAlchemy session engines & safety.db
│   │   ├── models/          # Declarative Pydantic schemas & DB entities
│   │   ├── routes/          # FastAPI routes (/predict, /hotspots, /reports)
│   │   └── services/        # Serialized ML engines (.pkl wrappers) & API connectors
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Common UI atoms & system layout skeletons
│   │   ├── hooks/           # Custom state lifecycle hooks (usePredict, useMap)
│   │   ├── services/        # Axios configurations pointing to localized endpoints
│   │   └── views/           # Analytics Dashboard and Global Safety Map interfaces
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── package.json
└── docker-compose.yml

**⚙️ Quick Start Installation**
Ensure you have Docker Desktop installed on your host system.

1. Clone the Repository
git clone [https://github.com/Tahura01/accident-severity-prediction-system.git](https://github.com/Tahura01/accident-severity-prediction-system.git)
cd accident-severity-prediction-system

2. Configure Environment Variables
Create a .env file in the root directory to hold dynamic server variables:

VITE_API_URL=http://localhost:8000
DATABASE_URL=sqlite+aiosqlite:///./safety.db

3. Spin Up Container Infrastructure via Docker Compose
The system employs a high-efficiency multi-stage build sequence, compressing bulky machine learning binary footings (scikit-learn, xgboost, pandas) down to an optimized production layer utilizing a python:3.11-slim framework footprint.

Bash
docker-compose up --build
Once initialized:

Frontend UI dashboard attaches to: http://localhost:5173

Backend REST API endpoints attach to: http://localhost:8000

Interactive Swagger API UI docs attach to: http://localhost:8000/docs