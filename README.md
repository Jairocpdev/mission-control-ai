# 🚀 Mission Control AI

IA que prevê falha de satélites consumindo a API Go `mission-control-go`.

**Baseado nos seus repos:** `rag-agent` (FastAPI + FAISS) e `ml-titanic` (67.1% acurácia Sklearn)

## O que faz

- Consome `GET https://mission-control-go.onrender.com/history/SAT-01`
- Treina `LinearRegression` com últimos 20 pontos de temperatura
- Prevê próximas 3 temperaturas (10s, 20s, 30s)
- Retorna `CRITICAL em ~20-30s` se previsão >85°C

## Endpoints

| Rota | Descrição |
|------|-----------|
| `/` | Info |
| `/health` | Status modelo |
| `/predict/SAT-01` | Previsão com IA |
| `/history/SAT-01` | Proxy histórico Go API |

## Rodar local

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Abre: http://localhost:8001/predict/SAT-01

Exemplo resposta:
```json
{
  "sat_id": "SAT-01",
  "ultimo": {"time": "12:00:52", "temp": 82, "status": "WARNING"},
  "proximas_temps": [83.1, 84.3, 85.5],
  "previsao": "CRITICAL em ~20-30s"
}
```

## Stack

- FastAPI (igual rag-agent)
- Scikit-Learn LinearRegression (igual ml-titanic)
- Requests consumindo Go API

## Próximos passos

- [ ] Adicionar DistilBERT para analisar logs
- [ ] Salvar modelo com pickle
- [ ] Dockerfile igual Go