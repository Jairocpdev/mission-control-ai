# 🚀 Mission Control AI

[[AI API LIVE](https://img.shields.io/badge/AI%20API-LIVE%20%40%20Render-success?style=for-the-badge&logo=render)](https://mission-control-ai.onrender.com)
[[Go API](https://img.shields.io/badge/Go%20API-LIVE-blue?style=for-the-badge&logo=go)](https://mission-control-go.onrender.com)
[[Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[[FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)

**LIVE:** https://mission-control-ai.onrender.com/predict/SAT-01 → consome Go API https://mission-control-go.onrender.com/history/SAT-01

Consome `https://mission-control-go.onrender.com/history/SAT-01` e prevê falha com LinearRegression.

**Teste direto:** https://mission-control-ai.onrender.com/predict/SAT-01

## O que faz

- Consome `GET https://mission-control-go.onrender.com/history/SAT-01` (20 pontos BRT)
- Treina `LinearRegression` com últimos pontos de temperatura
- Prevê próximas 3 temperaturas (10s, 20s, 30s)
- Retorna `CRITICAL em ~20-30s` se previsão >85°C
- Fallback com dados mockados se Go API dormir (Render free tier)

## Endpoints

| Rota | Descrição |
| --- | --- |
| `/` | Info + links |
| `/health` | Status modelo |
| `/predict/SAT-01` | Previsão com IA |
| `/history/SAT-01` | Proxy histórico Go API |

## Rodar local

```
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Abre: http://localhost:8001/predict/SAT-01

Exemplo resposta:

```
{
  "sat_id": "SAT-01",
  "ultimo": {"time": "12:00:52", "temp": 82, "status": "WARNING"},
  "proximas_temps": [83.1, 84.3, 85.5],
  "previsao": "CRITICAL em ~20-30s",
  "modelo": "LinearRegression treinado com 10 pontos"
}
```

## Stack

- FastAPI (igual rag-agent)
- Scikit-Learn LinearRegression (igual ml-titanic 67.1% acurácia)
- Requests consumindo Go API
- Docker + Render

## Arquitetura

```
Go API (mission-control-go.onrender.com)
   ↓ GET /history/SAT-01 (20 pontos BRT)
Python AI (mission-control-ai.onrender.com)
   ↓ LinearRegression
Predict /predict/SAT-01 → CRITICAL em ~20s
```

Microserviços: Go gera dado, Python prevê falha.

## Próximos passos

- [x] Deploy Render LIVE
- [x] Fallback mock se Go dormir
- [ ] Adicionar DistilBERT para analisar logs (igual genai-financeiro)
- [ ] Salvar modelo com pickle
- [ ] Teste unitário CheckHealth

## Autor

Jairo Andrade - Nilópolis/RJ - 305→500 contribuições 2026
Portfolio: https://jairo-andrade.vercel.app
Go API: https://github.com/Jairocpdev/mission-control-go
