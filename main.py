from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI(title="Mission Control AI - Prediction")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GO_API = "https://mission-control-go.onrender.com"
LOCAL_GO = "http://localhost:8080"

def get_history(sat_id="SAT-01", use_local=False):
    base = LOCAL_GO if use_local else GO_API
    try:
        r = requests.get(f"{base}/history/{sat_id}", timeout=5)
        return r.json()
    except:
        # Se a API cair, fallback mock
        return [{"time": f"12:{i:02d}:00", "temp": 70+i} for i in range(10)]

def predict_next_temps(history, steps=3):
    if len(history) < 3:
        return []
    X = np.array([[i] for i in range(len(history))])
    y = np.array([h["temp"] for h in history])
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.array([[len(history)+i] for i in range(steps)])
    preds = model.predict(future_X)
    return [round(float(p),1) for p in preds]

def check_health(temp):
    if temp > 85: return "CRITICAL"
    if temp > 75: return "WARNING"
    return "NOMINAL"

@app.get("/")
def root():
    return {
        "service": "Mission Control AI",
        "go_api": GO_API,
        "endpoints": ["/predict/{sat_id}", "/history/{sat_id}", "/health"]
    }

@app.get("/health")
def health():
    return {"status": "ok", "model": "LinearRegression", "source": "mission-control-go"}

@app.get("/predict/{sat_id}")
def predict(sat_id: str):
    history = get_history(sat_id)
    if not history:
        return {"error": "sem historico", "sat_id": sat_id}
    
    preds = predict_next_temps(history, steps=3)
    last_temp = history[-1]["temp"] if history else 0
    
    # Previsão de possível falha
    will_critical = any(t > 85 for t in preds)
    will_warning = any(t > 75 for t in preds)
    
    return {
        "sat_id": sat_id,
        "ultimo": {"time": history[-1]["time"], "temp": last_temp, "status": check_health(last_temp)},
        "historico_len": len(history),
        "proximas_temps": preds,
        "previsao": "CRITICAL em ~20-30s" if will_critical else "WARNING em breve" if will_warning else "NOMINAL estavel",
        "modelo": "LinearRegression treinado com {} pontos".format(len(history))
    }

@app.get("/history/{sat_id}")
def history_proxy(sat_id: str):
    return get_history(sat_id)