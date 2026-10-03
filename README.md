# Smart Garbage Collection Monitoring and Prediction System

## Problem
Irregular garbage collection causes waste accumulation, overflowing bins, and environmental problems. Traditional static routing leads to inefficient collection schedules where empty bins are collected and overflowing bins are missed.

## Solution
This system provides a modern solution using data analytics, GIS, and Machine Learning.
1. **Monitor**: Track real-time fill levels and collection statuses across city bins.
2. **Predict**: Use Machine Learning to predict the overflow risk of a bin based on historical collection delays, fill rates, and complaints.
3. **Act**: Allow admins to reroute and prioritize collections, while residents can easily report missed collections.

## Architecture
Resident/Admin
↓
Next.js Frontend
↓
FastAPI REST API
↓
SQLite Database
↓
Analytics + Collection Monitoring
↓
ML Prediction
↓
Dashboard + GIS Map

## Technologies
* **Frontend**: Next.js, TypeScript, Tailwind CSS, Recharts, Leaflet, React Leaflet
* **Backend**: FastAPI, Python, SQLite, SQLAlchemy, Pydantic
* **AI/ML**: scikit-learn (RandomForestClassifier)

---

## Running the project

### 1. Backend Setup

Open a Windows PowerShell terminal and run the following commands from the root directory of the project:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```
This will set up the database, train the ML model, seed the system with mock data, and start the FastAPI backend on `http://localhost:8000`. 
Swagger UI is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

Open a new Windows PowerShell terminal and run:

```powershell
cd frontend
npm install
npm run dev
```
The Next.js application will be available at `http://localhost:3000`.

---

## Demo Workflow (5 Minutes)
1. **Open Dashboard**: Go to `http://localhost:3000/admin`.
2. **Review KPIs**: Show total bins, delayed collections, and high-risk bins.
3. **Map Interaction**: Click on a high-risk (red) bin on the Live Map. Observe its fill percentage and status.
4. **Predict Risk**: Click "Predict Risk" on the map popup to see the ML model's confidence probability of an overflow.
5. **Resident Complaint**: Go to the Resident page (`http://localhost:3000`), and submit a "Missed Collection" report.
6. **Action & Resolution**: Return to the Admin Dashboard. See the new complaint appear. Click "Collect" on a delayed bin in the list to record a collection. Watch the status change to ON_TIME and the KPIs update immediately.
